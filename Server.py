import socket
import sys
import threading
from MessageData import MessageData
import DatabaseOperations
from FilterType import FilterType

class Server:

    def __init__(self, host, port, isOnline):
        self.host = host
        self.port = port
        self.isOnline = isOnline
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientDict = dict()

    def initializeServer(self):
        self.socket.bind((self.host, self.port))

    def waitForClients(self):
        try:
            # Maximum 10 clients can connect to the server
            self.socket.listen(10)
            print('Server is waiting for clients to connect')
            while self.isOnline:
                clientSocket, clientAddress = self.socket.accept()
                print('Connected to: ' + clientAddress[0] + ' : ' + str(clientAddress[1]))
                clientThread = threading.Thread(target=self.handleClientConnection, args=(clientSocket, ), daemon=True)
                clientThread.start()
        except ConnectionError or KeyboardInterrupt:
            self.closeServer()

    def getCurrentlyConnectedUsers(self):
        return ' , '.join(self.clientDict.keys())

    def handleListRequest(self, messageData):
        message = MessageData(content=self.getCurrentlyConnectedUsers(), type='list')
        self.clientDict[messageData.getSenderName()].send(message.serialize())

    def handleSendMessageToUser(self, messageData):
        if messageData.getReceiverName() in self.clientDict:
            DatabaseOperations.addMessage(message=messageData)
            self.clientDict[messageData.getReceiverName()].send(messageData.serialize())
        else:
            message = MessageData(content='There is no actively connected user named ' + messageData.getReceiverName())
            self.clientDict[messageData.getSenderName()].send(message.serialize())

    def handleFilterRequest(self, messageData):
        result = list()
        filterType = messageData.getType()
        if filterType.isOnlyFromMeFilter():
            result.extend(DatabaseOperations.getMessageBySenderName(messageData.getSenderName()))
        elif filterType.isOnlyToMeFilter():
            result.extend(DatabaseOperations.getMessageByReceiverName(messageData.getReceiverName()))
        message = MessageData(content=' , '.join(result), type='response')
        self.clientDict[messageData.getSenderName()].send(message.serialize())

    def handleRequests(self, data):
        message = MessageData().deserialize(data)
        if message.getType() == 'list':
            self.handleListRequest(message)
        elif message.getType() == 'message':
            self.handleSendMessageToUser(message)
        else:
            self.handleFilterRequest(message)

    def handleClientConnection(self, clientSocket):
        nickName = (clientSocket.recv(2048)).decode()
        self.clientDict[nickName] = clientSocket
        try:
            while True:
                data = clientSocket.recv(2048)
                if not data:
                    raise ConnectionError
                self.handleRequests(data)
        except ConnectionError or KeyboardInterrupt:
            self.clientDict.pop(nickName)
            clientSocket.close()

    def closeServer(self):
        print('Shutting down the server')
        self.socket.close()

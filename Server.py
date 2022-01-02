import socket
import sys
import threading
from MessageData import MessageData

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
                clientThread = threading.Thread(target=self.handleClientConnection, args=(clientSocket, ))
                clientThread.start()
        except ConnectionError:
            self.closeServer()

    def handleListRequest(self, messageData):
        listMessageContent = ' , '.join(self.clientDict.keys())
        message = MessageData(content=listMessageContent, type='list')
        self.clientDict[messageData.getSenderName()].send(message.serialize())

    def handleSendMessageToUser(self, messageData):
        if messageData.getReceiverName() in self.clientDict:
            # save to database in here
            self.clientDict[messageData.getReceiverName()].send(messageData.serialize())
        else:
            message = MessageData(content='There is no actively connected user named ' + messageData.getReceiverName())
            self.clientDict[messageData.getSenderName()].send(message.serialize())

    def handleRequests(self, data):
        message = MessageData().deserialize(data)
        if message.getType() == 'list':
            self.handleListRequest(message)
        elif message.getType() == 'message':
            self.handleSendMessageToUser(message)

    def handleClientConnection(self, clientSocket):
        nickName = (clientSocket.recv(2048)).decode()
        self.clientDict[nickName] = clientSocket
        print(nickName + ' is added to server dictionary')
        try:
            while True:
                data = clientSocket.recv(2048)
                if not data:
                    raise ConnectionError
                self.handleRequests(data)
        except ConnectionError:
            self.clientDict.pop(nickName)
            print(nickName + ' is removed from the server dictionary')
            clientSocket.close()

    def closeServer(self):
        print('Shutting down the server')
        self.socket.close()

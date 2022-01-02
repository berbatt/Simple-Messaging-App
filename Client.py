import socket
import threading
from MessageData import MessageData

class Client:

    def __init__(self, nickName, host, port):
        self.nickName = nickName
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def initializeClient(self):
        self.socket.connect((self.host, self.port))
        self.socket.send(str.encode(self.nickName))

    def sendListConnectedClientsMessage(self):
        message = MessageData(senderName=self.nickName, type='list')
        self.socket.send(message.serialize())

    def sendMessageToUser(self, receiverNickName, content):
        message = MessageData(senderName=self.nickName, receiverName=receiverNickName, content=content, type='message')
        self.socket.send(message.serialize())

    def queryFromServer(self):
        while True:
            query = input()
            if query == 'list':
                self.sendListConnectedClientsMessage()
            elif query == '':
                self.closeClientSocket()
                break
            else:
                queryAsList = list(query.split(' '))
                receiverNickName = queryAsList[0]
                content = ' '.join(queryAsList[1:])
                self.sendMessageToUser(receiverNickName, content)

    def handleServerConnection(self):
        senderThread = threading.Thread(target=self.handleServerSendOperations)
        receiverThread = threading.Thread(target=self.handleServerReceiveOperations)
        senderThread.start()
        receiverThread.start()
        senderThread.join()
        receiverThread.join()

    def handleServerSendOperations(self):
        try:
            self.queryFromServer()
        except ConnectionError:
            self.closeClientSocket()

    def handleServerReceiveOperations(self):
        try:
            while True:
                receivedMessage = self.socket.recv(2048)
                message = MessageData()
                message.deserialize(receivedMessage)
                print(message.toString())
        except ConnectionError:
            print('Client is closing')

    def closeClientSocket(self):
        print('Shutting down the client')
        self.socket.close()

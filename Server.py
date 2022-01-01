import socket
import sys
import threading


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
                print('Connected to: ' + clientAddress[0] + ':' + str(clientAddress[1]))
                clientThread = threading.Thread(target=self.handleClientConnection, args=(clientSocket, ))
                clientThread.start()
        except KeyboardInterrupt:
            self.closeServer()

    def handleListRequest(self, clientSocket):
        message = ' , '.join(self.clientDict.keys())
        print(message)
        clientSocket.send(str.encode(message))

    def handleRequests(self, data, clientSocket):
        message = data.decode()
        if message == 'list':
            self.handleListRequest(clientSocket)

    def handleClientConnection(self, clientSocket):
        nickName = (clientSocket.recv(1024)).decode()
        self.clientDict[nickName] = clientSocket
        print(nickName + ' is added to server dictionary')
        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            self.handleRequests(data, clientSocket)

        self.clientDict.pop(nickName)
        print(nickName + ' is removed from the server dictionary')
        clientSocket.close()

    def closeServer(self):
        print('Shutting down the server')
        self.socket.close()

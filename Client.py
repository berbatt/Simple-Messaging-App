import socket

class Client:

    def __init__(self, nickName, host, port):
        self.nickName = nickName
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def initializeClient(self):
        self.socket.connect((self.host, self.port))

    def handleListConnectedClientsMessage(self):
        message = 'list'
        self.socket.send(str.encode(message))
        connectedUsersList = self.socket.recv(1024)
        print(connectedUsersList.decode())

    def handleServerConnection(self):
        try:
            self.socket.send(str.encode(self.nickName))
            while True:
                query = input('Operations that you can do are: list \n')
                if query == 'list':
                    self.handleListConnectedClientsMessage()
                elif query == '':
                    self.closeClientSocket()
        except KeyboardInterrupt:
            self.closeClientSocket()

    def closeClientSocket(self):
        print('Shutting down the client')
        self.socket.close()

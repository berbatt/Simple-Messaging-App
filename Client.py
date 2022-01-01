import socket

class Client:

    def __init__(self, nickName, host, port):
        self.nickName = nickName
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def initializeClient(self):
        self.socket.connect((self.host, self.port))

    def handleServerConnection(self, message):
        initialResponse = self.socket.recv(1024)
        print(initialResponse.decode())
        sendMessage = self.nickName + ' ' + message
        self.socket.send(str.encode(sendMessage))
        while True:
            inputMessage = input('Write your message here \n')
            self.socket.send(str.encode(inputMessage))


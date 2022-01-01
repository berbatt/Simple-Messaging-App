import socket
import sys
import threading


class Server:

    def __init__(self, host, port, isOnline):
        self.host = host
        self.port = port
        self.isOnline = isOnline
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
                clientThread = threading.Thread(target=self.handleClientConnection, args=(clientSocket, clientAddress))
                clientThread.start()
        except KeyboardInterrupt:
            self.closeServer()

    def handleClientConnection(self, clientSocket, clientAddress):
        clientSocket.send(str.encode("Welcome to the server"))
        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(message)
        clientSocket.close()

    def closeServer(self):
        print('Shutting down the server')
        self.socket.close()

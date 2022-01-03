import socket
import threading
from MessageData import MessageData
from InputParser import InputParser

class Client:

    def __init__(self, nickName, host, port):
        self.nickName = nickName
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.inputParser = InputParser(self.nickName)

    def initializeClient(self):
        self.socket.connect((self.host, self.port))
        self.socket.send(str.encode(self.nickName))

    def sendMessageToServer(self, message):
        self.socket.send(message.serialize())

    def getInputAndQueryFromServer(self):
        self.inputParser.getInput()
        message = self.inputParser.generateMessage()
        if message is not None:
            self.sendMessageToServer(message)
        else:
            print('Please enter a valid input to client')
            print('Valid inputs are: list, target nickname <message>, get last <x>, ' +
                  'get contains <text>, get from-me or to-me')

    def handleServerConnection(self):
        senderThread = threading.Thread(target=self.handleServerSendOperations , daemon=True)
        receiverThread = threading.Thread(target=self.handleServerReceiveOperations, daemon=True)
        senderThread.start()
        receiverThread.start()
        senderThread.join()
        receiverThread.join()

    def handleServerSendOperations(self):
        try:
            while True:
                self.getInputAndQueryFromServer()
        except ConnectionError or KeyboardInterrupt:
            self.closeClientSocket()

    def handleServerReceiveOperations(self):
        try:
            while True:
                receivedMessage = self.socket.recv(2048)
                message = MessageData().deserialize(receivedMessage)
                print(message.toString())
        except ConnectionError or KeyboardInterrupt:
            print('Client is closing')

    def closeClientSocket(self):
        print('Shutting down the client')
        self.socket.close()

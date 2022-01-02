class MessageData:

    def __init__(self, senderName=' ', receiverName=' ', content=' ', type=' '):
        self.senderName = senderName
        self.receiverName = receiverName
        self.content = content
        self.type = type
        self.delimiter = '-/-'

    def getSenderName(self):
        return self.senderName

    def getReceiverName(self):
        return self.receiverName

    def getContent(self):
        return self.content

    def getType(self):
        return self.type

    def toString(self):
        return self.type + ' ' + self.senderName + ' ' + self.receiverName + ' ' + self.content

    def serialize(self):
        messageString = self.type + self.delimiter + self.senderName + self.delimiter + self.receiverName + self.delimiter + self.content
        return str.encode(messageString)

    def deserialize(self, messageByteArray):
        messageString = messageByteArray.decode()
        messageAsList = list(messageString.split(self.delimiter))
        self.type = messageAsList[0]
        self.senderName = messageAsList[1]
        self.receiverName = messageAsList[2]
        self.content = ''.join(messageAsList[3:])
        return self

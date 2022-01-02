from FilterType import FilterType

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
        result = ''
        if self.type == 'list':
            result = 'Connected users are: ' + self.content
        elif self.type == 'message':
            result = 'Message from ' + self.senderName + ' : ' + self.content
        else:
            result = self.content
        return result

    def serialize(self):
        typeString = self.type if isinstance(self.type, str) else self.type.toString()
        messageString = typeString + self.delimiter + self.senderName + self.delimiter + self.receiverName + self.delimiter + self.content
        return str.encode(messageString)

    def deserialize(self, messageByteArray):
        messageString = messageByteArray.decode()
        messageAsList = list(messageString.split(self.delimiter))
        typeString = messageAsList[0]
        self.type = typeString if (typeString == 'list' or typeString == 'message' or typeString == 'response') else FilterType().fromString(typeString)
        self.senderName = messageAsList[1]
        self.receiverName = messageAsList[2]
        self.content = ''.join(messageAsList[3:])
        return self

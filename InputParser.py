from MessageData import MessageData


class InputParser:
    def __init__(self, nickName):
        self.nickName = nickName
        self.text = ''

    def getInput(self):
        self.text = input()

    def generateMessage(self):
        generatedMessage = MessageData()
        textAsList = list(self.text.split(' '))
        if '' in textAsList:
            generatedMessage = None
        else:
            if 'list' in textAsList:
                generatedMessage = MessageData(senderName=self.nickName, type='list')
            elif 'get' in textAsList:
                pass
            else:
                generatedMessage = MessageData(senderName=self.nickName, receiverName=textAsList[0],
                                               content=' '.join(textAsList[1:]), type='message')
        return generatedMessage

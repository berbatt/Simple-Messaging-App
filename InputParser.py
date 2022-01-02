from MessageData import MessageData
from FilterType import FilterType

def handleGetFilterFromInput(inputList):
    filterType = FilterType()
    filterIndex = 0
    while filterIndex < len(inputList):
        if inputList[filterIndex] == 'get':
            pass
        elif inputList[filterIndex] == 'last':
            filterIndex += 1
            filterType.setLast(int(inputList[filterIndex]))
        elif inputList[filterIndex] == 'contains':
            filterIndex += 1
            filterType.setContainsText(inputList[filterIndex])
        elif inputList[filterIndex] == 'from-me' or inputList[filterIndex] == 'to-me':
            filterType.setDirection(inputList[filterIndex])
        filterIndex += 1
    return filterType

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
            if textAsList[0] == 'list':
                generatedMessage = MessageData(senderName=self.nickName, type='list')
            elif textAsList[0] == 'get':
                filterType = handleGetFilterFromInput(textAsList)
                generatedMessage = MessageData(senderName=self.nickName, type=filterType)
            else:
                generatedMessage = MessageData(senderName=self.nickName, receiverName=textAsList[0],
                                               content=' '.join(textAsList[1:]), type='message')
        return generatedMessage

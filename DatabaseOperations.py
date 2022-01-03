from peewee import *
from MessageData import MessageData
import datetime

db = SqliteDatabase('messages.db')


class MessageModel(Model):
    senderName = CharField()
    receiverName = CharField()
    messageBody = TextField()
    creationDate = DateTimeField()

    class Meta:
        database = db


MessageModel.create_table()


def addMessage(message):
    entry = MessageModel.create(senderName=message.getSenderName(),
                                receiverName=message.getReceiverName(),
                                messageBody=message.getContent(),
                                creationDate=datetime.datetime.now())


def queryResultToList(queryResult):
    result = list()
    for row in queryResult:
        result.append(row.messageBody)
    return result

def filterMessagesOfTheUser(queryResult, nickName, direction):
    result = list()
    for row in queryResult:
        if direction == 'both' or direction == '':
            if row.senderName == nickName or row.receiverName == nickName:
                result.append(row.messageBody)
        elif direction == 'to-me':
            if row.receiverName == nickName:
                result.append(row.messageBody)
        elif direction == 'from-me':
            if row.senderName == nickName:
                result.append(row.messageBody)
    return result

def getMessageBySenderName(senderName):
    sendByMe = MessageModel.select().order_by(MessageModel.creationDate.desc()).where(MessageModel.senderName == senderName)
    return queryResultToList(sendByMe)


def getMessageByReceiverName(receiverName):
    sendToMe = MessageModel.select().order_by(MessageModel.creationDate.desc()).where(MessageModel.receiverName == receiverName)
    return queryResultToList(sendToMe)


def getMessageByContainingText(text, nickName, direction):
    containsText = MessageModel.select().order_by(MessageModel.creationDate.desc()).where(MessageModel.messageBody.contains(text))
    return filterMessagesOfTheUser(containsText, nickName, direction)

def getMessagesOfTheUser(nickName):
    messagesOfTheUser = MessageModel.select().order_by(MessageModel.creationDate.desc()).where((MessageModel.senderName == nickName) |
                                                                                               (MessageModel.receiverName == nickName))
    return queryResultToList(messagesOfTheUser)

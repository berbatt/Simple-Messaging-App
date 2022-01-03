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


def getMessageBySenderName(senderName):
    result = list()
    sendByMe = MessageModel.select().where(MessageModel.senderName == senderName)
    for row in sendByMe:
        result.append(row.messageBody)
    return result

def getMessageByReceiverName(receiverName):
    result = list()
    sendToMe = MessageModel.select().where(MessageModel.receiverName == receiverName)
    for row in sendToMe:
        result.append(row.messageBody)
    return result

def getMessageByContainingText(text):
    result = list()
    containsText = MessageModel.select().where(MessageModel.messageBody.contains(text))
    for row in containsText:
        result.append(row.messageBody)
    return result

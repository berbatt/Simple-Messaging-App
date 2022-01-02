class FilterType:

    def __init__(self, last=0, containsText='', direction=''):
        self.last = last
        self.containsText = containsText
        self.direction = direction
        self.delimiter = '***'

    def setLast(self, last):
        self.last = last

    def setContainsText(self, text):
        self.containsText = text

    def setDirection(self, direction):
        self.direction = direction

    def getLast(self):
        return self.last

    def getContainsText(self):
        return self.containsText

    def getDirection(self):
        return self.direction

    def toString(self):
        return str(self.last) + self.delimiter + self.containsText + self.delimiter + self.direction

    def fromString(self, typeString):
        typeAsList = list(typeString.split(self.delimiter))
        self.last = int(typeAsList[0])
        self.containsText = typeAsList[1]
        self.direction = typeAsList[2]
        return self

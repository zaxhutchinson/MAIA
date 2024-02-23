class Action:
    def __init__(self):
        self.type = None
        self.data = {}

    def setType(self, typ):
        self.type = typ

    def getType(self):
        return self.type

    def setData(self, data):
        self.data = data

    def addData(self, key, value):
        self.data[key] = value

    def getData(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

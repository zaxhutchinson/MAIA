class Item:
    def __init__(self, data):
        self.data = data
        self.data["x"] = None
        self.data["y"] = None
        self.data["owner"] = None

    def getData(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def setData(self, key, value):
        self.data[key] = value

    def place(self, data):
        for k, v in data.items():
            self.data[k] = v

    def getDrawData(self):
        return {
            "uuid": self.getData("uuid"),
            "x": self.getData("x"),
            "y": self.getData("y"),
            "text": self.getData("text"),
            "fill": self.getData("fill"),
        }

    def takeItem(self, owner_uuid):
        self.data["owner"] = owner_uuid

    def dropItem(self):
        self.data["owner"] = None

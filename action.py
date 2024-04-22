class Action:
    def __init__(self):
        """Sets action type and data to default"""
        self.type = None
        self.data = {}

    def set_type(self, typ):
        """Sets type"""
        self.type = typ

    def get_type(self):
        """Gets type"""
        return self.type

    def set_data(self, data):
        """Sets data

        Replaced currently stored data
        """
        self.data = data

    def add_data(self, key, value):
        """Add key and value of data

        Adds to currently stored data
        """
        self.data[key] = value

    def get_data(self, key):
        """Gets data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

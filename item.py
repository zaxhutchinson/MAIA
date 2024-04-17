class Item:
    def __init__(self, data):
        """Initializes item data"""
        self.data = data
        self.data["x"] = None
        self.data["y"] = None
        self.data["owner"] = None

    def get_data(self, key):
        """Get data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set_data(self, key, value):
        """Set data"""
        self.data[key] = value

    def place(self, data):
        """Set all key/value pairs"""
        for k, v in data.items():
            self.data[k] = v

    def get_draw_data(self):
        """Get draw data"""
        return {
            "uuid": self.get_data("uuid"),
            "x": self.get_data("x"),
            "y": self.get_data("y"),
            "text": self.get_data("text"),
            "fill": self.get_data("fill"),
            "name": self.get_data("name"),
            "sprite_path": self.get_data("sprite_path"),
        }

    def take_item(self, owner_uuid):
        """Assigns owner that has taken item"""
        self.data["owner"] = owner_uuid

    def drop_item(self):
        """De-assigns owner that has dropped item"""
        self.data["owner"] = None

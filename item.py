

class Item:
    def __init__(self, unique_id, template):
        """Initializes item data"""
        self.uuid = unique_id
        self.id = template["id"]
        self.name = template["name"]
        self.sprite_filename = template["sprite_filename"]
        self.bulk = template["bulk"]
        self.weight = template["weight"]
        self.x = 0.0
        self.y = 0.0
        self.owner = None
        self.redraw = True

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.uuid == other.uuid
        else:
            return False

    def init_for_sim(self, **kwargs):
        self.x = kwargs["x"] + 0.5
        self.y = kwargs["y"] + 0.5
        self.owner = None

    def get_uuid(self):
        return self.uuid

    def get_template_id(self):
        return self.id

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_cell_x(self):
        return int(self.x)

    def get_cell_y(self):
        return int(self.y)

    def get_within_cell_x(self):
        return self.x - int(self.x)

    def get_within_cell_y(self):
        return self.y - int(self.y)

    def get_name(self):
        return self.name

    def get_sprite_filename(self):
        return self.sprite_filename

    def get_draw_data(self):
        """Get draw data"""
        return {
            "uuid": self.uuid,
            "x": self.get_cell_x(),
            "y": self.get_cell_y(),
            "name": self.name,
            "redraw": self.redraw,
            "sprite_filename": self.sprite_filename,
            "sprite_type": "item"
        }

    def take_item(self, owner):
        """Assigns owner that has taken item"""
        self.owner = owner

    def drop_item(self):
        """De-assigns owner that has dropped item"""
        self.owner = None

    def get_redraw(self):
        return self.redraw

    def set_redraw(self, redraw):
        self.redraw = redraw

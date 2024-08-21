TRIGGER_TYPES = [
    "OBJECT_AT_ITEM",
    "ITEM_AT_ITEM"
]


class Trigger:
    def __init__(self, template):
        self.type = template["type"]
        self.name = template["name"]
        self.points = template["points"]
        self.active = True
        self.init = None
        self.check = None
        self.item_ids = template["item_ids"]
        self.items = []

        match self.type:
            case "OBJECT_AT_ITEM":
                self.init = self.init_object_at_item
                self.check = self.check_object_at_item
            case "ITEM_AT_ITEM":
                self.init = self.init_item_at_item
                self.check = self.check_item_at_item

    def get_name(self):
        return self.name

    def init_object_at_item(self, items):
        for i in items:
            if i.get_template_id() in self.item_ids:
                self.items.append(i)

    def check_object_at_item(self, objects: dict):
        if self.active:
            for _uuid, o in objects.items():
                ox = o.get_cell_x()
                oy = o.get_cell_y()
                for i in self.items:
                    ix = i.get_cell_x()
                    iy = i.get_cell_y()
                    if ix == ox and iy == oy:
                        self.active = False
                        return o, self.points
        return None, 0

    def init_item_at_item(self, items):
        for i in items:
            if i.get_template_id() in self.item_ids:
                self.items.append(i)

    def check_item_at_item(self, objects):
        if self.active:
            for a in self.items:
                ax = a.get_cell_x()
                ay = a.get_cell_y()
                for b in self.items:
                    if a == b:
                        continue
                    bx = b.get_cell_x()
                    by = b.get_cell_y()
                    if ax == bx and ay == by:
                        self.active = False
                        for o in objects:
                            if o.get_cell_x() == ax and o.get_cell_y() == ay:
                                return o, self.points
        return None, 0

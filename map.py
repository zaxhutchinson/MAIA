import zmath


class Map:
    def __init__(self, template):
        self.width = template["width"]
        self.height = template["height"]
        self.object_grid = []
        self.item_grid = []
        self.edge_obj_id = template["edge_obj_id"]
        self.triggers = []
        self.build_map_grid()
        self.build_triggers(template)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_edge_obj_id(self):
        return self.edge_obj_id

    def build_triggers(self, map_template):
        pass

    def build_map_grid(self):
        """Generates map grid
        """
        for x in range(self.width):
            obj_new_col = []
            item_new_col = []
            for y in range(self.height):
                obj_new_col.append(None)
                item_new_col.append([])
            self.object_grid.append(obj_new_col)
            self.item_grid.append(item_new_col)

    def get_object_at(self, x, y):
        obj_uuid = self.object_grid[x][y]
        if obj_uuid is not None:
            return self.objects[obj_uuid]
        else:
            return None

    def add_object_to(self, x, y, obj_uuid):
        """Adds object"""
        if self.object_grid[x][y] is None:
            self.object_grid[x][y] = obj_uuid
            return True
        return False

    def remove_object_from(self, x, y, obj_uuid):
        """Removes object"""
        if self.object_grid[x][y] == obj_uuid:
            self.object_grid[x][y] = None
            return True
        return False

    def add_item_to(self, x, y, item_uuid):
        """Adds item"""
        if item_uuid not in self.item_grid[x][y]:
            self.item_grid[x][y].append(item_uuid)
            return True
        return False

    def remove_item_from(self, x, y, item_uuid):
        """Removes item"""
        if item_uuid in self.item_grid[x][y]:
            self.item_grid[x][y].remove(item_uuid)
            return True
        return False

    def get_items_at(self, x, y):
        """Gets items in a cell"""
        return self.item_grid[x][y]

    def contains_object(self, x, y):
        """Determines if a cell is empty"""
        return self.object_grid[x][y] is not None

    def contains_items(self, x, y):
        return len(self.item_grid[x][y]) == 0

    def move_obj_from_to(self, obj_uuid, from_x, from_y, to_x, to_y):
        """Moves object from one cell to another"""
        if self.contains_object(from_x, from_y):
            if self.remove_item_from(from_x, from_y, obj_uuid):
                return self.add_object_to(to_x, to_y, obj_uuid)
        return False

    def get_all_objs_along_trajectory(self, x, y, angle, distance):
        """Gets all object uuid's along a trajectory given a start point,
        angle and distance"""
        found = {}
        found["objects"] = []
        found["items"] = []

        # Get the cells
        cells = zmath.get_cells_along_trajectory(x, y, angle, distance)

        # So long as we're in the map,
        # If the obj or item grid cell is not None
        # create a ping and save it.
        for cell in cells:
            if 0 <= cell[0] < self.width and 0 <= cell[1] < self.height:
                if self.contains_object(cell[0], cell[1]):
                    ping = {}
                    ping["x"] = cell[0]
                    ping["y"] = cell[1]
                    ping["distance"] = zmath.distance(x, y, cell[0], cell[1])
                    ping["object"] = self.get_object_at(cell[0], cell[1])
                    ping["type"] = "object"
                    found["objects"].append(ping)
                if self.contains_items(cell[0], cell[1]):
                    for i in self.get_items_at(cell[0], cell[1]):
                        ping = {}
                        ping["x"] = cell[0]
                        ping["y"] = cell[1]
                        ping["distance"] = zmath.distance(
                            x, y, cell[0], cell[1]
                        )
                        ping["items"] = i
                        ping["type"] = "item"
                        found["items"].append(ping)

            else:
                break

        return found

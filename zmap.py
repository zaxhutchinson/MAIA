import random

import loader
import obj
import vec2
import log
import zmath


class Map:
    def __init__(self, data):
        self.data = data

    def set_data(self, key, val):
        """Sets data"""
        self.data[key] = val

    def get_data(self, key):
        """Gets data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def build_map_grid(self):
        """Generates map grid

        Build the map 2 hexes wider and taller. This allows for
        the placing of blocks around the edge while still keeping
        the same playable space outlined in the map json. And
        it means we do not have to worry about accounting for edge
        boundries as they cannot be reached (if the edge obj is indestructible).
        """
        obj_grid = []
        item_grid = []
        for x in range(self.data["width"] + 2):
            obj_new_col = []
            item_new_col = []
            for y in range(self.data["height"] + 2):
                obj_new_col.append(None)
                item_new_col.append([])
            obj_grid.append(obj_new_col)
            item_grid.append(item_new_col)

        self.data["obj_grid"] = obj_grid
        self.data["item_grid"] = item_grid

    def add_obj(self, x, y, _uuid):
        """Adds object"""
        self.data["obj_grid"][x][y] = _uuid

    def remove_obj(self, x, y, _uuid):
        """Removes object"""
        if self.data["obj_grid"][x][y] == _uuid:
            self.data["obj_grid"][x][y] = None

    def add_item(self, x, y, _uuid):
        """Adds item"""
        if _uuid not in self.data["item_grid"][x][y]:
            self.data["item_grid"][x][y].append(_uuid)

    def remove_item(self, x, y, _uuid):
        """Removes item"""
        if _uuid in self.data["item_grid"][x][y]:
            self.data["item_grid"][x][y].remove(_uuid)

    def get_items_in_cell(self, x, y):
        """Gets items in a cell"""
        return self.data["item_grid"][x][y]

    # Creates a list of the coordinates of the world edge.
    def get_list_of_edge_coordinates(self):
        """Gets list of edge coordinates"""
        edge_coords = []
        wide = self.data["width"]
        high = self.data["height"]
        for x in range(wide):
            edge_coords.append((x, 0))
            edge_coords.append((x, high - 1))
        for y in range(1, high - 1):
            edge_coords.append((0, y))
            edge_coords.append((wide - 1, y))
        return edge_coords

    def is_cell_empty(self, x, y):
        """Determines if a cell is empty"""
        return self.get_data("obj_grid")[x][y] is None

    def get_cell_occupant(self, x, y):
        """Gets cell occupant"""
        return self.get_data("obj_grid")[x][y]

    def move_obj_from_to(self, objuuid, from_x, from_y, to_x, to_y):
        """Moves object from one cell to another"""
        grid = self.get_data("obj_grid")
        if grid[from_x][from_y] == objuuid:
            grid[from_x][from_y] = None
            grid[to_x][to_y] = objuuid

    def get_all_obj_uuid_along_trajectory(self, x, y, angle, distance):
        """Gets all object uuid's along a trajectory given angle and distance"""
        found = {}
        found["objects"] = []
        found["items"] = []

        # Get refs to the two grids
        obj_grid = self.get_data("obj_grid")
        item_grid = self.get_data("item_grid")

        # Get the cells
        cells = zmath.get_cells_along_trajectory(x, y, angle, distance)

        # So long as we're in the map,
        # If the obj or item grid cell is not None
        # create a ping and save it.
        for cell in cells:
            if 0 <= cell[0] < self.get_data("width") and 0 <= cell[1] < self.get_data(
                "height"
            ):
                if obj_grid[cell[0]][cell[1]] is not None:
                    _uuid = obj_grid[cell[0]][cell[1]]
                    ping = {}
                    ping["x"] = cell[0]
                    ping["y"] = cell[1]
                    ping["distance"] = zmath.distance(x, y, cell[0], cell[1])
                    ping["uuid"] = _uuid
                    ping["type"] = "object"
                    found["objects"].append(ping)
                if len(item_grid[cell[0]][cell[1]]) > 0:
                    for i in item_grid[cell[0]][cell[1]]:
                        ping = {}
                        ping["x"] = cell[0]
                        ping["y"] = cell[1]
                        ping["distance"] = zmath.distance(x, y, cell[0], cell[1])
                        ping["uuid"] = i
                        ping["type"] = "item"
                        found["items"].append(ping)

            else:
                break

        return found

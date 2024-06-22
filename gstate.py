# gstate.py
# Global State
# By ZSH
# Created 9-1-2020

# Provides a global repository for state information.

GSTATE_TYPES = [
    "ITEMS_TOUCH",
    "OBJ_ITEMS_TOUCH",
    "N_OBJS_DESTROYED",
    "N_OBJS_IN_LOCS"
]

GOAL_ATTRS_BY_TYPE = {
    "ITEMS_TOUCH": [("items", [])],
    "OBJ_ITEMS_TOUCH": [("items", []), ("object", "")],
    "N_OBJS_DESTROYED": [("amount", 0), ("objects", [])],
    "N_OBJS_IN_LOCS": [("amount", 0), ("objects", []), ("locations", [])],
}


class GState:
    def __init__(self, data):
        """Initializes gstate data

        Sets data to input
        Sets check_state and init_state based on end-state type
        """
        self.data = data
        self.items = []
        self.objs = []

        self.init_state = None
        self.check_state = None

        if self.data["type"] == "N_OBJS_IN_LOCS":
            self.check_state = self.check_n_objs_in_locs
            self.init_state = self.init_n_objs_in_locs
        elif self.data["type"] == "OBJ_ITEMS_TOUCH":
            self.check_state = self.check_obj_items_touch
            self.init_state = self.init_obj_items_touch
        elif self.data["type"] == "ITEMS_TOUCH":
            self.check_state = self.check_item_touch
            self.init_state = self.init_item_touch
        elif self.data["type"] == "N_OBJS_DESTROYED":
            self.check_state = self.check_n_objs_destroyed
            self.init_state = self.init_n_objs_destroyed

    def get_data(self, key):
        """Gets data"""
        return self.data[key]

    ############################################################
    # N_OBJS_IN_LOCS
    #   This gstate tracks if a specific amount of objects have
    #   reached a set of locations.
    #
    #   A simple scenario is 1 obj and 1 location: i.e., maze.
    #
    #   Fox-hound scenarios where 1 obj is trying to reach
    #   one of multiple safe locations and several "foxes"
    #   are trying to destroy it.
    #
    #   But it also supports teams or parts of teams, multiple
    #   locations.
    def init_n_objs_in_locs(self, objs, items):
        """Initializes data for object in a cell

        N of the objects must be in one of the specified cells.
        """

        # Don't need to store items...irrelevant

        for o in objs.values():
            if o.get_data("id") in self.data["objects"]:
                self.objs.append(o)

    def check_n_objs_in_locs(self):
        amt = self.data["amount"]

        # First check if N objects are still alive.
        # Prevents impossible states in which combat is allowed
        #   and too many objects are destroyed.
        num_alive = 0
        for o in self.objs:
            if o.get_data("alive"):
                num_alive += 1
        if num_alive < amt:
            return False

        # Now check if enough objects have reached the dest cells
        locations = self.data["locations"]
        for o in self.objs:
            for loc in locations:
                if loc == f"{o.get_data('x')},{o.get_data('y')}":
                    amt -= 1
                    break

            if amt <= 0:
                return True

        return False

    ############################################################
    # OBJ_ITEM_TOUCH

    def init_obj_items_touch(self, objs, items):
        """Initializes data for object-items-touch end-state

        One of the objects must touch all items simultaneously.
        """
        for i in items.values():
            if i.get_data("id") in self.data["items"]:
                self.items.append(i)
        for o in objs.values():
            if o.get_data("id") in self.data["objects"]:
                self.objs.append(o)

    def check_obj_items_touch(self):
        """Check if object-item-touch condition has been met"""
        # First see if all items are in the same location
        loc = None
        all_touching = True
        for i in self.items:
            if loc is None:
                loc = (i.get_data("x"), i.get_data("y"))
            else:
                cur_loc = (i.get_data("x"), i.get_data("y"))
                all_touching = loc == cur_loc

            # Something isn't in the same location, stop.
            if not all_touching:
                break

        # If all items are in the same place...
        if all_touching:

            # If the obj is, set state to true
            for o in self.objs:
                if loc == (o.get_data("x"), o.get_data("y")):
                    return True

        return False

    ############################################################
    # ITEM TOUCH
    def init_item_touch(self, objs, items):
        """Initializes data for item-touch end-state"""
        for i in items.values():
            if i.get_data("id") in self.data["items"]:
                self.items.append(i)

    def check_item_touch(self):
        """Checks if item-touch condition has been met"""
        loc = None
        all_touching = True

        for i in self.items:

            if loc is None:
                loc = (i.get_data("x"), i.get_data("y"))
            else:
                cur_loc = (i.get_data("x"), i.get_data("y"))
                all_touching = loc == cur_loc

            # Something isn't in the same location, stop.
            if not all_touching:
                break

        return all_touching

    # ############################################################
    # # ALL OBJS DESTROYED
    # def init_all_objs_destroyed(self, objs, items):
    #     """Initializes data for all-objects-destroyed end-state"""
    #     for o in objs.values():
    #         if o.get_data("name") in self.data["objs"]:
    #             self.objs.append(o)

    # def check_all_objs_destroyed(self):
    #     """Checks if all-objects-destroyed condition has been met"""

    #     # If we find one alive, return False
    #     for o in self.objs:
    #         if o.get_data("alive"):
    #             return False

    #     return True

    ############################################################
    # N OBJS DESTROYED
    def init_n_objs_destroyed(self, objs, items):
        """Initializes data for n-objects-destroyed end-state"""
        for o in objs.values():
            if o.get_data("id") in self.data["objects"]:
                self.objs.append(o)

    def check_n_objs_destroyed(self):
        """Checks if n-objects-destroyed condition has been met"""
        num_dead = 0

        for o in self.objs:
            if not o.get_data("alive"):
                num_dead += 1

        # Int cast just in case someone adds as string
        return num_dead >= int(self.data["amount"])

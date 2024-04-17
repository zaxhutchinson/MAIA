# gstate.py
# Global State
# By ZSH
# Created 9-1-2020

# Provides a global repository for state information.


class GState:
    def __init__(self, data):
        """Initialize gstate data

        Sets data to input
        Sets check_state and init_state based on end-state type
        """
        self.data = data
        self.items = []
        self.objs = []

        self.init_state = None
        self.check_state = None

        if self.data["type"] == "OBJ_ITEMS_TOUCH":
            self.check_state = self.check_obj_items_touch
            self.init_state = self.init_obj_items_touch
        elif self.data["type"] == "ITEMS_TOUCH":
            self.check_state = self.check_item_touch
            self.init_state = self.init_item_touch
        elif self.data["type"] == "ALL_OBJS_DESTROYED":
            self.check_state = self.check_all_objs_destroyed
            self.init_state = self.init_all_objs_destroyed
        elif self.data["type"] == "N_OBJS_DESTROYED":
            self.check_state = self.check_n_objs_destroyed
            self.init_state = self.init_n_objs_destroyed

    def get_data(self, key):
        """Gets data"""
        return self.data[key]

    ############################################################
    # OBJ_ITEM_TOUCH

    def init_obj_items_touch(self, objs, items):
        """Initializes data for object-items-touch end-state

        One of the objects must touch all items simultaneously.
        """
        for i in items.values():
            if i.get_data("name") in self.data["items"]:
                self.items.append(i)
        for o in objs.values():
            if o.get_data("name") in self.data["objs"]:
                self.objs.append(o)

    def check_obj_items_touch(self):
        """Check if object-item-touch condition has been met"""
        # First see if all items are in the same location
        prev_x = None
        prev_y = None
        state_x = True
        state_y = True
        for i in self.items:
            if prev_x is None:
                prev_x = i.get_data("x")
                prev_y = i.get_data("y")
            else:
                state_x = state_x and prev_x == i.get_data("x")
                state_y = state_y and prev_y == i.get_data("y")

        # If all items are in the same place...
        if state_x and state_y:
            # Assume obj is not...
            self.data["state"] = False
            # If 1 obj is, set state to true
            for o in self.objs:
                if prev_x == o.get_data("x") and prev_y == o.get_data("y"):
                    self.data["state"] = True
        else:
            self.data["state"] = False

        return self.data["state"]

    ############################################################
    # ITEM TOUCH
    def init_item_touch(self, objs, items):
        """Initializes data for item-touch end-state"""
        for i in items.values():
            if i.get_data("name") in self.data["items"]:
                self.items.append(i)

    def check_item_touch(self):
        """Checks if item-touch condition has been met"""
        prev_x = None
        prev_y = None

        state_x = True
        state_y = True

        for i in self.items:

            if prev_x is None:
                prev_x = i.get_data("x")
                prev_y = i.get_data("y")
            else:
                state_x = state_x and prev_x == i.get_data("x")
                state_y = state_y and prev_y == i.get_data("y")

        self.data["state"] = state_x and state_y

        return self.data["state"]

    ############################################################
    # ALL OBJS DESTROYED
    def init_all_objs_destroyed(self, objs, items):
        """Initializes data for all-objects-destroyed end-state"""
        for o in objs.values():
            if o.get_data("name") in self.data["objs"]:
                self.objs.append(o)

    def check_all_objs_destroyed(self):
        """Checks if all-objects-destroyed condition has been met"""
        all_dead = True

        for o in self.objs:
            all_dead = all_dead and not o.get_data("alive")

        self.data["state"] = all_dead

        return all_dead

    ############################################################
    # N OBJS DESTROYED
    def init_n_objs_destroyed(self, objs, items):
        """Initializes data for n-objects-destroyed end-state"""
        for o in objs.values():
            if o.get_data("name") in self.data["objs"]:
                self.objs.append(o)

    def check_n_objs_destroyed(self):
        """Checks if n-objects-destroyed condition has been met"""
        num_dead = 0

        for o in self.objs:
            if not o.get_data("alive"):
                num_dead += 1

        # Int cast just in case someone adds as string
        self.data["state"] = num_dead >= int(self.data["number"])

        return self.data["state"]

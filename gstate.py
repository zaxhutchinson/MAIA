# gstate.py
# Global State
# By ZSH
# Created 9-1-2020

# Provides a global repository for state information.


class GState:
    def __init__(self, data):
        self.data = data
        self.items = []
        self.objs = []

        self.initState = None
        self.checkState = None

        if self.data["type"] == "OBJ_ITEMS_TOUCH":
            self.checkState = self.checkObjItemsTouch
            self.initState = self.initObjItemsTouch
        elif self.data["type"] == "ITEMS_TOUCH":
            self.checkState = self.checkItemTouch
            self.initState = self.initItemTouch
        elif self.data["type"] == "ALL_OBJS_DESTROYED":
            self.checkState = self.checkAllObjsDestroyed
            self.initState = self.initAllObjsDestroyed
        elif self.data["type"] == "N_OBJS_DESTROYED":
            self.checkState = self.checkNObjsDestroyed
            self.initState = self.initNObjsDestroyed

    def getData(self, key):
        return self.data[key]

    ############################################################
    # OBJ_ITEM_TOUCH
    # One of the objects must touch all items simultaneously.

    def initObjItemsTouch(self, objs, items):
        for i in items.values():
            if i.getData("name") in self.data["items"]:
                self.items.append(i)
        for o in objs.values():
            if o.getData("name") in self.data["objs"]:
                self.objs.append(o)

    def checkObjItemsTouch(self):
        # First see if all items are in the same location
        prev_x = None
        prev_y = None
        state_x = True
        state_y = True
        for i in self.items:
            if prev_x is None:
                prev_x = i.getData("x")
                prev_y = i.getData("y")
            else:
                state_x = state_x and prev_x == i.getData("x")
                state_y = state_y and prev_y == i.getData("y")

        # If all items are in the same place...
        if state_x and state_y:
            # Assume obj is not...
            self.data["state"] = False
            # If 1 obj is, set state to true
            for o in self.objs:
                if prev_x == o.getData("x") and prev_y == o.getData("y"):
                    self.data["state"] = True
        else:
            self.data["state"] = False

        return self.data["state"]

    ############################################################
    # ITEM TOUCH
    def initItemTouch(self, objs, items):
        for i in items.values():
            if i.getData("name") in self.data["items"]:
                self.items.append(i)

    def checkItemTouch(self):

        prev_x = None
        prev_y = None

        xstate = True
        ystate = True

        for i in self.items:

            if prev_x is None:
                prev_x = i.getData("x")
                prev_y = i.getData("y")
            else:
                xstate = xstate and prev_x == i.getData("x")
                ystate = ystate and prev_y == i.getData("y")

        self.data["state"] = xstate and ystate

        return self.data["state"]

    ############################################################
    # ALL OBJS DESTROYED
    def initAllObjsDestroyed(self, objs, items):
        for o in objs.values():
            if o.getData("name") in self.data["objs"]:
                self.objs.append(o)

    def checkAllObjsDestroyed(self):

        all_dead = True

        for o in self.objs:
            all_dead = all_dead and not o.getData("alive")

        self.data["state"] = all_dead

        return all_dead

    ############################################################
    # N OBJS DESTROYED
    def initNObjsDestroyed(self, objs, items):
        for o in objs.values():
            if o.getData("name") in self.data["objs"]:
                self.objs.append(o)

    def checkNObjsDestroyed(self):

        num_dead = 0

        for o in self.objs:
            if not o.getData("alive"):
                num_dead += 1

        # Int cast just in case someone adds as string
        self.data["state"] = num_dead >= int(self.data["number"])

        return self.data["state"]

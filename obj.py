import random
import math
import logging

import vec2
import line
import zfunctions

_2PI = 2.0 * math.pi


class Object:
    def __init__(self, data):
        self.data = data
        self.JSON_keys = list(self.data.keys())
        self.data["damage"] = 0.0
        self.data["facing"] = 0.0
        self.data["x"] = None
        self.data["y"] = None
        self.data["cell_x"] = 0.5
        self.data["cell_y"] = 0.5
        self.data["comps"] = {}
        self.data["uuid"] = None
        self.data["ai"] = None
        self.data["alive"] = True
        self.data["teamname"] = None
        self.data["callsign"] = None
        self.data["squad"] = None
        self.data["redraw"] = True
        self.data["points"] = 0

        self.logger = None

        self.view_keys = [
            "health",
            "damage",
            "facing",
            "x",
            "y",
            "cell_x",
            "cell_y",
            "name",
            "teamname",
            "callsign",
            "squad",
        ]

    def getData(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def setData(self, key, val):
        self.data[key] = val
        self.data["redraw"] = True

    def isAlive(self):
        return self.getData("alive")

    def addComp(self, comp):
        next_id = str(len(self.data["comps"]))
        comp.setData("slot_id", next_id)
        self.data["comps"][next_id] = comp

    def getComp(self, slot_id):
        if slot_id in self.getData("comps"):
            return self.getData("comps")[slot_id]
        else:
            return None

    def place(self, data):
        for k, v in data.items():
            self.data[k] = v
        self.initLogger()

    def initLogger(self):
        if self.getData("ai") is not None:
            self.logger = logging.getLogger(
                self.getData("teamname") + "." + self.getData("callsign")
            )
            self.logger.setLevel(logging.DEBUG)
            self.handler = logging.FileHandler(
                "log/" + self.logger.name + ".log", mode="w"
            )
            self.formatter = logging.Formatter("%(name)s - %(message)s")
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)

    # Obj-level pass through functions to the logger
    def logDebug(self, msg):
        if self.logger is not None:
            self.logger.debug(msg)

    def logInfo(self, msg):
        if self.logger is not None:
            self.logger.info(msg)

    def logWarning(self, msg):
        if self.logger is not None:
            self.logger.warning(msg)

    def logError(self, msg):
        if self.logger is not None:
            self.logger.error(msg)

    def logCritical(self, msg):
        if self.logger is not None:
            self.logger.critical(msg)

    def update(self, view):
        if self.isAlive():
            try:
                if self.data["ai"] is not None:
                    view["self"] = self.getSelfView()
                    return self.data["ai"].runAI(view)
                else:
                    return None
            except Exception as e:
                self.logError("runAI() raised an exception: " + str(e))
                # log.LogMostRecentException(
                #     "AI script for team "+
                #     self.getData('teamname') +
                #     " agent " + self.getData('callsign') +
                #     " raised the exception: " + str(e)

                # )

    def damageObj(self, amt):
        # Add damage to current total
        old_damage = self.getData("damage")
        new_damage = old_damage + amt
        self.setData("damage", new_damage)

        self.logInfo("Damaged for " + str(amt) + " - Total Damage: " + str(new_damage))

        points = 0
        if self.getData("points_count"):
            points = amt

        # If it's still alive and damage is greater than health,
        # OBJECT IS DESTROYED.
        if self.isAlive() and new_damage >= self.getData("health"):
            self.setData("alive", False)

            self.logInfo("DESTROYED!!!")

            points = self.getData("health") - old_damage

        return points

    def getDrawData(self):
        fill = self.getData("fill_alive")
        if not self.isAlive():
            fill = self.getData("fill_dead")
        redraw = self.getData("redraw")
        self.data["redraw"] = False
        return {
            "uuid": self.getData("uuid"),
            "x": self.getData("x"),
            "y": self.getData("y"),
            "alive": self.isAlive(),
            "text": self.getData("text"),
            "fill": fill,
            "redraw": redraw,
        }

    def processCommands(self, cmds):
        actions = []
        if self.isAlive():

            # Find number of commands that can be ordered.
            max_cmds = 0
            for comp in self.getData("comps").values():
                if comp.getData("ctype") == "CnC":
                    max_cmds += comp.getData("max_cmds_per_tick")

            for slot_id, cmd in cmds.items():

                # Check and reduce commands remaining
                # Having this outside the if-statment below
                # means that even badly formed commands count.
                if max_cmds == 0:
                    break
                else:
                    max_cmds -= 1

                if slot_id in self.data["comps"]:
                    actions += self.data["comps"][slot_id].Command(cmd)
                    self.logInfo(zfunctions.CmdToString(cmd))
                else:
                    self.logError(zfunctions.CmdToString(cmd))

            # MOVED INTO ITS OWN FUNCTION
            # for comp in self.data["comps"].values():
            #    actions += comp.Update()

        return actions

    def processUpdates(self):
        actions = []
        for comp in self.data["comps"].values():
            actions += comp.Update()

        return actions

    def getSelfView(self):
        view = {}

        for key in self.view_keys:
            view[key] = self.getData(key)

        comp_view = {}
        for k, v in self.getData("comps").items():
            comp_view[k] = v.getSelfView()
        view["comps"] = comp_view

        return view

    def getJSONView(self):
        view = {}
        for key in self.JSON_keys:
            view[key] = self.getData(key)
        return view

    def getBestDisplayName(self):
        if self.data["callsign"] is not None:
            return self.data["callsign"]
        else:
            return self.data["name"]

    def getAllHeldStoredItems(self):
        item_uuids = []

        for c in self.data["comps"].values():
            if c.getData("ctype") == "Arm":
                if c.isHoldingItem():
                    item_uuids.append(c.getData("item"))

        return item_uuids

    def getAndRemoveAllHeldStoredItems(self):
        item_uuids = []

        for c in self.data["comps"].values():
            if c.getData("ctype") == "Arm":
                if c.isHoldingItem():
                    item_uuids.append(c.getData("item"))
                    c.setData("item", None)

        return item_uuids

import random
import math
import logging

import vec2
import line
import zfunctions

_2PI = 2.0 * math.pi


class Object:
    def __init__(self, data):
        """Initializes default data and view_keys"""
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

    def get_data(self, key):
        """Gets data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set_data(self, key, val):
        """Sets data"""
        self.data[key] = val
        self.data["redraw"] = True

    def is_alive(self):
        """Deterimines if object is alive"""
        return self.get_data("alive")

    def add_comp(self, comp):
        """Adds component"""
        next_id = str(len(self.data["comps"]))
        comp.set_data("slot_id", next_id)
        self.data["comps"][next_id] = comp

    def get_comp(self, slot_id):
        """Gets component"""
        if slot_id in self.get_data("comps"):
            return self.get_data("comps")[slot_id]
        else:
            return None

    def place(self, data):
        """Sets all key/value pairs"""
        for k, v in data.items():
            self.data[k] = v
        self.init_logger()

    def init_logger(self):
        """Initializes logger"""
        if self.get_data("ai") is not None:
            self.logger = logging.getLogger(
                self.get_data("teamname") + "." + self.get_data("callsign")
            )
            self.logger.setLevel(logging.DEBUG)
            self.handler = logging.FileHandler(
                "log/" + self.logger.name + ".log", mode="w"
            )
            self.formatter = logging.Formatter("%(name)s - %(message)s")
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)

    # Obj-level pass through functions to the logger
    def log_debug(self, msg):
        """Logs debug message"""
        if self.logger is not None:
            self.logger.debug(msg)

    def log_info(self, msg):
        """Logs info message"""
        if self.logger is not None:
            self.logger.info(msg)

    def log_warning(self, msg):
        """Logs warning message"""
        if self.logger is not None:
            self.logger.warning(msg)

    def log_error(self, msg):
        """Logs error message"""
        if self.logger is not None:
            self.logger.error(msg)

    def log_critical(self, msg):
        """Logs critical message"""
        if self.logger is not None:
            self.logger.critical(msg)

    def update(self, view):
        """Updates object based on ai script"""
        if self.is_alive():
            try:
                if self.data["ai"] is not None:
                    view["self"] = self.get_self_view()
                    return self.data["ai"].run_ai(view)
                else:
                    return None
            except Exception as e:
                self.log_error("run_ai() raised an exception: " + str(e))
                # log.LogMostRecentException(
                #     "AI script for team "+
                #     self.get_data('teamname') +
                #     " agent " + self.get_data('callsign') +
                #     " raised the exception: " + str(e)

                # )

    def damage_obj(self, amt):
        """Applies damage to object"""
        # Add damage to current total
        old_damage = self.get_data("damage")
        new_damage = old_damage + amt
        self.set_data("damage", new_damage)

        self.log_info("Damaged for " + str(amt) + " - Total Damage: " + str(new_damage))

        points = 0
        if self.get_data("points_count"):
            points = amt

        # If it's still alive and damage is greater than health,
        # OBJECT IS DESTROYED.
        if self.is_alive() and new_damage >= self.get_data("health"):
            self.set_data("alive", False)

            self.log_info("DESTROYED!!!")

            points = self.get_data("health") - old_damage

        return points

    def get_draw_data(self):
        """Gets draw data"""
        fill = self.get_data("fill_alive")
        if not self.is_alive():
            fill = self.get_data("fill_dead")
        redraw = self.get_data("redraw")
        self.data["redraw"] = False
        return {
            "uuid": self.get_data("uuid"),
            "x": self.get_data("x"),
            "y": self.get_data("y"),
            "alive": self.is_alive(),
            "text": self.get_data("text"),
            "fill": fill,
            "redraw": redraw,
            "name": self.get_data("name"),
            "facing": self.data["facing"],
            "sprite_path": self.get_data("sprite_path"),
            "death_sprite_path": self.get_data("death_sprite_path"),
        }

    def process_commands(self, cmds):
        """Process commands given to each component of object"""
        actions = []
        if self.is_alive():

            # Find number of commands that can be ordered.
            max_cmds = 0
            for comp in self.get_data("comps").values():
                if comp.get_data("ctype") == "CnC":
                    max_cmds += comp.get_data("max_cmds_per_tick")

            for slot_id, cmd in cmds.items():

                # Check and reduce commands remaining
                # Having this outside the if-statment below
                # means that even badly formed commands count.
                if max_cmds == 0:
                    break
                else:
                    max_cmds -= 1

                if slot_id in self.data["comps"]:
                    actions += self.data["comps"][slot_id].command(cmd)
                    self.log_info(zfunctions.cmd_to_string(cmd))
                else:
                    self.log_error(zfunctions.cmd_to_string(cmd))

            # MOVED INTO ITS OWN FUNCTION
            # for comp in self.data["comps"].values():
            #    actions += comp.Update()

        return actions

    def process_updates(self):
        """Process updates to each component of object"""
        actions = []
        for comp in self.data["comps"].values():
            actions += comp.update()

        return actions

    def get_self_view(self):
        """Get self view"""
        view = {}

        for key in self.view_keys:
            view[key] = self.get_data(key)

        comp_view = {}
        for k, v in self.get_data("comps").items():
            comp_view[k] = v.get_self_view()
        view["comps"] = comp_view

        return view

    def get_json_view(self):
        """Get JSON view"""
        view = {}
        for key in self.JSON_keys:
            view[key] = self.get_data(key)
        return view

    def get_best_display_name(self):
        """Get best display name"""
        if self.data["callsign"] is not None:
            return self.data["callsign"]
        else:
            return self.data["name"]

    def get_all_held_stored_items(self):
        """Get all held/stored items"""
        item_uuids = []

        for c in self.data["comps"].values():
            if c.get_data("ctype") == "Arm":
                if c.is_holding_item():
                    item_uuids.append(c.get_data("item"))

        return item_uuids

    def get_and_remove_all_held_stored_items(self):
        """Get and removie all held/stored items"""
        item_uuids = []

        for c in self.data["comps"].values():
            if c.get_data("ctype") == "Arm":
                if c.is_holding_item():
                    item_uuids.append(c.get_data("item"))
                    c.set_data("item", None)

        return item_uuids

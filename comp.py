import math
import copy

import vec2
import action

CTYPES_LIST = ["FixedGun", "Engine", "Radar", "CnC", "Radio", "Arm"]

COMP_ATTRS_BY_CTYPE = {
    "FixedGun": [
        ("reload_ticks", 1),
        ("ammunition", 0),
        ("min_damage", 0),
        ("max_damage", 0),
        ("range", 0),
    ],
    "Engine": [("min_speed", 0.0), ("max_speed", 0.0), ("max_turnrate", 0.0)],
    "Radar": [
        ("range", 0),
        ("level", 0),
        ("visarc", 0),
        ("offset_angle", 0),
        ("resolution", 0),
    ],
    "CnC": [("max_cmds_per_tick", 0)],
    "Radio": [
        ("max_range", 0),
    ],
    "Arm": [("max_bulk", 0), ("max_weight", 0)],
}


class Comp:
    def __init__(self, data):
        """Initializes component data

        Sets data to input
        Sets command, update, and view_keys functions based on component type
        """

        self.data = copy.deepcopy(data)

        self.command = self.no_command
        self.update = self.no_update
        self.view_keys = []
        self.set_view_keys_basic()

        ctype = self.data["ctype"]
        if ctype == "FixedGun":
            self.command = self.fixed_gun_command
            self.update = self.fixed_gun_update
            self.set_view_keys_fixed_gun()
            self.data["reload_ticks_remaining"] = 0
            self.data["reloading"] = False
        elif ctype == "Engine":
            self.command = self.engine_command
            self.update = self.engine_update
            self.set_view_keys_engine()
            self.data["cur_speed"] = 0.0
            self.data["cur_turnrate"] = 0.0
        elif ctype == "Radar":
            self.command = self.radar_command
            self.update = self.radar_update
            self.set_view_keys_radar()
            self.data["active"] = False
        elif ctype == "CnC":
            self.command = self.cnc_command
            self.update = self.cnc_update
            self.set_view_keys_cnc()
        elif ctype == "Radio":
            self.command = self.radar_command
            self.update = self.radio_update
            self.set_view_keys_radio()
            self.data["message"] = None
        elif ctype == "Arm":
            self.command = self.arm_command
            self.update = self.arm_update
            self.set_view_keys_arm()
            self.data["item"] = None

    def get_data(self, key):
        """Gets data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set_data(self, key, value):
        """Sets data"""
        self.data[key] = value

    ###########################################################################
    # Self View dispatch
    def set_view_keys_basic(self):
        """Sets view keys to basic/default configuration"""
        self.view_keys += ["id", "name", "ctype", "slot_id"]

    def set_view_keys_fixed_gun(self):
        """Sets view keys to fixed gun configuration"""
        self.view_keys += [
            "reload_ticks",
            "reload_ticks_remaining",
            "reloading",
            "ammunition",
            "min_damage",
            "max_damage",
            "range",
        ]

    def set_view_keys_engine(self):
        """Sets view keys to engine configuration"""
        self.view_keys += [
            "min_speed",
            "max_speed",
            "cur_speed",
            "max_turnrate",
            "cur_turnrate",
        ]

    def set_view_keys_radar(self):
        """Sets view keys to radar configuration"""
        self.view_keys += [
            "active",
            "range",
            "level",
            "visarc",
            "offset_angle",
            "resolution",
        ]

    def set_view_keys_cnc(self):
        """Sets view keys to cnc configuration"""
        self.view_keys += ["max_cmds_per_tick"]

    def set_view_keys_radio(self):
        """Sets view keys to radio configuration"""
        self.view_keys += ["range"]

    def set_view_keys_arm(self):
        """Sets view keys to arm configuration"""
        self.view_keys += ["max_weight", "max_bulk", "item"]

    def get_self_view(self):
        """Gets self view"""
        view = {}
        for key in self.view_keys:
            view[key] = self.get_data(key)
        return view

    ##########################################################################
    # UPDATE METHODS
    ##########################################################################

    ###################################
    # Default
    def no_command(self, cmd):
        """Default command (does nothing)

        Intended for use in comps that never produce actions
        """
        return []

    def no_update(self):
        """Default update (does nothing)

        Intended for use in comps that never produce actions
        """
        return []

    ###################################
    # Fixed Gun
    def fixed_gun_command(self, cmd):
        """Update fixed gune data based on command

        Options: FIRE, RELOAD
        """
        actions = []

        if "command" in cmd:
            if cmd["command"] == "FIRE":

                if self.is_loaded():
                    # Reset the reload ticks
                    self.set_reload_ticks_to_full()

                    a = action.Action()
                    a.set_type("HIGHSPEED_PROJECTILE")
                    a.add_data("slot_id", self.get_data("slot_id"))
                    a.add_data("compname", self.get_data("name"))
                    a.add_data("direction", self.get_data("parent").get_data("facing"))
                    a.add_data("min_damage", self.get_data("min_damage"))
                    a.add_data("max_damage", self.get_data("max_damage"))
                    a.add_data("range", self.get_data("range"))
                    actions.append(a)

            elif cmd["command"] == "RELOAD":

                # We can reload if we aren't reloading,
                #   we are not currently loaded
                #   and we have ammo left.
                if (
                    not self.data["reloading"]
                    and not self.is_loaded()
                    and self.get_data("ammunition") > 0
                ):
                    self.data["reloading"] = True

        # See if we were reloading
        self.update_reloading()

        return actions

    def fixed_gun_update(self):
        """Update fixed gun data based on if it's reloading"""
        # See if we were reloading
        self.update_reloading()

        return []

    ###################################
    # Engine
    def engine_command(self, cmd):
        """Update engine data based on command

        Options: SET_SPEED, SET_TURNRATE
        """
        actions = []

        if "command" in cmd:

            if cmd["command"] == "SET_SPEED":

                if "speed" in cmd:
                    new_speed = cmd["speed"]
                    if new_speed < self.get_data("min_speed"):
                        self.data["cur_speed"] = self.get_data("min_speed")
                    elif new_speed > self.get_data("max_speed"):
                        self.data["cur_speed"] = self.get_data("max_speed")
                    else:
                        self.data["cur_speed"] = new_speed

            elif cmd["command"] == "SET_TURNRATE":

                if "turnrate" in cmd:
                    new_turnrate = cmd["turnrate"]

                    if abs(new_turnrate) <= self.get_data("max_turnrate"):
                        self.data["cur_turnrate"] = new_turnrate
                    else:
                        self.data["cur_turnrate"] = self.get_data("max_turnrate")

        return actions

    def engine_update(self):
        """Update engine data based on if it's moving and/or turning"""
        actions = []

        if self.is_moving():
            a = action.Action()
            a.set_type("MOVE")
            a.add_data("slot_id", self.get_data("slot_id"))
            a.add_data("speed", self.get_data("cur_speed"))
            actions.append(a)

        if self.is_turning():
            a = action.Action()
            a.set_type("TURN")
            a.add_data("slot_id", self.get_data("slot_id"))
            a.add_data("turnrate", self.get_data("cur_turnrate"))
            actions.append(a)

        return actions

    ###################################
    # Radar
    def radar_command(self, cmd):
        """Update radar data based on command

        Options: ACTIVATE_RADAR, DEACTIVATE_RADAR
        """
        if "command" in cmd:
            if cmd["command"] == "ACTIVATE_RADAR":
                self.make_active()
            elif cmd["command"] == "DEACTIVATE_RADAR":
                self.make_inactive()

        return []

    def radar_update(self):
        """Update radar data based on if it's activated"""
        actions = []

        if self.is_active():
            a = action.Action()
            a.set_type("TRANSMIT_RADAR")
            a.add_data("slot_id", self.get_data("slot_id"))
            a.add_data("compname", self.get_data("name"))
            a.add_data("ctype", self.get_data("ctype"))
            a.add_data("range", self.get_data("range"))
            a.add_data("offset_angle", self.get_data("offset_angle"))
            a.add_data("level", self.get_data("level"))
            a.add_data("visarc", self.get_data("visarc"))
            a.add_data("offset_angle", self.get_data("offset_angle"))
            a.add_data("resolution", self.get_data("resolution"))
            actions.append(a)

        return actions

    ##################################
    # CnC
    def cnc_command(self, cmd):
        """Update CnC data based on command (does nothing)"""
        return []

    def cnc_update(self):
        """Update CnC data (does nothing)"""
        return []

    ###################################
    # Radio
    def radio_command(self, cmd):
        """Update radio data based on command

        Options: BROADCAST, SET_RANGE
        """
        if "command" in cmd:
            if cmd["command"] == "BROADCAST" and "message" in cmd:
                self.set_data("message", cmd["message"])

            elif cmd["command"] == "SET_RANGE" and "range" in cmd:
                new_range = cmd["range"]
                if 0 <= new_range <= self.get_data("max_range"):
                    self.set_data("cur_range", new_range)

        return []

    def radio_update(self):
        """Update radio data based on if there is a message"""
        actions = []

        if self.get_data("message") is not None:
            a = action.Action()
            a.set_type("BROADCAST")
            a.add_data("slot_id", self.get_data("slot_id"))
            a.add_data("message", self.get_data("message"))
            a.add_data("range", self.get_data("cur_range"))
            actions.append(a)

        return actions

    ###################################
    # Arm Update
    def arm_command(self, cmd):
        """Update arm data based on command

        Options: TAKE_ITEM, DROP_ITEM
        """
        actions = []

        if "command" in cmd:
            if cmd["command"] == "TAKE_ITEM":
                a = action.Action()
                a.set_type("TAKE_ITEM")
                a.add_data("slot_id", self.get_data("slot_id"))

                if "item_name" in cmd:
                    a.add_data("item_name", cmd["item_name"])
                else:
                    a.add_data("item_name", None)

                if "item_index" in cmd:
                    a.add_data("item_index", cmd["item_index"])
                else:
                    a.add_data("item_index", None)

                if "item_uuid" in cmd:
                    a.add_data("item_uuid", cmd["item_uuid"])
                else:
                    a.add_data("item_uuid", None)

                if "location" in cmd:
                    a.add_data("location", cmd["location"])
                else:
                    a.add_data("location", None)

                actions.append(a)

            elif cmd["command"] == "DROP_ITEM":
                a = action.Action()
                a.set_type("DROP_ITEM")
                a.add_data("slot_id", self.get_data("slot_id"))
                a.add_data("location", cmd["location"])
                actions.append(a)

        return actions

    def arm_update(self):
        "Update Arm data (does nothing)"

        return []

    ###########################################################################
    ## WEAPON RELATED FUNCTIONS
    def set_reload_ticks_to_full(self):
        """Set reload ticks to full"""
        self.data["reload_ticks_remaining"] = self.data["reload_ticks"]

    def is_loaded(self):
        """Deteremines if weapon loaded"""
        return self.data["reload_ticks_remaining"] == 0

    def update_reloading(self):
        """Decrement reloading ticks"""
        if self.data["reloading"]:
            if self.data["reload_ticks_remaining"] > 0:
                self.data["reload_ticks_remaining"] -= 1
                if self.data["reload_ticks_remaining"] == 0:
                    self.data["reloading"] = False
            else:
                self.data["reloading"] = False

    ###########################################################################
    ## ENGINE RELATED FUNCTIONS
    def is_moving(self):
        """Determines if engine is moving"""
        return self.data["cur_speed"] != 0.0

    def is_turning(self):
        """Determines if engine is turning"""
        return self.data["cur_turnrate"] != 0.0

    ###########################################################################
    ## RADAR RELATED FUCNTIONS
    def is_transmitting(self):
        """Determines if radar is transmitting"""
        return self.get_data("active")

    ###########################################################################
    ## ARM RELATED FUNCTIONS
    def is_holding_item(self):
        """Determines if arm is holding an item"""
        return self.get_data("item") is not None

    def can_take_item(self, weight, bulk):
        """Determines if arm can take item"""
        return (
            self.get_data("max_weight") >= weight and self.get_data("max_bulk") >= bulk
        )

    ###########################################################################
    ##
    def is_active(self):
        """Determines if component is active"""
        return self.get_data("active")

    def make_active(self):
        """Makes component active"""
        self.set_data("active", True)

    def make_inactive(self):
        """Makes component inactive"""
        self.set_data("active", False)

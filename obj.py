import math
import logging
# import copy
import zfunctions
# import comp

_2PI = 2.0 * math.pi


class Object:
    def __init__(self, unique_id, template):
        """Initializes default data and view_keys"""

        self.uuid = unique_id
        self.comp_ids = template["comp_ids"]
        self.alive_sprite_filename = template["alive_sprite_filename"]
        self.dead_sprite_filename = template["dead_sprite_filename"]
        self.density = template["density"]
        self.template_id = template["id"]
        self.name = template["name"]
        self.health = template["health"]
        self.damage_to_points = template["damage_to_points"]
        self.redraw = True

        # Filled in during sim build.
        self.x = 0.0
        self.y = 0.0
        self.damage = 0.0
        self.facing = 0.0
        self.sprite = None
        self.comps = {}

        # Agent data
        self.ai_script = None
        self.team_name = None
        self.callsign = None
        self.squad = None
        self.logger = None
        self.points = 0.0

    def __eq__(self, other):
        if isinstance(other, Object):
            return self.uuid == other.uuid
        else:
            return False

    def get_uuid(self):
        return self.uuid

    def build_comps(self, ldr):
        # for ctype in comp.CTYPES_LIST:
        #     self.comps[ctype] = None

        for comp_id in self.comp_ids:
            new_comp = ldr.build_comp(comp_id)
            new_comp.set_parent(self)
            ctype = new_comp.get_ctype()
            self.comps[ctype] = new_comp

    def init_basic_data(self, **kwargs):
        self.x = kwargs["x"] + 0.5
        self.y = kwargs["y"] + 0.5
        self.facing = kwargs["facing"]

    def init_agent_data(self, **kwargs):
        self.damage = kwargs["damage"]
        self.sprite = kwargs["sprite"]
        self.ai_script = kwargs["ai_script"]
        self.team_name = kwargs["team_name"]
        self.callsign = kwargs["callsign"]
        self.squad = kwargs["squad"]

        # This object is an agent, so it needs a logger.
        self.init_logger()

        # Init AI script
        self.init_ai_script()

    def init_ai_script(self):
        """Provides starting information to the AI script."""
        self.ai_script.update(
            team_name=self.team_name,
            callsign=self.callsign,
            squad=self.squad,
            x=self.x,
            y=self.y,
            facing=self.facing,
            damage=self.damage,
            health=self.health
        )

    def get_name(self):
        return self.name

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

    def get_facing(self):
        return self.facing

    def get_damage(self):
        return self.damage

    def get_health(self):
        return self.health

    def get_density(self):
        return self.density

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def add_points(self, points):
        self.points += points

    def is_alive(self):
        """Determines if object is alive"""
        return self.damage < self.health

    def is_dead(self):
        return not self.is_alive()

    def get_comp(self, ctype, index):
        """Gets component"""
        if ctype in self.comps:
            # if len(self.comps[ctype]) < index:
            return self.comps[ctype]
        return None

    def get_alive_sprite_filename(self):
        return self.alive_sprite_filename

    def get_dead_sprite_filename(self):
        return self.dead_sprite_filename

    def get_sprite_filename_based_on_damage(self):
        if self.is_alive():
            return self.get_alive_sprite_filename()
        else:
            return self.get_dead_sprite_filename()

    def get_redraw(self):
        return self.redraw

    def set_redraw(self, redraw):
        self.redraw = redraw

    def init_logger(self):
        """Initializes logger"""
        self.logger = logging.getLogger(
            f"{self.team_name}.{self.squad}.{self.callsign}"
        )
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            f"log/{self.logger.name}.log", mode="w"
        )
        formatter = logging.Formatter("%(name)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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
            if self.ai_script is not None:
                view["self"] = self.get_self_view()
                return self.ai_script.run_ai(view)
            else:
                return None

    def damage_obj(self, amt):
        """Applies damage to object. And returns the points to be given to the
        damaging object."""
        points = 0
        if self.damage < self.health:
            points = amt
            new_damage = self.damage + amt
            if new_damage >= self.health:
                points = self.health - self.damage
                self.damage = self.health
            else:
                self.damage = new_damage
            points = points * self.damage_to_points

            self.log_info(f"Damaged for {amt} - Total Damage: {self.damage}/{self.health}")

            # If it's still alive and damage is greater than health,
            # OBJECT IS DESTROYED.
            if self.damage >= self.health:
                self.log_info("DESTROYED!!!")

        return points

    def get_draw_data(self):
        """Gets draw data"""

        dd = {
            "uuid": self.uuid,
            "x": self.get_cell_x(),
            "y": self.get_cell_y(),
            "alive": self.is_alive(),
            "redraw": self.redraw,
            "name": self.name,
            "facing": self.facing,
            "sprite_filename": self.alive_sprite_filename if self.is_alive() else self.dead_sprite_filename,
            "sprite_type": "object"
        }

        return dd

    def process_commands(self, cmds):
        """Process commands given to each component of object"""
        actions = []
        if self.is_alive():

            # Find number of commands that can be ordered.
            # By default, the object can issue a command to every
            # component.
            max_cmds = len(self.comps)
            if "CnC" in self.comps:
                cnc_comp = self.comps["CnC"]
                max_cmds = cnc_comp.get_data("max_cmds_per_tick")

            for ctype, cmd in cmds.items():

                print("OBJECT PROCESS COMMANDS:", ctype, cmd)

                # Check and reduce commands remaining
                # Having this outside the if-statment below
                # means that even badly formed commands count.
                if max_cmds == 0:
                    break
                else:
                    max_cmds -= 1

                if ctype in self.comps:
                    actions += self.comps[ctype].command(cmd)
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
        for c in self.comps.values():
            actions += c.update()

        return actions

    def get_self_view(self):
        """Get self view"""
        view = {
            "x": self.x,
            "y": self.y,
            "damage": self.damage,
            "health": self.health,
            "facing": self.facing,
            "density": self.density,
            "callsign": self.callsign,
            "squad": self.squad,
            "team_name": self.team_name
        }

        comp_view = {}
        for k, v in self.comps.items():
            comp_view[k] = v.get_self_view()
        view["comps"] = comp_view

        return view

    # def get_json_view(self):
    #     """Get JSON view"""
    #     view = {}
    #     for key in self.JSON_keys:
    #         view[key] = self.get_data(key)
    #     return view

    def get_best_display_name(self):
        """Get best display name"""
        if self.callsign is not None:
            return self.callsign
        else:
            return self.name

    def get_all_held_stored_items(self):
        """Get all held/stored items"""
        item_uuids = []

        if "Arm" in self.comps:
            c = self.comps["Arm"]
            if c.is_holding_item():
                item_uuids.append(c.get_data("item"))

        # for c in self.comps.values():
        #     if c.get_data("ctype") == "Arm":
        #         if c.is_holding_item():
        #             item_uuids.append(c.get_data("item"))

        return item_uuids

    def get_and_remove_all_held_stored_items(self):
        """Get and remove all held/stored items"""
        item_uuids = []

        if "Arm" in self.comps:
            c = self.comps["Arm"]
            if c.is_holding_item():
                item_uuids.append(c.get_data("item"))
                c.set_data("item", None)

        # for c in self.comps.values():
        #     if c.get_data("ctype") == "Arm":
        #         if c.is_holding_item():
        #             item_uuids.append(c.get_data("item"))
        #             c.set_data("item", None)

        return item_uuids

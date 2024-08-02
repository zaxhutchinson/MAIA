# Loads teams and other stuff

import json
import uuid
import obj
import copy
import map
import item
import comp
import goal
import team

class Loader:
    def __init__(self, logger=None):
        """Initializes empty dict templates and loads jsons"""
        self.main_config = {}
        self.obj_templates = {}
        self.item_templates = {}
        self.comp_templates = {}
        self.map_templates = {}
        self.team_templates = {}
        self.goal_templates = {}

        self.DIRECTORY = "settings"
        self.MAIN_JSON_FILENAME = f"{self.DIRECTORY}/main.json"
        self.COMPONENTS_JSON_FILENAME = f"{self.DIRECTORY}/components.json"
        self.OBJECTS_JSON_FILENAME = f"{self.DIRECTORY}/objects.json"
        self.ITEM_JSON_FILENAME = f"{self.DIRECTORY}/items.json"
        self.MAP_JSON_FILENAME = f"{self.DIRECTORY}/maps.json"
        self.TEAM_JSON_FILENAME = f"{self.DIRECTORY}/teams.json"
        # self.GOALS_JSON_FILENAME = f"{self.DIRECTORY}/goals.json"

        self.load_main_config()
        self.LoadAllTemplates()
        # self.load_goal_templates()

        self.logger = logger

    def LoadAllTemplates(self):
        self.load_comp_templates()
        self.load_obj_templates()
        self.load_item_templates()
        self.load_map_templates()
        self.load_team_templates()

    ##########################################################################
    # GSTATE
    # def load_goal_templates(self):
    #     """Loads goal templates"""
    #     with open(self.GOALS_JSON_FILENAME, "r") as f:
    #         json_objs = json.load(f)
    #         for k, v in json_objs.items():
    #             self.goal_templates[k] = v
    #
    # def save_goal_templates(self):
    #     if len(self.goal_templates) > 0:
    #         with open(self.GOALS_JSON_FILENAME, "w") as f:
    #             json.dump(self.goal_templates, f, indent=4, sort_keys=True)
    #
    # def build_goal(self, _id):
    #     return goal.Goal(self.goal_templates[_id])
    #
    # def get_goal_template(self, _id):
    #     return self.goal_templates[_id]
    #
    # def get_goal_templates(self):
    #     return self.goal_templates

    ##########################################################################
    # OBJ
    def load_obj_templates(self):
        """Loads object templates"""
        with open(self.OBJECTS_JSON_FILENAME, "r") as f:
            json_objs = json.load(f)
            for k, v in json_objs.items():
                self.obj_templates[k] = v

    def save_obj_templates(self):
        if len(self.obj_templates) > 0:
            with open(self.OBJECTS_JSON_FILENAME, "w") as f:
                json.dump(self.obj_templates, f, indent=4, sort_keys=True)

    def build_obj(self, _id):
        """Builds an object from a template"""
        return obj.Object(uuid.uuid4(), self.obj_templates[_id])

    def get_obj_template(self, _id):
        """Returns the object template specified by the _id"""
        try:
            return self.obj_templates[_id]
        except KeyError:
            return None

    def get_obj_templates(self):
        "Returns all templates"
        return self.obj_templates

    def copy_obj_template(self, _id):
        """Produces a deep copy of a object template"""
        try:
            return copy.deepcopy(self.obj_templates[_id])
        except KeyError:
            self.logger.error("LOADER: copyObjTemplate() KeyError " + str(_id))

    def get_obj_ids(self):
        """Gets object ids"""
        return list(self.obj_templates.keys())

    def get_obj_names(self):
        """Gets object names"""
        obj_names = []
        for object in self.obj_templates.values():
            obj_names.append(object.get_data("name"))
        return obj_names

    ##########################################################################
    # ITEMS
    def load_item_templates(self):
        """Loads item templates"""
        with open(self.ITEM_JSON_FILENAME, "r") as f:
            json_objs = json.load(f)
            for k, v in json_objs.items():
                self.item_templates[k] = v

    def save_item_templates(self):
        if len(self.item_templates) > 0:
            with open(self.ITEM_JSON_FILENAME, "w") as f:
                json.dump(self.item_templates, f, indent=4, sort_keys=True)

    def get_item_template(self, _id):
        return self.item_templates[_id]

    def get_item_templates(self):
        return self.item_templates

    def build_item(self, _id):
        return item.Item(uuid.uuid4(), self.item_templates[_id])

    def copy_item_template(self, _id):
        """Produces a deep copy of an item template"""
        try:
            return copy.deepcopy(self.item_templates[_id])
        except KeyError:
            self.logger.error(
                "LOADER: copyItemTemplate() KeyError " + str(_id)
            )

    ##########################################################################
    # COMPS
    # TODO: Need to clean up the comp template functions. Some are old
    #   and should not be used any longer.

    def load_comp_templates(self):
        """Loads component templates"""
        with open(self.COMPONENTS_JSON_FILENAME, "r") as f:
            json_objs = json.load(f)
            for k, v in json_objs.items():
                self.comp_templates[k] = v

    def save_comp_templates(self):
        if len(self.comp_templates) > 0:
            with open(self.COMPONENTS_JSON_FILENAME, "w") as f:
                json.dump(self.comp_templates, f, indent=4, sort_keys=True)

    def get_comp_template(self, _id):
        return self.comp_templates[_id]

    def get_comp_templates(self):
        return self.comp_templates

    # def get_comp_name(self, _id):
    #     return self.comp_templates[_id].get_data("name")

    def build_comp(self, _id):
        return comp.Comp(self.comp_templates[_id])

    def copy_comp_template(self, _id):
        """Produces a deep copy of a component template"""
        try:
            return copy.deepcopy(self.comp_templates[_id])
        except KeyError:
            self.logger.error(
                "LOADER: copyCompTemplate() KeyError " + str(_id)
            )

    def get_comp_ids(self):
        """Gets component ids"""
        return list(self.comp_templates.keys())

    def get_comp_ids_of_ctype(self, _ctype):
        comp_ids = []
        for _id, _comp in self.comp_templates.items():
            if _comp["ctype"] == _ctype:
                comp_ids.append(_id)
        return comp_ids

    def get_comp(self, _id):
        return self.comp_templates[_id]

    def get_comp_names(self):
        """Gets component names"""
        comp_names = []
        for component in self.comp_templates.values():
            comp_names.append(component.get_data("name"))
        return comp_names

    def get_comp_names_of_type(self, _type):
        comps = []
        for component in self.comp_templates.values():
            if component.get_data("ctype") == _type:
                comps.append(component.get_data("name"))
        return comps

    def get_comp_types(self):
        """Gets component types"""
        comp_types = []
        for component in self.comp_templates.values():
            comp_types.append(component.get_data("ctype"))
        return comp_types

    ##########################################################################
    # MAPS
    def load_map_templates(self):
        """Loads map templates"""
        with open(self.MAP_JSON_FILENAME, "r") as f:
            json_objs = json.load(f)
            for k, v in json_objs.items():
                self.map_templates[k] = v

    def save_map_templates(self):
        if len(self.map_templates) > 0:
            with open(self.MAP_JSON_FILENAME, "w") as f:
                json.dump(self.map_templates, f, indent=4, sort_keys=True)

    def build_map(self, _id):
        return map.Map(self.map_templates[_id])

    def get_map_template(self, _id):
        return self.map_templates[_id]

    def get_map_templates(self):
        return self.map_templates

    def delete_map(self, map_id):
        del self.map_templates[map_id]

    def get_map_ids(self):
        """Gets map ids"""
        return list(self.map_templates.keys())

    ##########################################################################
    # TEAMS
    def load_team_templates(self):
        """Loads team templates"""
        with open(self.TEAM_JSON_FILENAME, "r") as f:
            json_obj = json.load(f)
            for k, v in json_obj.items():
                self.team_templates[k] = v

    def save_team_templates(self):
        if len(self.team_templates) > 0:
            with open(self.TEAM_JSON_FILENAME, "w") as f:
                json.dump(self.team_templates, f, indent=4, sort_keys=True)

    def build_team(self, _id):
        return team.Team(self.team_templates[_id])

    def get_team_templates(self):
        return self.team_templates

    def get_team_template(self, _id):
        return self.team_templates[_id]

    def copy_all_team_templates(self):
        return copy.deepcopy(self.team_templates)

    def copy_team_template(self, _id):
        """Produces a deep copy of a team template"""
        try:
            return copy.deepcopy(self.team_templates[_id])
        except KeyError:
            self.logger.error(
                "LOADER: copyTeamTemplate() KeyError " + str(_id)
            )

    def get_team_ids(self):
        """Gets team ids"""
        return list(self.team_templates.keys())

    def get_team_names(self):
        """Gets team names"""
        names = []
        for t in self.team_templates.values():
            names.append(t["name"])
        return names

    def update_team_template(self, _id, **kwargs):
        try:
            _team = self.team_templates[_id]
            for k, v in kwargs.items():
                try:
                    _team[k] = v
                except KeyError:
                    self.logger.error(
                        f"LOADER: update_team_template() KeyError {k} is an "
                        + "invalid team attribute."
                    )
        except KeyError:
            self.logger.error(f"LOADER: update_team_template() KeyError {_id}")

    ##########################################################################
    # Mainconfig
    def load_main_config(self):
        """Loads main config"""
        with open(self.MAIN_JSON_FILENAME, "r") as f:
            self.main_config = json.load(f)

    def copy_main_config(self):
        """Produces a deep copy of main config"""
        return copy.deepcopy(self.main_config)

    def get_main_config_data(self, key):
        """Gets main config data"""
        try:
            return self.main_config[key]
        except KeyError:
            self.logger.error(f"LOADER: getMainConfigData() KeyError {key}")

import copy
import logging

import trigger
from old_code import agent
import uuid
import random

class Team:
    """This class is currently depreciated and is not in use"""

    def __init__(self, template):
        """Initializes data to input and creates agents"""

        self.name = template["name"]
        self.agent_defs = template["agent_defs"]
        self.agents = []
        self.side_id = None
        self.logger = logging.getLogger(self.name)
        self.handler = logging.FileHandler(
            "log/" + self.logger.name + ".log", mode="w"
        )
        self.formatter = logging.Formatter("%(name)s - %(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.triggers = []

    def build_triggers(self, trigger_list, items):
        for trgr in trigger_list:
            t = trigger.Trigger(trgr)
            t.init(items)
            self.triggers.append(t)

    def get_side_id(self):
        return self.side_id

    def set_side_id(self, side_id):
        self.side_id = side_id

    def get_agent_defs(self):
        return self.agent_defs

    def get_triggers(self):
        return self.triggers

    def get_name(self):
        return self.name

    def add_agent(self, _agent):
        self.agents.append(_agent)

    def get_agents(self):
        return self.agents

    # def create_agents(self, ldr, side_data):
    #     """Creates agents"""
    #     starting_locations = copy.deepcopy(["starting_locations"])
    #     if side_data["random_placement"]:
    #         random.shuffle(starting_locations)
    #
    #     for adef in self.agent_defs:
    #         agent_id = uuid.uuid4()
    #         agent_object = ldr.build_object(adef["object"])
    #         _agent = agent.Agent(adef, agent_id, agent_object, self.name)
    #
    #         self.agents[agent_id] = _agent


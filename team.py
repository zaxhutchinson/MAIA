import logging
import agent


class Team:
    """This class is currently depreciated and is not in use"""

    def __init__(self, data):
        """Initializes data to input and creates agents"""
        self.data = {}
        self.logger = None

        if "name" in data:
            self.logger = logging.getLogger(data["name"])
            self.handler = logging.FileHandler(
                "log/" + self.logger.name + ".log", mode="w"
            )
            self.formatter = logging.Formatter("%(name)s - %(message)s")
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
        else:
            raise KeyError("name")

        self.required_data = []

        self.set_data(data)

        self.create_agents()

    def set_data(self, data):
        """Sets data"""
        # Agents are created later based on agent_defs read from the json
        self.data["agents"] = {}

        req_data = ["size", "agent_defs"]

        for rd in req_data:
            if rd in data:
                self.data[rd] = data[rd]
            else:
                self.data[rd] = None
                self.logger.error("TEAM: Missing data " + rd)

        self.required_data += req_data

    def get_data(self, key):
        """Gets data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def get_number_of_agents(self):
        """Gets number of agents"""
        if "agents" in self.data:
            return len(self.data["agents"])
        else:
            0

    def create_agents(self):
        """Creates agents"""
        agent_defs = self.get_data("agent_defs")

        if agent_defs is None:
            self.logger.error("AGENT: Agent definition data is missing.")
        else:
            for ID, data in agent_defs.items():
                ID = int(ID)
                obj_id = data["object"]
                ai_file_name = data["AI_file"]

                _agent = agent.Agent(ID, obj_id, ai_file_name)
                self.data["agents"][ID] = _agent

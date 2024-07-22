class Agent:
    """This class is currently depreciated and is not in use"""

    def __init__(self, template, team_name, ai_script):
        """Initializes data values to associated params"""
        self.callsign = template["callsign"]
        self.obj_id = template["object"]
        self.ai_filename = template["AI_filename"]
        self.squad = template["squad"]
        self.ai_script = ai_script
        self.team_name = team_name

    # def get_data(self, key):
    #     """Gets data"""
    #     if key in self.data:
    #         return self.data[key]
    #     else:
    #         return None
    #
    # def set_data(self, key, val):
    #     """Sets data"""
    #     self.data[key] = val

    # def setObj(self,obj):
    #     self.obj = obj
    # def getObj(self):
    #     return self.obj
    # def getObjProfile(self):
    #     if self.obj != None:
    #         return self.obj.getObjProfile()
    #     else:
    #         return {}
    # def setAI(self,ai):
    #     self.ai = ai

    # Returns a list of commands

    # def Update(self,world_state):
    #     if self.ai != None:
    #         return self.ai(world_state)
    #     else:
    #         return []

class Agent:
    """This class is currently depreciated and is not in use"""

    def __init__(self, ID, obj_id, ai_filename):
        """Sets data values to associated params"""
        self.data = {}
        self.data["id"] = ID
        self.data["objid"] = obj_id
        self.data["ai_filename"] = ai_filename
        self.data["ai"] = None
        self.data["obj"] = None

    def get_data(self, key):
        """Gets data"""
        if key in self.data:
            return self.data[key]
        else:
            return None

    def set_data(self, key, val):
        """Sets data"""
        self.data[key] = val

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

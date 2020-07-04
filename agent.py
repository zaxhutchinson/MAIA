from log import *

class Agent:
    def __init__(self,ID,obj_id,ai_filename):
        self.data = {}
        self.data['id'] = ID
        self.data['objid'] = obj_id
        self.data['ai_filename']=ai_filename
        self.ai = None
        self.obj = None

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def setObj(self,obj):
        self.obj = obj
    def getObj(self):
        return self.obj
    def getObjProfile(self):
        if self.obj != None:
            return self.obj.getObjProfile()
        else:
            return {}
    def setAI(self,ai):
        self.ai = ai

    # Returns a list of commands
    def Update(self,world_state):
        if self.ai != None:
            return self.ai(world_state)
        else:
            return []
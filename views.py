import copy

class ViewManager:
    def __init__(self):
        self.view_templates = {}
        self.buildTemplates()

    def getViewTemplate(self,vtype):
        if vtype in self.view_templates:
            return copy.deepcopy(self.view_templates[vtype])
        return None

    def buildTemplates(self):
        #####################
        # projectile
        #####################
        v = {}
        v['vtype']='projectile'
        v['compname']=None
        v['hit_x']=None
        v['hit_y']=None
        v['name']=None
        self.view_templates[v['vtype']]=v
        #####################
        # radar
        #####################
        v={}
        v['vtype']='radar'
        v['ctype']=None
        v['tick']=None
        v['compname']=None
        v['slot_id']=None
        v['pings']=[]
        self.view_templates[v['vtype']]=v
        #####################
        # broadcast
        #####################
        v={}
        v['vtype']='broadcast'
        v['tick']=None
        v['message']=""
        self.view_templates[v['vtype']]=v

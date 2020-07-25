# Loads teams and other stuff

import json
import importlib

import obj
import copy
import zmap
import item
import comp
import vec2
import log
import team

class Loader:
    def __init__(self):

        self.main_config={}
        self.obj_templates={}
        self.item_templates={}
        self.comp_templates={}
        self.map_templates={}
        self.team_templates={}

        self.loadMainConfig('settings/main.json')
        self.loadCompTemplates('settings/components.json')
        self.loadObjTemplates("settings/objects.json")
        self.loadItemTemplates("settings/items.json")
        self.loadMapTemplates("settings/maps.json")
        self.loadTeamTemplates("settings/teams.json")

        
    ##########################################################################
    # LOAD/COPY OBJ
    def loadObjTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                self.obj_templates[k] = obj.Object(v)
    def copyObjTemplate(self,_id):
        try:
            return copy.deepcopy(self.obj_templates[_id])
        except KeyError:
            log.LogError("LOADER: copyObjTemplate() KeyError "+str(_id))
    ##########################################################################
    # LOAD/COPY ITEMS
    def loadItemTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                self.item_templates[k] = item.Item(v)
    def copyItemTemplate(self,_id):
        try:
            return copy.deepcopy(self.item_templates[_id])
        except KeyError:
            log.LogError("LOADER: copyItemTemplate() KeyError "+str(_id))
    ##########################################################################
    # LOAD/COPY COMPS
    def loadCompTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                self.comp_templates[k]=comp.Comp(v)
    def copyCompTemplate(self,_id):
        try:
            return copy.deepcopy(self.comp_templates[_id])
        except KeyError:
            log.LogError("LOADER: copyCompTemplate() KeyError "+str(_id))
    ##########################################################################
    # LOAD/COPY MAPS
    def loadMapTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                self.map_templates[k]=zmap.Map(v)
    def copyMapTemplate(self,_id):
        try:
            return copy.deepcopy(self.map_templates[_id])
        except KeyError:
            log.LogError("LOADER: copyMapTemplate() KeyError "+str(_id))
    def getMapIDs(self):
        return list(self.map_templates.keys())
    ##########################################################################
    # LOAD/COPY TEAMS
    def loadTeamTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObj = json.load(f)
            for k,v in jsonObj.items():
                self.team_templates[k]=v
    def copyTeamTemplate(self,_id):
        try:
            return copy.deepcopy(self.team_templates[_id])
        except KeyError:
            log.LogError("LOADER: copyTeamTemplate() KeyError "+str(_id))
    def getTeamIDs(self):
        return list(self.team_templates.keys())
    def getTeamNames(self):
        names = []
        for t in self.team_templates.values():
            names.append(t['name'])
        return names
    ##########################################################################
    # LOAD/COPY Mainconfig
    def loadMainConfig(self,filename):
        with open(filename,'r') as f:
            self.main_config = json.load(f)
    def copyMainConfig(self):
        return copy.deepcopy(self.main_config)
    def getMainConfigData(self,key):
        try:
            return self.main_config[key]
        except KeyError:
            log.LogError("LOADER: getMainConfigData() KeyError "+str(key))



# Loads teams and other stuff

import json
import importlib

import obj
import copy
import zmap
import comp
import vec2
from log import *
import team

class Loader:
    def __init__(self):

        self.main_config={}
        self.obj_templates={}
        self.comp_templates={}
        self.map_templates={}
        self.team_templates={}

        self.loadMainConfig('settings/main.json')
        self.loadCompTemplates('settings/components.json')
        self.loadObjTemplates("settings/objects.json")
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
        return copy.deepcopy(self.obj_templates[_id])
    ##########################################################################
    # LOAD/COPY COMPS
    def loadCompTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                self.comp_templates[k]=comp.Comp(v)
    def copyCompTemplate(self,_id):
        return copy.deepcopy(self.comp_templates[_id])
    ##########################################################################
    # LOAD/COPY MAPS
    def loadMapTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                self.map_templates[k]=zmap.Map(v)
    def copyMapTemplate(self,_id):
        return copy.deepcopy(self.map_templates[_id])
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
        return copy.deepcopy(self.team_templates[_id])
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
        if key in self.main_config:
            return self.main_config[key]
        else:
            return None

    # def loadMaps(self,filename,sim):
    #     with open(filename,'r') as f:
    #         jsonObjs = json.load(f)
    #         for k,v in jsonObjs.items():
    #             _map = zmap.Map(v)

    #             # try:
    #             #     for k2,v2 in v['rand_objects'].items():
    #             #         mS.rand_objects[int(k2)]=int(v2)
    #             # except(KeyError):
    #             #     mS.rand_percent=None
    #             #     mS.rand_objects={}


    #             # try:
    #             #     for k2,v2 in v['placed_objects'].items():
    #             #         for d in v2:
    #             #             if 'pos' in d:
    #             #                 coords = d['pos']
    #             #                 d['pos'] = vec2.Vec2(coords[0],coords[1])

    #             #         mS.placed_objects[int(k2)]=v2
    #             # except(KeyError):
    #             #     mS.placed_objects={}

    #             sim.addMap(_map)

    # def loadComponents(self,filename,sim):
    #     with open(filename,'r') as f:
    #         jsonObjs = json.load(f)
    #         compmodule = importlib.import_module('component')
    #         for k,v in jsonObjs.items():
    #             if 'ctype' not in v:
    #                 LogError('Comp is missing the ctype.')
    #             else:
    #                 ctype = v['ctype']
    #                 CompClass = getattr(compmodule,ctype)
    #                 comp = CompClass(v)
    #                 sim.addComponent(comp)


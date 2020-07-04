# Loads teams and other stuff

import json
import importlib

import obj
import copy
import zmap
import component
import vec2
from log import *
import team

class Loader:
    def __init__(self,sim):

        self.loadMainConfig('settings/main.json',sim)
        self.loadComponents('settings/components.json',sim)
        self.loadObjectTemplates("settings/objects.json",sim)
        self.loadMaps("settings/maps.json",sim)
        self.loadTeamData("settings/teams.json",sim)

    def loadShape(self,shapeData):
        name = shapeData['name']

        shape = None
        
        if name == 'CYLINDER':
            radius = shapeData['radius']
            shape = obj.Cylinder(name,radius)

        elif name == "RECTANGLE":
            width = shapeData['width']
            height = shapeData['height']
            shape = obj.Rectangle(name,width,height)
        
        return shape

    def loadTeamData(self,filename,sim):
        with open(filename,'r') as f:
            jsonObj = json.load(f)
            for k,v in jsonObj.items():
                _team = team.Team(v)
                sim.addTeam(_team)

    def loadMainConfig(self,filename,sim):
        with open(filename,'r') as f:
            sim.mainConfigDict = json.load(f)

    def loadObjectTemplates(self,filename,sim):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                shape = self.loadShape(v['shape'])
                if shape != None:
                    o = obj.Object(v,shape)
                    sim.addObject(o)
                else:
                    LogError('OBJECT is missing shape.')

    def loadMaps(self,filename,sim):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                _map = zmap.Map(v)

                # try:
                #     for k2,v2 in v['rand_objects'].items():
                #         mS.rand_objects[int(k2)]=int(v2)
                # except(KeyError):
                #     mS.rand_percent=None
                #     mS.rand_objects={}


                # try:
                #     for k2,v2 in v['placed_objects'].items():
                #         for d in v2:
                #             if 'pos' in d:
                #                 coords = d['pos']
                #                 d['pos'] = vec2.Vec2(coords[0],coords[1])

                #         mS.placed_objects[int(k2)]=v2
                # except(KeyError):
                #     mS.placed_objects={}

                sim.addMap(_map)

    def loadComponents(self,filename,sim):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            compmodule = importlib.import_module('component')
            for k,v in jsonObjs.items():
                if 'ctype' not in v:
                    LogError('Comp is missing the ctype.')
                else:
                    ctype = v['ctype']
                    CompClass = getattr(compmodule,ctype)
                    comp = CompClass(v)
                    sim.addComponent(comp)


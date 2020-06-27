# Loads teams and other stuff

import json
import importlib

import obj
import copy
import zmap
import component
import vec2
from log import *

class Loader:
    def __init__(self):
        self.objectDict = {}
        self.mapDict = {}
        self.componentDict = {}

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

    def loadObjectTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                shape = self.loadShape(v['shape'])
                if shape != None:
                    if 'ID' in v:
                        o = obj.Object(v,shape)
                        self.objectDict[v['ID']]=o
                    else:
                        LogError('OBJECT is missing ID.')

    def loadMapTemplates(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            for k,v in jsonObjs.items():
                mS = zmap.MapSettings()
                mS.ID = int(k)
                mS.name = v['name']
                mS.width = v['width']
                mS.height = v['height']
                try:
                    for k2,v2 in v['rand_objects'].items():
                        mS.rand_objects[int(k2)]=int(v2)
                except(KeyError):
                    mS.rand_percent=None
                    mS.rand_objects={}


                try:
                    for k2,v2 in v['placed_objects'].items():
                        for d in v2:
                            if 'pos' in d:
                                coords = d['pos']
                                d['pos'] = vec2.Vec2(coords[0],coords[1])

                        mS.placed_objects[int(k2)]=v2
                except(KeyError):
                    mS.placed_objects={}

                self.mapDict[mS.ID]=mS

    def loadComponents(self,filename):
        with open(filename,'r') as f:
            jsonObjs = json.load(f)
            compmodule = importlib.import_module('component')
            for k,v in jsonObjs.items():
                if 'type' not in v:
                    LogError('Comp is missing the type.')
                else:
                    ctype = v['type']
                    CompClass = getattr(compmodule,ctype)
                    comp = CompClass(v)

    def getObject(self,ID):
        return copy.deepcopy(self.objectDict[ID])

    def getMapSetting(self,ID):
        return copy.deepcopy(self.mapDict[ID])
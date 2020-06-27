
import random

import loader
import obj
import vec2
from log import *

# class MapSettings:
#     def __init__(self):
#         self.ID = None
#         self.name = None
#         self.width = 0
#         self.height = 0
#         self.rand_objects = {}
#         self.placed_objects = {}


class Map:
    def __init__(self, data):
        self.objects = []
        self.setData(data)
        

    def setData(self,data):
        self.data = {}
        self.required_data = []

        req_data = [
            'name','width','height'
        ]
            
        for rd in req_data:
            if rd in data:
                self.data[rd] = data[rd]
            else:
                self.data[rd] = None
                LogError("MAP: Missing data "+rd)

        self.required_data += req_data

        opt_data = [
            'rand_objects','placed_objs'
        ]
        for od in opt_data:
            if od in data:
                self.data[od] = data[od]
                self.required_data.append(od)

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def generateMap(self,sim):
        count = 0
        # placed objects
        for k,v in self.data['placed_objects'].items():
            for data in v:
                thisObj = sim.getObject(k)
                thisObj.setDataFromDict(data)
                self.objects.append(thisObj)
        
        # rand objects
        for k,v in self.settings.rand_objects.items():
            for i in range(v):
                thisObj = sim.getObject(k)
                x = random.uniform(0.0,self.width)
                y = random.uniform(0.0,self.height)
                thisObj.setPosition(vec2.Vec2(x,y))
                thisObj.randomize()
                self.objects.append(thisObj)





import random

import loader
import obj
import vec2


class MapSettings:
    def __init__(self):
        self.ID = None
        self.name = None
        self.width = 0
        self.height = 0
        self.rand_objects = {}
        self.placed_objects = {}


class Map:
    def __init__(self, settings):
        self.name = settings.name
        self.width = settings.width
        self.height = settings.height
        self.objects = []
        self.settings = settings

    def generateMap(self,loader):
        count = 0
        # placed objects
        for k,v in self.settings.placed_objects.items():
            for data in v:
                thisObj = loader.getObject(k)
                thisObj.setDataFromDict(data)
                self.objects.append(thisObj)
        
        # rand objects
        for k,v in self.settings.rand_objects.items():
            for i in range(v):
                thisObj = loader.getObject(k)
                x = random.uniform(0.0,self.width)
                y = random.uniform(0.0,self.height)
                thisObj.setPosition(vec2.Vec2(x,y))
                thisObj.randomize()
                self.objects.append(thisObj)




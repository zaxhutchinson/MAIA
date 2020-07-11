
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
        self.data = data

    def setData(self,key,val):
        self.data[key]=val
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    # def getTeamLabels(self):
    #     return list(self.data['starting_regions'].keys())

    # def getOpenStartingPosition(self,team_index):
    #     if team_index in self.open_starting_positions:
    #         if len(self.open_starting_positions[team_index]) > 0:
    #             return self.open_starting_positions[team_index].pop()
    #         else:
    #             LogError("MAP: getOpenStartingPosition() attempt to get another position from empty team list.")
    #     else:
    #         LogError("MAP: getOpenStartingPosition() team_index not in open positions.")

    # def addObject(self,obj):
    #     for o in self.objects:
            
    #         self.objects.append(obj)


    # def addTeam(self,team,team_index):
    #     if team.getNumberOfAgents() != self.getData('agents'):
    #         LogError("MAP: addTeam() map does not support "+str(team.getNumberOfAgents())+" agents.")
    #     else:
    #         agents = team.getData('agents')
                    
    #         for i in range(len(agents)):
    #             agents[i].getObject().setPosition(self.getOpenStartingPosition(team_index))
    #             if not self.addObject(agents[i].getObject()):
    #                 LogError("MAP: addTeam() attempt to add agent to an already occupied location.")



    # def generateMap(self,sim):
    #     count = 0
    #     # placed objects
    #     if 'placed_objects' in self.data:
    #         for k,v in self.data['placed_objects'].items():
    #             for data in v:
    #                 thisObj = sim.getObject(int(k))
    #                 thisObj.initObjectFromData(data)
    #                 self.addObject(thisObj)
        
        # rand objects
        # if 'rand_objects' in self.data:
        #     for k,v in self.data['rand_objects'].items():
        #         for i in range(v):
        #             thisObj = sim.getObject(int(k))
        #             x = random.uniform(0.0,self.data['width'])
        #             y = random.uniform(0.0,self.data['height'])
        #             thisObj.setPosition(vec2.Vec2(x,y))
        #             thisObj.randomize()
        #             self.addObject(thisObj)

        


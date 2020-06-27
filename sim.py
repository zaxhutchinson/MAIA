import importlib

import obj
import copy
import zmap
import component
import vec2
from log import *

class Sim:
    def __init__(self):
        self.objectDict = {}
        self.mapDict = {}
        self.componentDict = {}
        self.mainConfigDict = {}
        self.teamDict = {}

        self.teamsInPlay = {}


    def addObject(self,_obj):
        key = _obj.getData('id')
        if key != None:
            self.objectDict[key]=_obj

    def addComponent(self,comp):
        key = comp.getData('id')
        if key != None:
            self.componentDict[key] = comp

    def addMap(self,_map):
        key = _map.getData('id')
        if key != None:
            self.mapDict[key] = _map

    def addTeam(self,team):
        key = team.getData('name')
        if key != None:
            self.teamDict[key]=team


    def buildObject(self,key):
        if key in self.objectDict:
            _obj = copy.deepcopy(self.objectDict[key])

            comps = _obj.getData('component_ids')
            if comps != None:
                
                for c in comps:
                    newComp = self.buildComponent(c)
                    _obj.addComponent(newComp)


    def buildComponent(self,key):
        if key in self.componentDict:
            comp = copy.deepcopy(self.componentDict[key])

        return comp

    def clearTeamsInPlay(self):
        self.teamsInPlay.clear()
    

    def buildTeam(self,key):
        if key in self.teamDict:
            _team = self.getTeam(key)

            name = _team.getData('name')
            _agents = _team.getData('agents')
            for agent in _agents.items():
                self.buildAgent(agent,name)

            self.teamsInPlay[key]=_team

    def buildAgent(self,_agent,teamName):
        if _agent != None:
            objid = _agent.getData('objid')
            ai_filename = _agent.getData('ai_filename')
            _agent.setObj(self.buildObject(objid))

            ai_spec = importlib.util.spec_from_file_location(ai_filename,'teams/'+teamName+"/"+ai_filename)
            ai_module = importlib.util.module_from_spec(ai_spec)
            ai_spec.loader.exec_module(ai_module)

            _agent.setAI(ai_module.AI())

            
        else:
            LogError("SIM: Agent is None")

    def getObject(self,ID):
        return copy.deepcopy(self.objectDict[ID])

    def getMap(self,ID):
        return copy.deepcopy(self.mapDict[ID])

    def getTeam(self,key):
        return copy.deepcopy(self.teamDict[key])


    def getTeamNames(self):
        return list(self.teamDict.keys())
    def getMapNames(self):
        return list(self.mapDict.keys())

    def runSim(self):
        pass
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
        self.mapInPlay = None


    def addObject(self,_obj):
        key = _obj.getData('id')
        if key != None:
            self.objectDict[key]=_obj

    def addComponent(self,comp):
        key = comp.getData('id')
        if key != None:
            self.componentDict[key] = comp
        else:
            print("Sim: Adding component, comp has not data member id.")

    def addMap(self,_map):
        key = _map.getData('name')
        if key != None:
            self.mapDict[key] = _map
        else:
            LogError("LOADER: Map has no name.")

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

            return _obj
        else:
            print("Obj key "+key+" not in dict")
            return None

    def buildComponent(self,key):
        if key in self.componentDict:
            comp = copy.deepcopy(self.componentDict[key])

            return comp
        else:
            print("Comp "+str(key)+" not in comp dict.")
            return None

    def clearTeamsInPlay(self):
        self.teamsInPlay.clear()
    

    def buildTeam(self,key):
        if key in self.teamDict:
            _team = self.getTeamCopy(key)

            teamName = _team.getData('name')
            _agents = _team.getData('agents')
            for k,v in _agents.items():
                self.buildAgent(v,teamName)

            self.teamsInPlay[key]=_team

    def buildAgent(self,_agent,teamName):
        if _agent != None:
            objid = _agent.getData('objid')
            ai_filename = _agent.getData('ai_filename')
            _agent.setObj(self.buildObject(objid))


            print(ai_filename,'teams/'+teamName+"/"+ai_filename)
            ai_spec = importlib.util.spec_from_file_location(ai_filename,'teams/'+teamName+"/"+ai_filename)
            ai_module = importlib.util.module_from_spec(ai_spec)
            ai_spec.loader.exec_module(ai_module)

            _agent.setAI(ai_module.AI(teamName,self.getSimProfile(),_agent.getObjProfile()))

            #self.mapInPlay.addAgentObject(_agent.getObj())
            
        else:
            LogError("SIM: Agent is None")

    def getObject(self,ID):
        return copy.deepcopy(self.objectDict[ID])

    def getMapCopy(self,ID):
        if ID in self.mapDict:
            return copy.deepcopy(self.mapDict[ID])
        else:
            return None

    def getMap(self,ID):
        if ID in self.mapDict:
            return self.mapDict[ID]
        else:
            return None

    def getTeam(self,key):
        if key in self.teamDict:
            return self.teamDict[key]
        else:
            return None

    def getTeamCopy(self,key):
        if key in self.teamDict:
            return copy.deepcopy(self.teamDict[key])
        else:
            return None

    def getTeamNames(self):
        return list(self.teamDict.keys())
    def getMapNames(self):
        return list(self.mapDict.keys())


    def getSimProfile(self):
        simdata = {}
        simdata['map_name']=self.mapInPlay.getData('name')
        simdata['map_width']=self.mapInPlay.getData('width')
        simdata['map_height']=self.mapInPlay.getData('height')
        return simdata

    def setMapInPlay(self,name):
        self.mapInPlay = self.getMapCopy(name)
        if self.mapInPlay != None:
            self.mapInPlay.generateMap(self)

    def isMapReady(self):
        return self.mapInPlay != None

    def runSim(self):
        pass
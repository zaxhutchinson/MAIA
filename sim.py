import importlib

import obj
import copy
import zmap
import comp
import vec2
import loader
#from log import *

class Sim:
    def __init__(self):
        self.map = None
        self.sides={}
    def reset(self):
        self.map=None
        self.sides={}

    ##########################################################################
    # MAP
    def setMap(self,_map):
        self.map = _map
        sides = self.map.getData('sides')
        for k,v in sides.items():
            self.addSide(k,v)
    def getMap(self):
        return self.map
    def hasMap(self):
        return self.map!=None

    ##########################################################################
    # SIDES
    def addSideID(self,ID):
        self.sides[ID]=None
    def addSide(self,ID,side):
        self.sides[ID]=side
        self.sides[ID]['team']=None
    def getSides(self):
        return self.sides
    
    ##########################################################################
    # TEAMS
    def addTeam(self,ID,team):
        self.sides[ID]['team']=team
    def getTeam(self,ID):
        return self.sides[ID]['team']
    def delTeam(self,ID):
        self.sides[ID]['team']=None


    ##########################################################################
    # BUILD SIM
    def buildSim(self):
        pass

    ##########################################################################
    # RUN SIM
    def runSim(self):
        pass



    # def addObject(self,_obj):
    #     key = _obj.getData('id')
    #     if key != None:
    #         self.objectDict[key]=_obj

    # def addComponent(self,comp):
    #     key = comp.getData('id')
    #     if key != None:
    #         self.componentDict[key] = comp
    #     else:
    #         print("Sim: Adding component, comp has not data member id.")

    # def addMap(self,_map):
    #     key = _map.getData('name')
    #     if key != None:
    #         self.mapDict[key] = _map
    #     else:
    #         LogError("LOADER: Map has no name.")

    # def addTeam(self,team):
    #     key = team.getData('name')
    #     if key != None:
    #         self.teamDict[key]=team


    # def buildObject(self,key):
    #     if key in self.objectDict:
    #         _obj = copy.deepcopy(self.objectDict[key])

    #         comps = _obj.getData('component_ids')
    #         if comps != None:
                
    #             for c in comps:
    #                 newComp = self.buildComponent(c)
    #                 _obj.addComponent(newComp)

    #         return _obj
    #     else:
    #         print("Obj key "+str(key)+" not in dict")
    #         return None

    # def buildComponent(self,key):
    #     if key in self.componentDict:
    #         comp = copy.deepcopy(self.componentDict[key])

    #         return comp
    #     else:
    #         print("Comp "+str(key)+" not in comp dict.")
    #         return None

    # def clearTeamsInPlay(self):
    #     self.teamsInPlay.clear()
    
    # def buildSim(self, teams):
    #     if self.isMapReady():
    #         self.clearTeamsInPlay()
    #         for k,v in teams.items():
    #             if v == None:
    #                 return (False,"Team " + str(k) + " is None.")
    #             else:
    #                 self.buildTeam(k,v)
    #         return (True,"OK")
    #     else:
    #         return (False, "Map isn't ready.")

    # def buildTeam(self,side_key,team_key):
    #     if team_key in self.teamDict:
    #         _team = self.getTeamCopy(team_key)

    #         teamName = _team.getData('name')
    #         _agents = _team.getData('agents')


    #         starting_regions = self.mapInPlay.getData('starting_regions')
    #         starting_region = None
    #         if side_key in starting_regions:
    #             starting_region = starting_regions[side_key]
    #         else:
    #             LogError("Side key "+side_key+" not in starting regions.")

    #         for k,v in _agents.items():
    #             pos = self.buildAgent(v,teamName,starting_region)
                
    #         for k,v in _agents.items():
    #             for k2,v2 in _agents.items():
    #                 if k == k2:
    #                     continue
    #                 else:
    #                     if v.getData('obj').collidesWith(v2):
    #                         LogError('Team: '+teamName+" agents "+k+" and "+k2+" have selected colliding starting positions of" +\
    #                             str(v.getData('obj').getData('pos')) + " and " + str(v2.getData('obj').getData('pos')))


    #         self.teamsInPlay[side_key]=_team

    # def buildAgent(self,_agent,teamName,starting_region):
    #     if _agent != None:
    #         objid = _agent.getData('objid')
    #         ai_filename = _agent.getData('ai_filename')
    #         _agent.setData('obj',self.buildObject(objid))

            
    #         ai_spec = importlib.util.spec_from_file_location(ai_filename,'teams/'+teamName+"/"+ai_filename)
    #         ai_module = importlib.util.module_from_spec(ai_spec)
    #         ai_spec.loader.exec_module(ai_module)

    #         ai = ai_module.AI()
            
    #         pos = ai.initData(teamName,self.getSimProfile(), starting_region)

    #         if type(pos) != tuple and type(pos) != list:
    #             LogError("Team: "+teamName+" - Agent: "+ai_filename+" did not return a tuple or list from initData().")
    #             return None
    #         try:
    #             pos_vec2 = vec2.Vec2(pos[0],pos[1])
    #         except:
    #             LogError("Team: "+teamName+" - Agent: "+ai_filename+" initData() returned a list or tuple of something other than int/float for its starting location.")
    #             return None

    #         if pos[0] < starting_region['left'] or pos[0] >= starting_region['right'] or \
    #             pos[1] < starting_region['top'] or pos[1] >= starting_region['bottom']:
    #             LogError("Team: "+teamName+" - Agent: "+ai_filename+" starting location is outside the starting region.")
    #             return None

    #         _agent.getData('obj').setPosition(pos_vec2)

    #         _agent.setData('ai',ai)

    #         return pos_vec2

    #         #self.mapInPlay.addAgentObject(_agent.getObj())
            
    #     else:
    #         LogError("SIM: Agent is None")

    # def getObject(self,ID):
    #     return copy.deepcopy(self.objectDict[ID])

    # def getMapCopy(self,ID):
    #     if ID in self.mapDict:
    #         return copy.deepcopy(self.mapDict[ID])
    #     else:
    #         return None

    # def getMap(self,ID):
    #     if ID in self.mapDict:
    #         return self.mapDict[ID]
    #     else:
    #         return None

    # def getTeam(self,key):
    #     if key in self.teamDict:
    #         return self.teamDict[key]
    #     else:
    #         return None

    # def getTeamCopy(self,key):
    #     if key in self.teamDict:
    #         return copy.deepcopy(self.teamDict[key])
    #     else:
    #         return None

    # def getTeamNames(self):
    #     return list(self.teamDict.keys())
    # def getMapNames(self):
    #     return list(self.mapDict.keys())


    # def getSimProfile(self):
    #     simdata = {}
    #     simdata['map_name']=self.mapInPlay.getData('name')
    #     simdata['map_width']=self.mapInPlay.getData('width')
    #     simdata['map_height']=self.mapInPlay.getData('height')
    #     return simdata

    # def setMapInPlay(self,name):
    #     self.mapInPlay = self.getMapCopy(name)
    #     if self.mapInPlay != None:
    #         self.mapInPlay.generateMap(self)

    # def isMapReady(self):
    #     return self.mapInPlay != None


    # def runSim(self):
    #     self.simData = {}
    #     self.simData['tick'] = 0
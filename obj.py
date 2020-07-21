import random
import math

import vec2
import line
import log

_2PI = 2.0*math.pi

class Object:
    def __init__(self,data):
        self.data = {}
        self.data['id']=data['id']
        self.data['objname']=data['objname']
        self.data['text']=data['text']
        self.data['color']=data['color']
        self.data['health']=data['health']
        self.data['damage']=0.0
        self.data['facing']=0.0
        self.data['density']=data['density']
        self.data['x']=0
        self.data['y']=0
        self.data['cell_x']=0.5
        self.data['cell_y']=0.5
        self.data['comp_ids']=data['comp_ids']
        self.data['comps']={}
        self.data['uuid']=None
        self.data['ai']=None
        self.data['alive']=True
        self.data['teamname']=None
        self.data['callsign']=None
        self.data['squad']=None
        
        self.view_keys = [
            'health','damage','facing','x','y','cell_x','cell_y','objname','teamname',
            'callsign','squad'
        ]

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None
    def setData(self,key,val):
        self.data[key]=val

    def addComp(self,comp):
        next_id = str(len(self.data['comps']))
        comp.setData('slot_id',next_id)
        self.data['comps'][next_id]=comp

    def place(self,data):
        for k,v in data.items():
            self.data[k]=v

    def update(self,view):
        try:
            if self.data['ai'] != None:
                view['self']=self.getSelfView()
                return self.data['ai'].runAI(view)
            else:
                return None
        except Exception as e:
            log.LogMostRecentException(
                "AI script for team "+
                self.getData('teamname') +
                " agent " + self.getData('callsign') +
                " raised the exception: " + str(e)

            )

    def damageObj(self,amt):
        # Add damage to current total
        new_damage = self.getData('damage') + amt
        self.setData('damage',new_damage)

        # If damage is greater than health
        if new_damage >= self.getData('health'):
            self.setData('alive',False)

    def getDrawData(self):
        return {
            'x':self.getData('x'),'y':self.getData('y'),
            'text':self.getData('text'), 'fill':self.getData('color')
        }


    def processCommands(self,cmds):
        actions = []

        # Find number of commands that can be ordered.
        max_cmds = 0
        for comp in self.getData('comps').values():
            if comp.getData('ctype')=='CnC':
                max_cmds += comp.getData('max_cmds_per_tick')

        for compid,cmd in cmds.items():
            
            # Check and reduce commands remaining
            # Having this outside the if-statment below
            # means that even badly formed commands count.
            if max_cmds==0:
                break
            else:
                max_cmds-=1

            if compid in self.data['comps']:
                comp_actions = self.data['comps'][compid].Update(cmd)
                actions += comp_actions
            

        return actions


    def getSelfView(self):
        view = {}
        
        for key in self.view_keys:
            view[key]=self.getData(key)

        comp_view = {}
        for k,v in self.getData('comps').items():
            comp_view[k]=v.getSelfView()
        view['comps']=comp_view

        return view

    def getBestDisplayName(self):
        if self.data['callsign'] != None:
            return self.data['callsign']
        else:
            return self.data['objname']
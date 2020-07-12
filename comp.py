import math

import vec2
from log import *
import action

class Comp:
    def __init__(self,data):
        self.data=data

        self.Update = None

        ctype = self.data['ctype']
        if ctype=='FixedGun':
            self.Update = self.FixedGunUpdate
        elif ctype=='Engine':
            self.Update = self.EngineUpdate
        elif ctype=='Scanner':
            self.Update = self.ScannerUpdate
        else:
            self.Update = self.NoUpdate

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None
    def setData(self,key,value):
        self.data[key]=value

    ###########################################################################
    # Default Update: does nothing.
    #   Intended for use in comps that never produce actions
    def NoUpdate(self,cmd):
        return []

    ###########################################################################
    # FixedGun Update:
    #   Commands: FIRE, RELOAD
    def FixedGunUpdate(self, cmd):

        actions = []

        # See if we were reloading
        self.updateReloading()        

        if 'command' in cmd:
            if cmd['command']=='FIRE':

                if self.isLoaded():
                    # Reset the reload ticks
                    self.setReloadTicksToFull()

                    a = action.Action()
                    a.setType('HIGHSPEED_PROJECTILE')
                    a.addData('compname',self.getData('name'))
                    a.addData('direction',self.getData('parent').getData('facing'))
                    a.addData('min_damage',self.getData('min_damage'))
                    a.addData('max_damage',self.getData('max_damage'))
                    a.addData('range',self.getData('range'))
                    actions.append(a)

            elif cmd['command']=='RELOAD':
                
                if not self.data['reloading'] and not self.isLoaded():
                    self.data['reloading']=True

        return actions


    ###########################################################################
    # Engine Update:
    def EngineUpdate(self, cmd):
        
        actions = []

        if 'command' in cmd:

            if cmd['command']=='SET_SPEED':

                if 'speed' in cmd:
                    newspeed = cmd['speed']
                    if newspeed >= self.getData('min_speed') and newspeed <= self.getData('max_speed'):
                        self.data['cur_speed']=newspeed

            elif cmd['command']=='SET_TURNRATE':
                if 'turnrate' in cmd:
                    newturnrate = cmd['data']['turnrate']
                    if abs(newturnrate) <= self.getData('max_turnrate'):
                        self.data['cur_turnrate']=newturnrate



        if self.isMoving():
            a = action.Action()
            a.setType('MOVE')
            a.addData('direction',self.getData('parent').getData('facing'))
            a.addData('speed',self.getData('cur_speed'))
            actions.append(a)
        
        if self.isTurning():
            a = action.Action()
            a.setType('TURN')
            a.addData('turnrate',self.getData('cur_turnrate'))
            actions.append(a)

        return actions

    ###########################################################################
    # Scanner Update
    def ScannerUpdate(self, cmd):

        actions = []

        if 'command' in cmd:
            if cmd['command']=='ACTIVATE':
                self.setData('active',True)
            elif cmd['command']=='DEACTIVATE':
                self.setData('active',False)

        if self.isScanning():
            a = action.Action()
            a.setType('SCAN')
            a.addData('compname',self.getData('name'))
            a.addData('range',self.getData('range'))
            a.addData('x',self.getData('parent').getData('x'))
            a.addData('y',self.getData('parent').getData('y'))
            facing = self.getData('parent').getData('facing')+self.getData('offset_angle')
            a.addData('facing',facing)
            a.addData('level',self.getData('level'))
            a.addData('visarc',self.getData('visarc'))
            a.addData('offset_angle',self.getData('offset_angle'))
            a.addData('resolution',self.getData('resolution'))
            actions.append(a)

        return actions


    ###########################################################################
    ## WEAPON RELATED FUNCTIONS
    def setReloadTicksToFull(self):
        self.data['reload_ticks_remaining']=self.data['reload_ticks']
    def isLoaded(self):
        return self.data['reload_ticks_remaining']==0
    def updateReloading(self):
        if self.data['reloading']:
            if self.data['reload_ticks_remaining'] > 0:
                self.data['reload_ticks_remaining'] -= 1
                if self.data['reload_ticks_remaining']==0:
                    self.data['reloading']=False


    ###########################################################################
    ## ENGINE RELATED FUNCTIONS
    def isMoving(self):
        return self.data['cur_speed'] != 0.0
    def isTurning(self):
        return self.data['cur_turnrate']!=0.0



    ###########################################################################
    ## SCANNER RELATED FUCNTIONS
    def isScanning(self):
        return self.getData('active')
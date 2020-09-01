import math

import vec2
from log import *
import action

class Comp:
    def __init__(self,data):
        self.data=data

        self.Update = self.NoUpdate
        self.view_keys = []
        self.setViewKeysBasic()

        ctype = self.data['ctype']
        if ctype=='FixedGun':
            self.Update = self.FixedGunUpdate
            self.setViewKeysFixedGun()
        elif ctype=='Engine':
            self.Update = self.EngineUpdate
            self.setViewKeysEngine()
        elif ctype=='Radar':
            self.Update = self.RadarUpdate
            self.setViewKeysRadar()
        elif ctype=='CnC':
            self.Update = self.CnCUpdate
            self.setViewKeysCnC()
        elif ctype=='Radio':
            self.Update = self.RadioUpdate
            self.setViewKeysRadio()
        elif ctype=='Arm':
            self.Update = self.ArmUpdate
            self.setViewKeysArm()


    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None
    def setData(self,key,value):
        self.data[key]=value
    
    ###########################################################################
    # Self View dispatch
    def setViewKeysBasic(self):
        self.view_keys += [
            'id','ctype','name','slot_id'
        ]
    def setViewKeysFixedGun(self):
        self.view_keys += [
            'reload_ticks','reload_ticks_remaining','reloading',
            'ammunition','min_damage','max_damage','range'
        ]
    def setViewKeysEngine(self):
        self.view_keys += [
            'min_speed','max_speed','cur_speed','max_turnrate','cur_turnrate'
        ]
    def setViewKeysRadar(self):
        self.view_keys += [
            'active','range','level','visarc','offset_angle','resolution'
        ]
    def setViewKeysCnC(self):
        self.view_keys += [
            'max_cmds_per_tick'
        ]
    def setViewKeysRadio(self):
        self.view_keys += [
            'range'
        ]
    def setViewKeysArm(self):
        self.view_keys += [
            'max_bulk', 'max_weight', 'item'
        ]

    def getSelfView(self):
        view = {}
        for key in self.view_keys:
            view[key] = self.getData(key)
        return view

    ##########################################################################
    # UPDATE METHODS
    ##########################################################################

    ###################################
    # Default Update: does nothing.
    #   Intended for use in comps that never produce actions
    def NoUpdate(self,cmd):
        return []

    ###################################
    # FixedGun Update:
    #   Commands: FIRE, RELOAD
    def FixedGunUpdate(self, cmd):

        actions = []

        if 'command' in cmd:
            if cmd['command']=='FIRE':

                if self.isLoaded():
                    # Reset the reload ticks
                    self.setReloadTicksToFull()

                    a = action.Action()
                    a.setType('HIGHSPEED_PROJECTILE')
                    a.addData('slot_id',self.getData('slot_id'))
                    a.addData('compname',self.getData('name'))
                    a.addData('direction',self.getData('parent').getData('facing'))
                    a.addData('min_damage',self.getData('min_damage'))
                    a.addData('max_damage',self.getData('max_damage'))
                    a.addData('range',self.getData('range'))
                    actions.append(a)

            elif cmd['command']=='RELOAD':
                
                # We can reload if we aren't reloading,
                #   we are not currently loaded
                #   and we have ammo left.
                if not self.data['reloading'] and not self.isLoaded() and self.getData('ammunition')>0:
                    self.data['reloading']=True

        # See if we were reloading
        self.updateReloading() 

        return actions


    ###################################
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
                    newturnrate = cmd['turnrate']
                    if abs(newturnrate) <= self.getData('max_turnrate'):
                        self.data['cur_turnrate']=newturnrate



        if self.isMoving():
            a = action.Action()
            a.setType('MOVE')
            a.addData('slot_id',self.getData('slot_id'))
            a.addData('direction',self.getData('parent').getData('facing'))
            a.addData('speed',self.getData('cur_speed'))
            actions.append(a)
        
        if self.isTurning():
            a = action.Action()
            a.setType('TURN')
            a.addData('slot_id',self.getData('slot_id'))
            a.addData('turnrate',self.getData('cur_turnrate'))
            actions.append(a)

        return actions

    ###################################
    # Radar Update
    def RadarUpdate(self, cmd):

        actions = []
        # if 'command' in cmd:
        #     if cmd['command']=='ACTIVATE':
        #         self.setData('active',True)
        #     elif cmd['command']=='DEACTIVATE':
        #         self.setData('active',False)

        if 'command' in cmd:
            if cmd['command']=='TRANSMIT_RADAR':
                a = action.Action()
                a.setType('TRANSMIT_RADAR')
                a.addData('slot_id',self.getData('slot_id'))
                a.addData('compname',self.getData('name'))
                a.addData('ctype',self.getData('ctype'))
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

    ##################################
    # CnC Udpate
    def CnCUpdate(self,cmd):
        return []

    ###################################
    # Radio Update
    def RadioUpdate(self,cmd):
        actions = []

        if 'command' in cmd:
            if cmd['command']=='BROADCAST' and 'message' in cmd:
                a = action.Action()
                a.setType('BROADCAST')
                a.addData('slot_id',self.getData('slot_id'))
                a.addData('message',cmd['message'])
                a.addData('range',self.getData('cur_range'))
                actions.append(a)

            elif cmd['command']=='SET_RANGE' and 'range' in cmd:
                newrange = cmd['range']
                if 0 <= newrange <= self.getData('max_range'):
                    self.setData('cur_range',newrange)
        

        return actions

    ###################################
    # Arm Update
    def ArmUpdate(self,cmd):
        actions = []

        if 'command' in cmd:
            if cmd['command']=='TAKE_ITEM':
                a = action.Action()
                a.setType('TAKE_ITEM')
                a.addData('slot_id',self.getData('slot_id'))

                if 'item_name' in cmd:
                    a.addData('item_name',cmd['item_name'])
                else:
                    a.addData('item_name',None)
                
                if 'item_index' in cmd:
                    a.addData('item_index',cmd['item_index'])
                else:
                    a.addData('item_index',None)

                if 'item_uuid' in cmd:
                    a.addData('item_uuid',cmd['item_uuid'])
                else:
                    a.addData('item_uuid',None)

                if 'location' in cmd:
                    a.addData('location', cmd['location'])
                else:
                    a.addData('location',None)

                actions.append(a)

            elif cmd['command']=='DROP_ITEM':
                a = action.Action()
                a.setType('DROP_ITEM')
                a.addData('slot_id',self.getData('slot_id'))
                a.addData('location',cmd['location'])
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
            else:
                self.data['reloading']=False


    ###########################################################################
    ## ENGINE RELATED FUNCTIONS
    def isMoving(self):
        return self.data['cur_speed'] != 0.0
    def isTurning(self):
        return self.data['cur_turnrate']!=0.0



    ###########################################################################
    ## RADAR RELATED FUCNTIONS
    def isTransmitting(self):
        return self.getData('active')


    ###########################################################################
    ## ARM RELATED FUNCTIONS
    def isHoldingItem(self):
        return self.getData('item')!=None
    def canTakeItem(self,weight,bulk):
        return self.getData('max_weight') >= weight and self.getData('max_bulk') >= bulk

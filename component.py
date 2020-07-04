import math

import vec2
from log import *

# COMPONENT TYPES
#   'WEAPON' = can be fired.

class Projectile:
    def __init__(self,owner,damage,velocity,heading):
        self.owner = owner
        self.damage = damage
        self.velocity = velocity
        self.position = owner.getData('pos')
        self.heading = heading

class Component:
    def __init__(self,data,parent=None):
        self.parent = parent
        self.required_data = []
        self.data = {}
        print("COMPONENT setData()")

        # Fill out self.data with None values
        req_data = [
            'id','name','ctype'
        ]
        
        # Populate with actual data.
        for rd in req_data:
            if rd in data:
                self.data[rd] = data[rd]
            else:
                self.data[rd]=None
                self.LogMissingData(rd)

        self.required_data += req_data
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            print("Component: getData() key "+str(key)+" does not exist.")
            return None

    def update(self,time,command):
        return None
    def getHeading(self):
        return self.parent.heading
    def LogMissingData(self,rd):
        LogError("COMP is missing "+rd)
    # Will update when component destruction can happen
    def isAlive(self):
        return True
    
class FixedGun(Component):
    def __init__(self,data,parent=None):
        super().__init__(data,parent)
        print("FIXEDGUN setData()")

        self.data['prev_update_time'] = 0.0
        self.data['reload_timer']=0.0

        local_data = [
            'reload_duration','ammunition','damage','velocity'
        ]
        for rd in local_data:
            self.data[rd] = None

        for rd in local_data:
            if rd in data:
                self.data[rd]=data[rd]
            else:
                self.LogMissingData(rd)

        self.required_data += local_data

    
    def update(self,time,command):
        # Update timers
        if self.data['reload_timer'] > 0.0:
            self.data['reload_timer'] -= (time - self.data['prev_update_time'])
            if self.data['reload_timer'] < 0.0:
                self.data['reload_timer'] = 0.0
        self.data['prev_update_time'] = time

        rtn = None
        if not self.parent.isAlive() or not self.isAlive():
            rtn = None
        elif command == None:
            rtn = None
        elif command['name'] == 'FIRE':
            if self.data['ammunition'] > 0 and self.data['reload_timer'] <= 0.0:
                self.data['reload_timer'] = self.data['reload_duration']
                self.data['ammunition'] -= 1
                p = Projectile(
                    self.parent,self.data['damage'],
                    self.data['velocity'],self.getHeading()
                )
                rtn = ('PROJECTILE',p)

        return rtn

class Engine(Component):
    def __init__(self,data,parent=None):
        super().__init__(data,parent)
        
        self.data['throttle']=0.0
        self.data['turn']=0.0

        local_data = [
            'speed','turn_rate'
        ]
            
        for rd in local_data:
            if rd in data:
                self.data[rd]=data[rd]
            else:
                self.data[rd]=None
                self.LogMissingData(rd)

        self.required_data += local_data

    def update(self,time,command):

        rtn = None
        if not self.parent.isAlive() or not self.isAlive():
            rtn = None
        elif command == None:
            rtn = None
        elif command['name'] == 'TURN':
            self.data['turn'] = min(max(command['value'],-1.0),1.0)
        elif command['name'] == 'THROTTLE':
            self.data['throttle'] = min(max(command['value'],-1.0),1.0)
        

        distance = self.data['speed']*self.data['throttle']
        self.parent.move(distance)

        turn = self.data['turn_rate']*math.radians(self.data['turn'])
        self.parent.turn(turn)

    
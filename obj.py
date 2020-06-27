import random
import math

import vec2
import line
from log import *

_2PI = 2.0*math.pi

class Shape:
    def __init__(self,name):
        self.name = name
    def collision(self,pos,line):
        return False
    def randomize(self):
        None
    def setData(self,data):
        pass

class Cylinder(Shape):
    def __init__(self,name,radius):
        super().__init__(name)
        self.radius=radius
    def collision(self,pos,line):
        return self.radius >= pos.distanceToLine(line)
    def randomize(self):
        pass
    def setData(self,data):
        if 'radius' in data:
            self.radius = data['radius']

class Rectangle(Shape):
    def __init__(self,name,width,height):
        super().__init__(name)
        self.width=width
        self.height=height
        self.half_width = width/2.0
        self.half_height = height/2.0
    def TopLeft(self,pos,rotation):
        x = pos.getX() - self.half_width
        y = pos.getY() - self.half_height
        return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    def TopRight(self,pos,rotation):
        x = pos.getX() + self.half_width
        y = pos.getY() - self.half_height
        return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    def BottomLeft(self,pos,rotation):
        x = pos.getX() - self.half_width
        y = pos.getY() + self.half_height
        return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    def BottomRight(self,pos,rotation):
        x = pos.getX() + self.half_width
        y = pos.getY() + self.half_height
        return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    def collision(self,pos,rotation,l):
        tl = self.TopLeft(pos,rotation)
        tr = self.TopRight(pos,rotation)
        bl = self.BottomLeft(pos,rotation)
        br = self.BottomRight(pos,rotation)
        top = line.LineSeg(tl,tr)
        bottom = line.LineSeg(bl,br)
        left = line.LineSeg(tl,bl)
        right = line.LineSeg(tr,br)
        return l.intersectsLineSeg(top) or \
            l.intersectsLineSeg(bottom) or \
            l.intersectsLineSeg(left) or \
            l.intersectsLineSeg(right)

    def randomize(self):
        self.rotation = random.uniform(0.0,2.0*math.pi)
    def setData(self,data):
        if 'width' in data:
            self.width = data['width']
            self.half_width = self.width / 2.0
        if 'height' in data:
            self.height = data['height']
            self.half_height = self.height / 2.0
        if 'rotation' in data:
            self.rotation = data['rotation']


class Object:
    def __init__(self,data,shape):

        self.data = {}
        self.data['shape']=shape
        self.data['pos']=vec2.Vec2(0.0,0.0)
        self.data['components']={}
        self.required_data = []
        self.setData(data)
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def setData(self,data):
        req_data = [
            'id','name','health','damage','heading'
        ]
            

        for rd in req_data:
            if rd in data:
                self.data[rd] = data[rd]
            else:
                self.data[rd]=None
                self.LogMissingData(rd)

        self.required_data += req_data

        opt_data = [
            'component_ids'
        ]
        for od in opt_data:
            if od in data:
                self.data[od] = data[od]
                self.required_data.append(od)

    def LogMissingData(self,rd):
        LogError("Comp is missing "+rd)
    def getCurrentHealth(self):
        return self.data['health'] - self.data['damage']
    def addDamage(self,amt):
        self.data['damage'] += amt
    def isAlive(self):
        return True if (self.getCurrentHealth() > 0) else False
    def setPosition(self,vec):
        self.data['pos']=vec
    def getPosition(self):
        return self.data['pos']
    def turn(self,angle):
        self.data['heading'] += angle
        if self.data['heading'] < 0.0:
            self.data['heading'] += _2PI
        elif self.data['heading'] > _2PI:
            self.data['heading'] -= _2PI
    def move(self,distance):
        self.data['pos'].move(self.data['heading'],distance)
    def collidesWithMe(self,line):
        return self.data['shape'].collision(self.data['pos'],self.data['heading'],line)
    def randomize(self):
        self.data['shape'].randomize()

    def setDataFromDict(self,data):
        for k,v in data:
            if k in self.data:
                self.data[k]=v
        self.shape.setData(data)


    def addComponent(self,comp):
        comp_id = comp.getData('id')
        if comp_id in self.data['components']:
            self.data['components'][comp_id].append(comp)
        else:
            self.data['components'][comp_id]=[comp]

        




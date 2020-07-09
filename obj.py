import random
import math

import vec2
import line
from log import *

_2PI = 2.0*math.pi

class Shape:
    def __init__(self,data):
        self.data={}
        self.data['name'] = data['name']
        self.data['pos'] = None
        self.data['heading'] = None
    def collision(self,line):
        return False
    def randomize(self):
        None
    def setData(self,key,val):
        self.data[key]=val
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def turn(self,angle):
        self.data['heading'] += angle
        if self.data['heading'] < 0.0:
            self.data['heading'] += _2PI
        elif self.data['heading'] > _2PI:
            self.data['heading'] -= _2PI
    def move(self,distance):
        self.data['pos'].move(self.data['heading'],distance)

    def collidesWith(self,other):
        if isinstance(other,line.LineSeq):
            return self.collidesWithLineSeg(other)
        elif isinstance(other,vec2.Vec2):
            return self.collidesWithPoint(other)
        else:
            return self.collidesWithShape(other)

    def collidesWithPoint(self,point):
        return self.data['pos'] == point
    def collidesWithLineSeg(self,lineseg):
        return self.data['pos'].intersectsLineSeg(lineseg)
    def collidesWithShape(self,shape):
        return shape.collidesWithPoint(self.data['pos'])


class Cylinder(Shape):
    def __init__(self,data):
        super().__init__(data)
        self.radius = data['radius']
    def collidesWithPoint(self,point):
        return self.data['radius'] >= self.data['pos'].distanceToPoint(point)
    def collidesWithLineSeg(self,lineseg):
        return self.data['radius'] >= self.data['pos'].distanceToLineSeg(lineseg)
    def collidesWithShape(self,shape):
        return self.collidesWithPoint(shape.getData('pos'))
            

# class Rectangle(Shape):
#     def __init__(self,name,width,height):
#         super().__init__(name)
#         self.width=width
#         self.height=height
#         self.half_width = width/2.0
#         self.half_height = height/2.0
#     def TopLeft(self,pos,rotation):
#         x = pos.getX() - self.half_width
#         y = pos.getY() - self.half_height
#         return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
#     def TopRight(self,pos,rotation):
#         x = pos.getX() + self.half_width
#         y = pos.getY() - self.half_height
#         return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
#     def BottomLeft(self,pos,rotation):
#         x = pos.getX() - self.half_width
#         y = pos.getY() + self.half_height
#         return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
#     def BottomRight(self,pos,rotation):
#         x = pos.getX() + self.half_width
#         y = pos.getY() + self.half_height
#         return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
#     def collision(self,pos,rotation,l):
#         tl = self.TopLeft(pos,rotation)
#         tr = self.TopRight(pos,rotation)
#         bl = self.BottomLeft(pos,rotation)
#         br = self.BottomRight(pos,rotation)
#         top = line.LineSeg(tl,tr)
#         bottom = line.LineSeg(bl,br)
#         left = line.LineSeg(tl,bl)
#         right = line.LineSeg(tr,br)
#         return l.intersectsLineSeg(top) or \
#             l.intersectsLineSeg(bottom) or \
#             l.intersectsLineSeg(left) or \
#             l.intersectsLineSeg(right)

#     def randomize(self):
#         self.rotation = random.uniform(0.0,2.0*math.pi)
#     def setData(self,data):
#         if 'width' in data:
#             self.width = data['width']
#             self.half_width = self.width / 2.0
#         if 'height' in data:
#             self.height = data['height']
#             self.half_height = self.height / 2.0
#         if 'rotation' in data:
#             self.rotation = data['rotation']


class Object:
    def __init__(self,data):


        self.data = {}
        self.data['shape']=data['shape']
        self.data['components']={}
        self.data['damage']=0.0
        self.required_data = []


        req_data = [
            'id','name','health','heading'
        ]
            

        for rd in req_data:
            if rd in data:
                self.data[rd] = data[rd]
            else:
                self.data[rd]=None
                self.LogMissingData(rd)

        self.required_data += req_data

        opt_data = [
            'component_ids','damage'
        ]
        for od in opt_data:
            if od in data:
                self.data[od] = data[od]
                self.required_data.append(od)

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None
    def setData(self,key,val):
        self.data[key]=val

    # SHAPE PASS THROUGH FUNCTIONS
    def move(self,distance):
        self.data['shape'].move(distance)
    def turn(self,angle):
        self.data['shape'].turn(angle)
    def collidesWith(self,other):
        return self.data['shape'].collidesWith(other)
    def setPosition(self,pos):
        self.data['shape'].setData('pos',pos)


    def LogMissingData(self,rd):
        LogError("Object is missing "+rd)
    def getCurrentHealth(self):
        return self.data['health'] - self.data['damage']
    def addDamage(self,amt):
        self.data['damage'] += amt
    def isAlive(self):
        return True if (self.getCurrentHealth() > 0) else False

    def initObjectFromData(self,data):
        for k,v in data.items():
            if k in self.data:
                if k == 'pos':
                    self.data['pos'] = vec2.Vec2(v[0],v[1])
                else:
                    self.data[k]=v


    def addComponent(self,comp):
        comp_id = comp.getData('id')
        if comp_id in self.data['components']:
            self.data['components'][comp_id].append(comp)
        else:
            self.data['components'][comp_id]=[comp]

        
    def getObjProfile(self):
        obj_prof = {}
        obj_prof['shape_name']=self.getData('name')
        obj_prof['loc_x']=self.getData('pos').getX()
        obj_prof['loc_y']=self.getData('pos').getY()
        return obj_prof



import random
import math

import vec2
import line
from log import *

_2PI = 2.0*math.pi

class Shape:
    def __init__(self,name):
        self.data={}
        self.data['name'] = name
        self.data['heading']=0.0
        self.data['x']=0
        self.data['y']=0

    def setData(self,key,val):
        self.data[key]=val
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def place(self,data):
        if 'x' in data:
            self.data['x']=data['x']
        if 'y' in data:
            self.data['y']=data['y']
        if 'heading' in data:
            self.data['heading']=data['heading']


    def turn(self,angle):
        self.data['heading'] += angle
        if self.data['heading'] < 0.0:
            self.data['heading'] += _2PI
        elif self.data['heading'] > _2PI:
            self.data['heading'] -= _2PI
    def move(self,distance):
        self.data['pos'].move(self.data['heading'],distance)

    def collidesWith(self,other):
        if isinstance(other,line.LineSeg):
            return self.collidesWithLineSeg(other)
        elif isinstance(other,vec2.Vec2):
            return self.collidesWithPoint(other)
        elif isinstance(other,Circle):
            return self.collidesWithCylinder(other)

    def collidesWithPoint(self,point):
        return self.data['pos'] == point
    def collidesWithLineSeg(self,lineseg):
        return self.data['pos'].intersectsLineSeg(lineseg)
    def collidesWithCylinder(self,shape):
        return shape.collidesWithPoint(self.data['pos'])


class Circle(Shape):
    def __init__(self,data):
        super().__init__(data)
        self.data['radius']=1.0
    def place(self,data):
        super().place(data)
        if 'radius' in data:
            self.data['radius']=data['radius']
    def collidesWithPoint(self,point):
        return self.data['radius'] >= self.data['pos'].distanceToPoint(point)
    def collidesWithLineSeg(self,lineseg):
        return self.data['radius'] >= self.data['pos'].distanceToLineSeg(lineseg)
    def collidesWithCylinder(self,shape):
        return self.collidesWithPoint(shape.getData('pos'))

class Polygon(Shape):
    def __init__(self,data):
        super().__init__(data)
        self.data['vertices']=[]
    def place(self,data):
        super().place(data)
        self.data['vertices']=data['vertices']





    # def TopLeft(self,pos,rotation):
    #     x = pos.getX() - self.half_width
    #     y = pos.getY() - self.half_height
    #     return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    # def TopRight(self,pos,rotation):
    #     x = pos.getX() + self.half_width
    #     y = pos.getY() - self.half_height
    #     return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    # def BottomLeft(self,pos,rotation):
    #     x = pos.getX() - self.half_width
    #     y = pos.getY() + self.half_height
    #     return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    # def BottomRight(self,pos,rotation):
    #     x = pos.getX() + self.half_width
    #     y = pos.getY() + self.half_height
    #     return vec2.Vec2(x,y).rotateAroundPoint(rotation,pos)
    def isLeft(self,A, B, P):
        return (
            (B.x - A.x) * (P.y - A.y) - (P.x - A.x) * (B.y - A.y)
        )

    # def collidesWithPoint(self,P):
    #     pass

    # def collision(self,pos,rotation,l):
    #     tl = self.TopLeft(pos,rotation)
    #     tr = self.TopRight(pos,rotation)
    #     bl = self.BottomLeft(pos,rotation)
    #     br = self.BottomRight(pos,rotation)
    #     top = line.LineSeg(tl,tr)
    #     bottom = line.LineSeg(bl,br)
    #     left = line.LineSeg(tl,bl)
    #     right = line.LineSeg(tr,br)
    #     return l.intersectsLineSeg(top) or \
    #         l.intersectsLineSeg(bottom) or \
    #         l.intersectsLineSeg(left) or \
    #         l.intersectsLineSeg(right)


class Object:
    def __init__(self,data):
        self.data = {}
        self.data['id']=data['id']
        self.data['name']=data['name']
        self.data['health']=data['health']
        self.data['damage']=0.0
        self.data['facing']='N'
        self.data['x']=0
        self.data['y']=0
        self.data['components']=data['components']

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None
    def setData(self,key,val):
        self.data[key]=val

    def place(self,data):
        self.data['x']=data['x']
        self.data['y']=data['y']
        self.data['facing']=data['facing']






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



import random
import math

import vec2
import line
from log import *

_2PI = 2.0*math.pi

# class Shape:
#     def __init__(self,name):
#         self.data={}
#         self.data['name'] = name
#         self.data['heading']=0.0
#         self.data['x']=0
#         self.data['y']=0

#     def setData(self,key,val):
#         self.data[key]=val
#     def getData(self,key):
#         if key in self.data:
#             return self.data[key]
#         else:
#             return None

#     def place(self,data):
#         if 'x' in data:
#             self.data['x']=data['x']
#         if 'y' in data:
#             self.data['y']=data['y']
#         if 'heading' in data:
#             self.data['heading']=data['heading']


#     def turn(self,angle):
#         self.data['heading'] += angle
#         if self.data['heading'] < 0.0:
#             self.data['heading'] += _2PI
#         elif self.data['heading'] > _2PI:
#             self.data['heading'] -= _2PI
#     def move(self,distance):
#         self.data['pos'].move(self.data['heading'],distance)

#     def collidesWith(self,other):
#         if isinstance(other,line.LineSeg):
#             return self.collidesWithLineSeg(other)
#         elif isinstance(other,vec2.Vec2):
#             return self.collidesWithPoint(other)
#         elif isinstance(other,Circle):
#             return self.collidesWithCylinder(other)

#     def collidesWithPoint(self,point):
#         return self.data['pos'] == point
#     def collidesWithLineSeg(self,lineseg):
#         return self.data['pos'].intersectsLineSeg(lineseg)
#     def collidesWithCylinder(self,shape):
#         return shape.collidesWithPoint(self.data['pos'])


# class Circle(Shape):
#     def __init__(self,data):
#         super().__init__(data)
#         self.data['radius']=1.0
#     def place(self,data):
#         super().place(data)
#         if 'radius' in data:
#             self.data['radius']=data['radius']
#     def collidesWithPoint(self,point):
#         return self.data['radius'] >= self.data['pos'].distanceToPoint(point)
#     def collidesWithLineSeg(self,lineseg):
#         return self.data['radius'] >= self.data['pos'].distanceToLineSeg(lineseg)
#     def collidesWithCylinder(self,shape):
#         return self.collidesWithPoint(shape.getData('pos'))

# class Polygon(Shape):
#     def __init__(self,data):
#         super().__init__(data)
#         self.data['vertices']=[]
#     def place(self,data):
#         super().place(data)
#         self.data['vertices']=data['vertices']





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
    # def isLeft(self,A, B, P):
    #     return (
    #         (B.x - A.x) * (P.y - A.y) - (P.x - A.x) * (B.y - A.y)
    #     )

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
        self.data['objname']=data['objname']
        self.data['char']=data['char']
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
        
        self.view_keys = [
            'health','damage','facing','x','y','cell_x','cell_y','objname'
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

    def update(self,my_view,world_view):
        if self.data['ai'] != None:
            my_view['self']=self.getSelfView()
            my_view['world']=world_view
            return self.data['ai'].runAI(my_view)
        else:
            return None

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
            'char':self.getData('char'), 'color':self.getData('color')
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

import random

import loader
import obj
import vec2
import log
import zmath

class Map:
    def __init__(self, data):
        self.data = data

    def setData(self,key,val):
        self.data[key]=val
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    # Build the map 2 hexes wider and taller. This allows for
    # the placing of blocks around the edge while still keeping
    # the same playable space outlined in the map json. And
    # it means we do not have to worry about accounting for edge
    # boundries as they cannot be reached (if the edge obj is indestructible).
    def buildMapGrid(self):
        obj_grid=[]
        item_grid=[]
        for x in range(self.data['width']+2):
            obj_newcol = []
            item_newcol = []
            for y in range(self.data['height']+2):
                obj_newcol.append(None)
                item_newcol.append([])
            obj_grid.append(obj_newcol)
            item_grid.append(item_newcol)

        self.data['obj_grid']=obj_grid
        self.data['item_grid']=item_grid

    def addObj(self,x,y,_uuid):
        self.data['obj_grid'][x][y]=_uuid
    def removeObj(self,x,y,_uuid):
        if self.data['obj_grid'][x][y]==_uuid:
            self.data['obj_grid'][x][y]=None

    def addItem(self,x,y,_uuid):
        if _uuid not in self.data['item_grid'][x][y]:
            self.data['item_grid'][x][y].append(_uuid)
    def removeItem(self,x,y,_uuid):
        if _uuid in self.data['item_grid'][x][y]:
            self.data['item_grid'][x][y].remove(_uuid)
    def getItemsInCell(self,x,y):
        return self.data['item_grid'][x][y]

    # Creates a list of the coordinates of the world edge.
    def getListOfEdgeCoordinates(self):
        edge_coords = []
        wide=self.data['width']
        high=self.data['height']
        for x in range(wide):
            edge_coords.append((x,0))
            edge_coords.append((x,high-1))
        for y in range(1,high-1):
            edge_coords.append((0,y))
            edge_coords.append((wide-1,y))
        return edge_coords

    def isCellEmpty(self,x,y):
        return self.getData('obj_grid')[x][y]==None
    def getCellOccupant(self,x,y):
        return self.getData('obj_grid')[x][y]

    def moveObjFromTo(self,objuuid,from_x,from_y,to_x,to_y):
        grid = self.getData('obj_grid')
        if grid[from_x][from_y]==objuuid:
            grid[from_x][from_y]=None
            grid[to_x][to_y]=objuuid

    def getAllObjUUIDAlongTrajectory(self,x,y,angle,distance):

        found = {}
        found['objects']=[]
        found['items']=[]

        # Get refs to the two grids
        obj_grid = self.getData('obj_grid')
        item_grid = self.getData('item_grid')

        # Get the cells
        cells = zmath.getCellsAlongTrajectory(x,y,angle,distance)

        # So long as we're in the map,
        # If the obj or item grid cell is not None
        # create a ping and save it.
        for cell in cells:
            if 0 <= cell[0] < self.getData('width') and 0<=cell[1]<self.getData('height'):
                if obj_grid[cell[0]][cell[1]] != None:
                    _uuid = obj_grid[cell[0]][cell[1]]
                    ping = {}
                    ping['x']=cell[0]
                    ping['y']=cell[1]
                    ping['distance']=zmath.distance(x,y,cell[0],cell[1])
                    ping['uuid']=_uuid
                    ping['type']='object'
                    found['objects'].append(ping)
                if len(item_grid[cell[0]][cell[1]]) > 0:
                    for i in item_grid[cell[0]][cell[1]]:
                        ping={}
                        ping['x']=cell[0]
                        ping['y']=cell[1]
                        ping['distance']=zmath.distance(x,y,cell[0],cell[1])
                        ping['uuid']=i
                        ping['type']='item'
                        found['items'].append(ping)
                
            else:
                break

        return found

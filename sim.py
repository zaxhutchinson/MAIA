import importlib
import uuid
import random

import obj
import copy
import zmap
import comp
import vec2
import loader
import zmath
import msgs
#from log import *

class Sim:
    def __init__(self, imsgr):
        self.reset()
        self.imsgr = imsgr

        self.action_dispatch_table = {}
        self.buildActionDispatchTable()
    def reset(self):
        self.map = None
        self.objs = {}
        self.sides={}
        self.ticks_per_turn=1
        self.tick = 0

        self.obj_views={}

    def buildActionDispatchTable(self):
        self.action_dispatch_table['HIGHSPEED_PROJECTILE'] = self.ACTN_HighspeedProjectile
        self.action_dispatch_table['MOVE']=self.ACTN_Move
        self.action_dispatch_table['TURN']=self.ACTN_Turn
        self.action_dispatch_table['SCAN']=self.ACTN_Scan

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
        self.sides[ID]['teamname']=None
    def getSides(self):
        return self.sides
    
    ##########################################################################
    # TEAMS
    def addTeamName(self,ID,teamname):
        self.sides[ID]['teamname']=teamname
    def getTeamName(self,ID):
        return self.sides[ID]['teamname']
    def delTeamName(self,ID):
        self.sides[ID]['teamname']=None

    ##########################################################################
    # VIEWS
    def addObjView(self,_uuid,viewname,view):
        if _uuid not in self.obj_views:
            self.obj_views[_uuid]={}
        self.obj_views[_uuid][viewname]=view

    ##########################################################################
    # BUILD SIM
    def buildSim(self, ldr):

        config = ldr.copyMainConfig()
        team_dir = config['team_dir']

        # Set the number of ticks per turn
        self.ticks_per_turn = config['ticks_per_turn']
        self.tick=0

        # Build the map grid
        self.map.buildMapGrid()

        # Create the map border
        edge_obj_id = self.map.getData('edge_obj_id')
        edge_coords = self.map.getListOfEdgeCoordinates()
        for ec in edge_coords:
            # Copy the obj
            newobj = ldr.copyObjTemplate(edge_obj_id)
            # Create obj place data
            data = {}
            data['x']=ec[0]
            data['y']=ec[1]
            data['uuid']=uuid.uuid4()
            # Place, add to objDict and add to map
            newobj.place(data)
            self.objs[data['uuid']]=newobj
            self.map.addObj(data['x'],data['y'],data['uuid'])

        # Add all placed objects
        pl_objs = self.map.getData('placed_objects')
        for oid,lst in pl_objs.items():
            for o in lst:
                # If an object entry in placed_objs does not
                # have a position, it is ignored.
                if 'x' in o and 'y' in o:
                    newobj = ldr.copyObjTemplate(oid)
                    data=o
                    data['uuid']=uuid.uuid4()
                    newobj.place(data)
                    self.objs[data['uuid']]=newobj
                    self.map.addObj(data['x'],data['y'],data['uuid'])

        # Add teams and ai-controlled objs
        for k,v in self.sides.items():
            team_data = ldr.copyTeamTemplate(v['teamname'])
            team_data['side']=k
            team_data['agents']={}
            team_name = team_data['name']
            # Copy so we don't f-up the original
            starting_locations = list(v['starting_locations'])

            for agent in team_data['agent_defs']:
                newobj = ldr.copyObjTemplate(agent['object'])
                data={}
                data['side']=k
                data['ticks_per_turn']=config['ticks_per_turn']
                data['callsign']=agent['callsign']
                data['teamname']=team_data['name']
                data['squad']=agent['squad']
                data['object']=agent['object']
                data['uuid']=uuid.uuid4()

                # Randomly choose a starting location
                sl = random.randint(0,len(starting_locations)-1)
                data['x'] = starting_locations[sl][0]
                data['y'] = starting_locations[sl][1]
                # Delete the chosen location so no other team mate gets it.
                del starting_locations[sl]

                # Load and set AI
                ai_filename = agent['AI_file']
                # Load AI module
                ai_spec = importlib.util.spec_from_file_location(ai_filename,team_dir+'/'+team_name+'/'+ai_filename)
                ai_module = importlib.util.module_from_spec(ai_spec)
                ai_spec.loader.exec_module(ai_module)
                data['ai']=ai_module.AI()

                # Create and store components
                for c in newobj.getData('comp_ids'):
                    newcomp = ldr.copyCompTemplate(c)
                    newcomp.setData('parent',newobj)
                    newobj.addComp(newcomp)

                # Place and store and add to map
                newobj.place(data)
                self.objs[data['uuid']]=newobj
                self.map.addObj(data['x'],data['y'],data['uuid'])

                # Add agent obj to team dictionary of agents
                team_data['agents'][data['uuid']]=newobj

            # Add the team data to the side entry
            v['team']=team_data



    def getWorldView(self):
        view = {}
        view['tick']=self.tick
        return view


    ##########################################################################
    # RUN SIM
    def runSim(self, turns):

        objuuids_list = list(self.objs.keys())
        # Shuffle the obj uuids
        random.shuffle(objuuids_list)
        
        for turn in range(turns):
            # A place to store the commands by uuid and tick
            cmds_by_uuid = {}
            
            # get the world view to pass onto objects.
            world_view = self.getWorldView()

            # Run all obj's updates, storing the returned commands
            for objuuid,obj in self.objs.items():
                cmd = None
                if objuuid in self.obj_views:
                    cmd = obj.update(self.obj_views[objuuid],world_view)
                else:
                    cmd = obj.update({},world_view)
                if cmd != None:
                    cmds_by_uuid[objuuid]=cmd


            # Flush the obj_views, so no one gets old data.
            self.obj_views = {}
            
            # Run each tick
            for tick in range(self.ticks_per_turn):

                self.imsgr.addMsg(msgs.Msg(self.tick,"---NEW TICK---",""))

                # Check all commands to see if there is
                # something to do this tick.
                for objuuid,objcmds in cmds_by_uuid.items():
                    
                    if str(tick) in objcmds:

                        cmds_this_tick = objcmds[str(tick)]
                        self.processCommands(objuuid,cmds_this_tick)

                self.tick += 1


    def processCommands(self,objuuid,cmds):

        obj = self.objs[objuuid]
        
        # Send the commands to the object so they can be
        # processed. This returns a list of actions.
        actions = self.objs[objuuid].processCommands(cmds)

        # Dispatch each action to the function that
        # handles its execution.
        for a in actions:

            self.action_dispatch_table[a.getType()](obj,a)

    ##########################################################################
    # ACTION PROCESSING FUNCTIONS
    # These handle the meat of turning actions into world changes.
    # All the sexy happens here.
    ##########################################################################

    # High-speed projectile action
    def ACTN_HighspeedProjectile(self,obj,actn):
        
        # Get list of cells through which the shell travels.
        cells_hit = zmath.getCellsAlongTrajectory(
            obj.getData('x'),
            obj.getData('y'),
            actn.getData('direction'),
            actn.getData('range')
        )

        # Get the list of cells through which the shell travels.
        damage = random.randint(actn.getData('min_damage'),actn.getData('max_damage'))

        # If there's something in a cell, damage the first thing
        # along the path and quit.
        for cell in cells_hit:
            id_in_cell = self.map.getCellOccupant(cell[0].cell[1])
            if id_in_cell != None:

                self.damageObj(id_in_cell,damage)

                break

            
    # Regular object move action
    def ACTN_Move(self,obj,actn):
        # Get current data
        direction = actn.getData('direction')
        cur_speed = actn.getData('speed')
        old_x = obj.getData('x')
        old_y = obj.getData('y')
        old_cell_x = obj.getData('cell_x')
        old_cell_y = obj.getData('cell_y')
        x = old_x + old_cell_x
        y = old_y + old_cell_y
        # translate and new data
        new_position = zmath.translatePoint(x,y,direction,cur_speed)
        new_x = int(new_position[0])
        new_y = int(new_position[1])
        new_cell_x = abs(new_position[0]-abs(new_x))
        new_cell_y = abs(new_position[1]-abs(new_y))
        # see if move is possible.
        if new_x != old_x or new_y != old_y:
            if self.map.isCellEmpty(new_x,new_y):
                self.map.moveObjFromTo(obj.getData('uuid'),old_x,old_y,new_x,new_y)
                obj.setData('x',new_x)
                obj.setData('y',new_y)
                obj.setData('cell_x',new_cell_x)
                obj.setData('cell_y',new_cell_y)
            else:
                # CRASH INTO SOMETHING
                
                # We're still in the same cell but we need to move the obj to the edge
                # of the old cell to simulate that they reached the edge of it before
                # crashing.
                if new_x != old_x:
                    if new_x > old_x:
                        obj.setData('cell_x',0.99)
                    else:
                        obj.setData('cell_x',0.0)
                if new_y != old_y:
                    if new_y > old_y:
                        obj.setData('cell_y',0.99)
                    else:
                        obj.setData('cell_y',0.0)
        else:
            obj.setData('cell_x',new_cell_x)
            obj.setData('cell_y',new_cell_y)
            pass


    # Turns the obj
    def ACTN_Turn(self,obj,actn):
        cur_facing = obj.getData('facing')
        new_facing = cur_facing + actn.getData('turnrate')
        while new_facing < -360:
            new_facing += 360
        while new_facing > 360:
            new_facing -= 360
        obj.setData('facing',new_facing)


    # Performs a scan
    def ACTN_Scan(self,obj,actn):
        print("Performing Scan")
        view = {}
        view['compname']=actn.getData('compname')
        view['pings']={}

        # Set up the necessary data for easy access
        scan_facing = actn.getData('facing')+actn.getData('offset_angle')
        start = scan_facing-actn.getData('visarc')
        end = scan_facing+actn.getData('visarc')
        angle = start
        jump = actn.getData('resolution')
        x = actn.getData('x')
        y = actn.getData('y')
        _range = actn.getData('range')

        temp_view = {}

        # While we're in our arc of visibility
        while angle <= end:
            # Get all objects along this angle
            pings = self.map.getAllObjUUIDAlongTrajectory(
                x,y,angle,_range
            )
            # Pings should be in order. Start adding if they're not there.
            # If the scanner's level is less than the obj's density, stop. We can't see through.
            # Else keep going.

            
            for ping in pings:

                # Scanned ourself
                if ping['x']==x and ping['y']==y:
                    pass
                else:
                    if ping['uuid'] not in temp_view:
                        # For now all we're giving the scanning player
                        # the object name. Up to the player to figure out
                        # if this is a teammate.
                        ping['objname']=self.objs[ping['uuid']].getData('objname')
                        temp_view[str(angle)]=ping
                    if actn.getData('level') < self.objs[ping['uuid']].getData('density'):
                        break

            angle += jump

        for angl,ping in temp_view.items():
            del ping['uuid']
            view['pings'][angl]=ping

        self.addObjView(obj.getData('uuid'),actn.getData('slot_id'),view)


    ##########################################################################
    # ADDITIONAL HELPER FUNCTIONS
    # Some of the ACTN function do similar work.
    ##########################################################################
    def damageObj(self,_uuid,damage):
        # Damage object
        self.objs[_uuid].damage(damage)
        
        # If obj is dead, remove it.
        if self.objs[_uuid].getData('alive')==False:

            dead_obj = self.objs[_uuid]
            # Remove from map
            self.map.removeObj(dead_obj.getData('x'),dead_obj.getData('y'),dead_obj.getData('uuid'))
            # Remove from obj dict
            del self.objs[_uuid]
            # Remove from team
            side = dead_obj.getData('side')
            del self.sides[side]['agents'][_uuid]

            # NOTE: Maybe at some point I'll need to do something with
            # dead objects. For now, the reference will just go out of scope.


    ##########################################################################
    # DRAWING DATA
    # This gets and returns a list of all drawing necessary data from the
    # live objects.
    ##########################################################################

    def getObjDrawData(self):
        dd = []
        for obj in self.objs.values():
            dd.append(obj.getDrawData())
        return dd
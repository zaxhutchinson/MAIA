import importlib
import uuid
import random

import copy
import zmap
import comp
import vec2
import loader
import zmath
import msgs
from zexceptions import *
import valid
import views
import gstate
import zfunctions

from ui_sim import UISim


class Sim:
    def __init__(self, imsgr):
        self.reset()
        self.imsgr = imsgr
        self.command_validator = valid.CommandValidator()

        self.action_dispatch_table = {}
        self.buildActionDispatchTable()

        self.view_manager = views.ViewManager()

    def reset(self):
        self.map = None
        self.objs = {}
        self.items = {}
        self.destroyed_objs = {}
        self.sides = {}
        self.ticks_per_turn = 1
        self.tick = 0
        self.win_states = []
        self.comp_views = {}
        self.actions = {}
        self.action_priority = {}
        self.action_priority_keys = []

    def buildActionDispatchTable(self):
        self.action_dispatch_table["HIGHSPEED_PROJECTILE"] = (
            self.ACTN_HighspeedProjectile
        )
        self.action_dispatch_table["MOVE"] = self.ACTN_Move
        self.action_dispatch_table["TURN"] = self.ACTN_Turn
        self.action_dispatch_table["TRANSMIT_RADAR"] = self.ACTN_TransmitRadar
        self.action_dispatch_table["BROADCAST"] = self.ACTN_BroadcastMessage
        self.action_dispatch_table["TAKE_ITEM"] = self.ACTN_TakeItem
        self.action_dispatch_table["DROP_ITEM"] = self.ACTN_DropItem

    ##########################################################################
    # MAP
    def setMap(self, _map):
        self.map = _map
        sides = self.map.getData("sides")
        for k, v in sides.items():
            self.addSide(k, v)

    def getMap(self):
        return self.map

    def hasMap(self):
        return self.map is not None

    ##########################################################################
    # SIDES
    def addSideID(self, ID):
        self.sides[ID] = None

    def addSide(self, ID, side):
        self.sides[ID] = side
        self.sides[ID]["teamname"] = None

    def getSides(self):
        return self.sides

    ##########################################################################
    # TEAMS
    def addTeamName(self, ID, teamname):
        self.sides[ID]["teamname"] = teamname

    def getTeamName(self, ID):
        return self.sides[ID]["teamname"]

    def delTeamName(self, ID):
        self.sides[ID]["teamname"] = None

    ##########################################################################
    # VIEWS
    # def addSelfView(self,_uuid,view):
    #     if _uuid not in self.self_views:
    #         self.self_views[_uuid]=[]
    #     self.self_views[_uuid].append(view)
    def addCompView(self, _uuid, view):
        if _uuid not in self.comp_views:
            self.comp_views[_uuid] = []

        self.comp_views[_uuid].append(view)

    ##########################################################################
    # ACTIONS
    def buildActionPriority(self, config):
        ap = config["action_priority"]
        for k, v in ap.items():
            self.action_priority_keys.append(v)
            self.action_priority[v] = k
            self.actions[k] = []
        self.action_priority_keys = sorted(self.action_priority_keys)

    def resetActionDict(self):
        for v in self.actions.values():
            v.clear()

    ##########################################################################
    # WIN STATE
    def setAllWinStates(self, ldr, ws_names):
        for wsname in ws_names:
            # Copy gstate
            win_states = ldr.copyGStateTemplate(wsname)
            # Init using the objects/items on hand
            for ws in win_states:
                ws.initState(self.objs, self.items)
                # Add
                self.addWinState(ws)

    def addWinState(self, ws):
        self.win_states.append(ws)

    ##########################################################################
    # BUILD SIM
    def buildSim(self, ldr):

        if not self.hasMap():
            raise BuildException("No map was selected.")

        for k, v in self.sides.items():
            if v["teamname"] is None:
                raise BuildException("Side " + k + " has no team assignment.")

        # Get the main config dict
        config = ldr.copyMainConfig()

        # Set the team directory
        team_dir = config["team_dir"]

        # Set the action Priority and sorted keys.
        self.buildActionPriority(config)

        # Set the number of ticks per turn
        self.ticks_per_turn = config["ticks_per_turn"]
        self.tick = 0

        # Build the map grid
        self.map.buildMapGrid()

        # Create the map border
        edge_obj_id = self.map.getData("edge_obj_id")
        edge_coords = self.map.getListOfEdgeCoordinates()
        for ec in edge_coords:
            # Copy the obj
            newobj = ldr.copyObjTemplate(edge_obj_id)
            # Create obj place data
            data = {}
            data["x"] = ec[0]
            data["y"] = ec[1]
            data["uuid"] = uuid.uuid4()
            # Place, add to objDict and add to map
            newobj.place(data)
            self.objs[data["uuid"]] = newobj
            self.map.addObj(data["x"], data["y"], data["uuid"])

        # Add all placed objects
        pl_objs = self.map.getData("placed_objects")
        for oid, lst in pl_objs.items():
            for o in lst:
                # If an object entry in placed_objs does not
                # have a position, it is ignored.
                if "x" in o and "y" in o:
                    newobj = ldr.copyObjTemplate(oid)
                    data = o
                    data["uuid"] = uuid.uuid4()
                    newobj.place(data)
                    self.objs[data["uuid"]] = newobj
                    self.map.addObj(data["x"], data["y"], data["uuid"])

        # Add all placed items
        pl_items = self.map.getData("placed_items")
        for iid, lst in pl_items.items():
            for i in lst:
                # If an item entry does not have a position, ignore.
                if "x" in i and "y" in i:
                    newitem = ldr.copyItemTemplate(iid)
                    data = i
                    data["uuid"] = uuid.uuid4()
                    newitem.place(data)
                    self.items[data["uuid"]] = newitem
                    self.map.addItem(data["x"], data["y"], data["uuid"])

        # Add teams and ai-controlled objs
        for k, v in self.sides.items():
            team_data = ldr.copyTeamTemplate(v["teamname"])
            team_data["side"] = k
            team_data["agents"] = {}
            team_name = team_data["name"]
            # Copy so we don't f-up the original
            starting_locations = list(v["starting_locations"])

            for agent in team_data["agent_defs"]:
                newobj = ldr.copyObjTemplate(agent["object"])
                data = {}
                data["side"] = k
                data["ticks_per_turn"] = config["ticks_per_turn"]
                data["callsign"] = agent["callsign"]
                data["teamname"] = team_data["name"]
                data["squad"] = agent["squad"]
                data["object"] = agent["object"]
                data["uuid"] = uuid.uuid4()

                # Randomly choose a starting location
                sl = random.randint(0, len(starting_locations) - 1)
                data["x"] = starting_locations[sl][0]
                data["y"] = starting_locations[sl][1]

                # Delete the chosen location so no other team mate gets it.
                del starting_locations[sl]

                # select a random facing.
                facing = v["facing"]
                if facing == "None":
                    facing = random.random() * 360.0
                else:
                    facing = float(facing)

                data["facing"] = facing

                # Load and set AI
                ai_filename = agent["AI_file"]
                ai_spec = importlib.util.spec_from_file_location(
                    ai_filename, team_dir + "/" + team_name + "/" + ai_filename
                )
                ai_module = importlib.util.module_from_spec(ai_spec)
                ai_spec.loader.exec_module(ai_module)
                AI = ai_module.AI()
                AI.initData(data)

                # Store the AI object after initialization
                # to avoid including it in the data dict passed
                # to the AI itself.
                data["ai"] = AI

                # Create and store components
                for c in newobj.getData("comp_ids"):
                    newcomp = ldr.copyCompTemplate(c)
                    newcomp.setData("parent", newobj)
                    newobj.addComp(newcomp)

                # Place and store and add to map
                newobj.place(data)
                self.objs[data["uuid"]] = newobj
                self.map.addObj(data["x"], data["y"], data["uuid"])

                # Add agent obj to team dictionary of agents
                team_data["agents"][data["uuid"]] = newobj

            # Add the team data to the side entry
            v["team"] = team_data

        # Set the Global States
        self.setAllWinStates(ldr, self.map.getData("win_states"))

    ##########################################################################
    # Get the world view
    def getGeneralView(self):
        view = {}
        view["tick"] = self.tick
        return view

    ##########################################################################
    # CHECK END OF GAME
    def checkEndOfSim(self):

        rtn = False

        # Run through all win conditions even if one is True.
        # Two win conditions could come up True in the same turn.
        for win_state in self.win_states:

            r = win_state.checkState()

            if r:
                self.imsgr.addMsg(
                    msgs.Msg(
                        self.tick,
                        "GAME OVER",
                        win_state.getData("msg"),
                    )
                )
            rtn = rtn or r
        return rtn

        # Only 1 team remaining
        # teams_remaining = []
        # for name,data in self.sides.items():
        #     team_eliminated = True

        #     for obj in data['team']['agents'].values():
        #         if obj.getData('alive'):
        #             team_eliminated=False
        #             break
        #     if not team_eliminated:
        #         teams_remaining.append(name)

        # if len(teams_remaining) == 1:
        #     self.imsgr.addMsg(msgs.Msg(self.tick,"---GAME OVER---","The winning side is: " + teams_remaining[0]))
        #     return True
        # if len(teams_remaining) == 0:
        #     self.imsgr.addMsg(msgs.Msg(self.tick,"---GAME OVER---","All teams are dead???"))
        #     return True
        # return False

    def getPointsData(self):
        msg = ""
        for name, data in self.sides.items():
            msg += "  TEAM: " + name + "\n"
            total = 0
            for curr_obj in data["team"]["agents"].values():
                msg += (
                    "    "
                    + curr_obj.getBestDisplayName()
                    + ": "
                    + str(curr_obj.getData("points"))
                    + "\n"
                )
                total += curr_obj.getData("points")
            msg += "    TOTAL: " + str(total) + "\n"

        m = msgs.Msg(str(self.tick), "CURRENT POINTS", msg)
        self.imsgr.addMsg(m)

    def getFinalScores(self):
        final_scores = {}
        for name, data in self.sides.items():
            team_scores = {"agents": {}, "total": 0}

            for agent_name, curr_obj in data["team"]["agents"].items():
                agent_score = curr_obj.getData("points")
                team_scores["agents"][curr_obj.getBestDisplayName()] = agent_score
                team_scores["total"] += agent_score

            final_scores[name] = team_scores

        return final_scores

    ##########################################################################
    # RUN SIM
    def runSim(self, turns):

        for turn in range(turns):
            # A place to store the commands by uuid and tick
            cmds_by_uuid = {}

            # get the general view to pass onto objects.
            general_view = self.getGeneralView()

            # Run all obj's updates, storing the returned commands
            # Don't need to shuffle order while getting commands
            for objuuid, curr_obj in self.objs.items():

                cmd = None
                view = {}
                view["general"] = general_view
                if objuuid in self.comp_views:
                    view["comp"] = self.comp_views[objuuid]

                # Call update and get commands
                cmd = curr_obj.update(view)

                # Validate commands
                cmd = self.command_validator.validateCommands(cmd)

                if cmd is not None:
                    if type(cmd) is dict and len(cmd) > 0:
                        cmds_by_uuid[objuuid] = cmd

            # Flush the obj_views, so no one gets old data.
            self.comp_views = {}

            # Get the list of obj uuids which have issued cmds.
            objuuids_list = list(cmds_by_uuid.keys())

            # Run each tick
            for tick in range(self.ticks_per_turn):
                self.imsgr.addMsg(msgs.Msg(self.tick, "---NEW TICK---", ""))

                # Advance turn order sequentially by rotating list of all active agents by 1.
                objuuids_list = objuuids_list[1:]

                # Check all commands to see if there is
                # something to do this tick.
                # for objuuid,objcmds in cmds_by_uuid.items():
                for objuuid in objuuids_list:
                    objcmds = cmds_by_uuid[objuuid]
                    if str(tick) in objcmds:
                        cmds_this_tick = objcmds[str(tick)]
                        self.processCommands(objuuid, cmds_this_tick)

                self.processUpdates()

                # Run all actions by type in the order specified in the main
                # config's action_priority
                for ap in self.action_priority_keys:
                    action_type = self.action_priority[ap]

                    cur_actions = self.actions[action_type]

                    # act is a tuple: (obj,action)
                    for act in cur_actions:
                        # Log the action with the object's logger.
                        act[0].logInfo(zfunctions.ActionToString(act[1]))
                        # Execute action.
                        self.action_dispatch_table[action_type](act[0], act[1])

                # All actions have been run, now clear action dict.
                self.resetActionDict()

                # Check if the sim is over.
                if self.checkEndOfSim():
                    return True
                else:
                    self.tick += 1

    def processCommands(self, objuuid, cmds):

        # Prevents commands from objs destroyed in this tick
        # from taking place.
        if objuuid in self.objs:

            curr_obj = self.objs[objuuid]

            # Send the commands to the object so they can be
            # processed. This returns a list of actions.
            actions = self.objs[objuuid].processCommands(cmds)

            # Dispatch each action to the function that
            # handles its execution.
            for a in actions:

                # Add obj ref and action as a tuple.
                self.actions[a.getType()].append((curr_obj, a))

                # self.action_dispatch_table[a.getType()](obj,a)

    def processUpdates(self):

        for objuuid, obj in self.objs.items():

            actions = obj.processUpdates()

            for a in actions:

                # Add obj ref and action as a tuple.
                self.actions[a.getType()].append((obj, a))

    ##########################################################################
    # ACTION PROCESSING FUNCTIONS
    # These handle the meat of turning actions into world changes.
    # All the sexy happens here.
    ##########################################################################

    # High-speed projectile action
    def ACTN_HighspeedProjectile(self, curr_obj, actn):

        view = self.view_manager.getViewTemplate("projectile")
        view["compname"] = actn.getData("compname")

        # Get list of cells through which the shell travels.
        cells_hit = zmath.getCellsAlongTrajectory(
            curr_obj.getData("x"),
            curr_obj.getData("y"),
            actn.getData("direction"),
            actn.getData("range"),
        )

        # Get the list of cells through which the shell travels.
        damage = random.randint(actn.getData("min_damage"), actn.getData("max_damage"))

        # If there's something in a cell, damage the first thing
        # along the path and quit.
        for cell in cells_hit:
            id_in_cell = self.map.getCellOccupant(cell[0], cell[1])
            if id_in_cell == curr_obj.getData("uuid"):
                continue
            elif id_in_cell is not None:

                view["hit_x"] = cell[0]
                view["hit_y"] = cell[1]
                view["name"] = self.objs[id_in_cell].getData("name")

                damage_str = (
                    curr_obj.getBestDisplayName()
                    + " shot "
                    + self.objs[id_in_cell].getBestDisplayName()
                    + " for "
                    + str(damage)
                    + " points of damage."
                )
                self.logMsg("DAMAGE", damage_str)

                points = self.damageObj(id_in_cell, damage)

                curr_obj.setData("points", points)

                break

        self.addCompView(curr_obj.getData("uuid"), view)

    # Regular object move action
    def ACTN_Move(self, curr_obj, actn):
        # Get current data
        facing = curr_obj.getData("facing")
        cur_speed = actn.getData("speed")
        old_x = curr_obj.getData("x")
        old_y = curr_obj.getData("y")
        old_cell_x = curr_obj.getData("cell_x")
        old_cell_y = curr_obj.getData("cell_y")
        x = old_x + old_cell_x
        y = old_y + old_cell_y
        # translate and new data
        new_position = zmath.translatePoint(x, y, facing, cur_speed)
        new_x = int(new_position[0])
        new_y = int(new_position[1])
        new_cell_x = abs(new_position[0] - abs(new_x))
        new_cell_y = abs(new_position[1] - abs(new_y))

        # see if move is possible.
        if new_x != old_x or new_y != old_y:

            # Might be moving more than 1 cell. Get trajectory.
            cell_path = zmath.getCellsAlongTrajectory(x, y, facing, cur_speed)

            cur_cell = (old_x, old_y)
            collision = False

            # for all cells in the path, update if empty.
            for cell in cell_path:
                if cell == (old_x, old_y):
                    continue
                else:
                    if self.map.isCellEmpty(cell[0], cell[1]):
                        cur_cell = cell
                    else:
                        collision = True
                        break

            new_x = cur_cell[0]
            new_y = cur_cell[1]

            # Move the object
            self.map.moveObjFromTo(curr_obj.getData("uuid"), old_x, old_y, new_x, new_y)
            curr_obj.setData("x", new_x)
            curr_obj.setData("y", new_y)
            curr_obj.setData("cell_x", new_cell_x)
            curr_obj.setData("cell_y", new_cell_y)

            # Update held item's locations
            item_uuids = curr_obj.getAllHeldStoredItems()
            for _uuid in item_uuids:
                i = self.items[_uuid]
                i.setData("x", new_x)
                i.setData("y", new_y)

            if collision:
                # CRASH INTO SOMETHING

                # We need to move the obj to the edge
                # of the old cell to simulate that they reached the edge of it before
                # crashing.
                if new_x != old_x:
                    if new_x > old_x:
                        curr_obj.setData("cell_x", 0.99)
                    else:
                        curr_obj.setData("cell_x", 0.0)
                if new_y != old_y:
                    if new_y > old_y:
                        curr_obj.setData("cell_y", 0.99)
                    else:
                        curr_obj.setData("cell_y", 0.0)

        # Didn't leave the cell, update in-cell coords.
        else:
            curr_obj.setData("cell_x", new_cell_x)
            curr_obj.setData("cell_y", new_cell_y)
            pass

    # Turns the obj
    def ACTN_Turn(self, curr_obj, actn):

        cur_facing = curr_obj.getData("facing")
        new_facing = cur_facing + actn.getData("turnrate")
        while new_facing < 0:
            new_facing += 360
        while new_facing >= 360:
            new_facing -= 360
        curr_obj.setData("facing", new_facing)

    # Performs a radar transmission
    def ACTN_TransmitRadar(self, curr_obj, actn):

        view = self.view_manager.getViewTemplate("radar")
        view["tick"] = self.tick
        view["ctype"] = actn.getData("ctype")
        view["compname"] = actn.getData("compname")
        view["slot_id"] = actn.getData("slot_id")

        # Set up the necessary data for easy access
        radar_facing = curr_obj.getData("facing") + actn.getData("offset_angle")
        start = radar_facing - actn.getData("visarc")
        end = radar_facing + actn.getData("visarc")
        angle = start
        jump = actn.getData("resolution")
        x = curr_obj.getData("x")
        y = curr_obj.getData("y")
        _range = actn.getData("range")

        temp_view = []

        # While we're in our arc of visibility
        while angle <= end:
            # Get all object/item pings along this angle
            pings = self.map.getAllObjUUIDAlongTrajectory(x, y, angle, _range)
            # Pings should be in order. Start adding if they're not there.
            # If the radar's level is less than the obj's density, stop. We can't see through.
            # Else keep going.
            obj_pings = pings["objects"]
            item_pings = pings["items"]

            for ping in obj_pings:

                # Pinged ourself
                if ping["x"] == curr_obj.getData("x") and ping["y"] == curr_obj.getData(
                    "y"
                ):
                    pass
                else:
                    # For now all we're giving the transmitting player
                    # the object name. Up to the player to figure out
                    # if this is a teammate.
                    ping["name"] = self.objs[ping["uuid"]].getData("name")

                    # Make sure the reported direction is 0-360
                    direction = angle
                    if direction < 0:
                        direction += 360
                    if direction >= 360:
                        direction -= 360

                    ping["direction"] = direction
                    ping["cell_x"] = self.objs[ping["uuid"]].getData("cell_x")
                    ping["cell_y"] = self.objs[ping["uuid"]].getData("cell_y")
                    ping["alive"] = self.objs[ping["uuid"]].isAlive()
                    temp_view.append(ping)

                    # If our radar level can't penetrate the object, stop.
                    if actn.getData("level") < self.objs[ping["uuid"]].getData(
                        "density"
                    ):
                        break

            for ping in item_pings:

                item = self.items[ping["uuid"]]

                # Make sure the reported direction is 0-360
                direction = angle
                if direction < 0:
                    direction += 360
                if direction >= 360:
                    direction -= 360

                ping["direction"] = direction
                ping["name"] = item.getData("name")
                ping["weight"] = item.getData("weight")
                ping["bulk"] = item.getData("bulk")
                ping["owner"] = item.getData("owner")
                temp_view.append(ping)

            if jump == 0:
                break
            else:
                angle += jump

        for ping in temp_view:
            del ping["uuid"]
            view["pings"].append(ping)

        self.addCompView(curr_obj.getData("uuid"), view)

    def ACTN_BroadcastMessage(self, curr_obj, actn):

        view = {}
        view["vtype"] = "message"
        view["tick"] = self.tick
        view["message"] = actn.getData("message")

        for curr_uuid, other_obj in self.objs.items():
            if curr_uuid != curr_obj.getData("uuid"):

                distance = zmath.distance(
                    curr_obj.getData("x"),
                    curr_obj.getData("y"),
                    other_obj.getData("x"),
                    other_obj.getData("y"),
                )

                # if the distance to the other obj is less than
                # the broadcast range, add the view.
                if distance <= actn.getData("range"):
                    self.addCompView(curr_uuid, view)

    def ACTN_TakeItem(self, curr_obj, actn):

        take_location = actn.getData("location")

        # If we're taking from the cell,
        # or if a take location was not provided, take from cell.
        if take_location == "cell" or take_location is None:

            obj_x = curr_obj.getData("x")
            obj_y = curr_obj.getData("y")
            items_in_obj_cell = self.map.getItemsInCell(obj_x, obj_y)

            if len(items_in_obj_cell) > 0:
                item_name = actn.getData("item_name")
                item_index = actn.getData("item_index")
                item_uuid = actn.getData("item_uuid")

                matching_item = None

                # If the action provided a specific uuid,
                # look only for that and ignore the other info.
                if item_uuid is not None:
                    if item_uuid in items_in_obj_cell:
                        matching_item = item_uuid

                elif item_name is not None:
                    for item_id in items_in_obj_cell:
                        item = self.items[item_id]
                        if item.getData("name") == item_name:
                            matching_item = item_id
                            break
                elif item_index is not None:
                    if len(items_in_obj_cell) > item_index:
                        matching_item = items_in_obj_cell[item_index]

                else:
                    if len(items_in_obj_cell) > 0:
                        matching_item = items_in_obj_cell[0]

                if matching_item is not None:
                    item_to_take = self.items[matching_item]

                    # Get the arm component and make sure it isn't None
                    arm_comp = curr_obj.getComp(actn.getData("slot_id"))
                    if arm_comp is None:
                        print("ArmComp is None")
                        return

                    if not arm_comp.isHoldingItem():
                        if arm_comp.canTakeItem(
                            item_to_take.getData("weight"), item_to_take.getData("bulk")
                        ):
                            arm_comp.setData("item", matching_item)
                            self.map.removeItem(obj_x, obj_y, matching_item)
                            item_to_take.takeItem(curr_obj.getData("uuid"))
                            print("Take successful.")
                        else:
                            print("Item too heavy or bulky.")
                            pass
                    else:
                        print("Arm is already packing.")
                        pass

    def ACTN_DropItem(self, curr_obj, actn):
        print("Dropping item")
        obj_x = curr_obj.getData("x")
        obj_y = curr_obj.getData("y")

        arm_comp = curr_obj.getComp(actn.getData("slot_id"))
        if arm_comp is None:
            return

        if arm_comp.isHoldingItem():
            held_item_uuid = arm_comp.getData("item")
            held_item = self.items[held_item_uuid]

            drop_location = actn.getData("location")

            # Action must specify a valid drop location before
            # the item is dropped.
            if drop_location == "cell":
                print("Drop successful")
                self.map.addItem(obj_x, obj_y, held_item_uuid)
                arm_comp.setData("item", None)
                held_item.dropItem()

    ##########################################################################
    # ADDITIONAL HELPER FUNCTIONS
    # Some of the ACTN function do similar work.
    ##########################################################################

    def damageObj(self, _uuid, damage):
        # Damage object
        points = self.objs[_uuid].damageObj(damage)

        # If obj is dead, remove it.
        if not self.objs[_uuid].isAlive():

            dead_obj = self.objs[_uuid]

            # Check for held/stored items
            held_items_uuids = dead_obj.getAndRemoveAllHeldStoredItems()
            for i in held_items_uuids:
                self.map.addItem(dead_obj.getData("x"), dead_obj.getData("y"), i)

            # Remove from map
            self.map.removeObj(
                dead_obj.getData("x"), dead_obj.getData("y"), dead_obj.getData("uuid")
            )

            # Remove from obj dict
            del self.objs[_uuid]

            # # Add to destroyed objs
            self.destroyed_objs[_uuid] = dead_obj

        return points

    ##########################################################################
    # DRAWING DATA
    # This gets and returns a list of all drawing necessary data from the
    # live objects.
    ##########################################################################

    def getObjDrawData(self):
        dd = []
        for curr_obj in self.destroyed_objs.values():
            dd.append(curr_obj.getDrawData())
        for curr_obj in self.objs.values():
            dd.append(curr_obj.getDrawData())
        return dd

    def getItemDrawData(self):
        dd = []
        for item in self.items.values():
            dd.append(item.getDrawData())
        return dd

    ##########################################################################
    # SEND MESSAGE TO HANDLER
    ##########################################################################
    # Convenience function to create a message for the UI's log
    def logMsg(self, title, text):
        self.imsgr.addMsg(msgs.Msg(self.tick, title, text))

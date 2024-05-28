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
        """Initializes default sim values and an empty action dispatch table"""
        self.reset()
        self.imsgr = imsgr
        self.command_validator = valid.CommandValidator()

        self.action_dispatch_table = {}
        self.build_action_dispatch_table()

        self.view_manager = views.ViewManager()

    def reset(self):
        """Resets default sim values"""
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

    def build_action_dispatch_table(self):
        """Adds actions to dispatch table"""
        self.action_dispatch_table["HIGHSPEED_PROJECTILE"] = (
            self.actn_highspeed_projectile
        )
        self.action_dispatch_table["MOVE"] = self.actn_move
        self.action_dispatch_table["TURN"] = self.actn_turn
        self.action_dispatch_table["TRANSMIT_RADAR"] = self.actn_transmit_radar
        self.action_dispatch_table["BROADCAST"] = self.actn_broadcast_message
        self.action_dispatch_table["TAKE_ITEM"] = self.actn_take_item
        self.action_dispatch_table["DROP_ITEM"] = self.actn_drop_item

    ##########################################################################
    # MAP
    def set_map(self, _map):
        """Sets map"""
        self.map = _map
        sides = self.map.get_data("sides")
        for k, v in sides.items():
            self.add_side(k, v)

    def get_map(self):
        """Gets map"""
        return self.map

    def has_map(self):
        """Determines if sim has map"""
        return self.map is not None

    ##########################################################################
    # SIDES
    def add_side_id(self, ID):
        """Adds side id"""
        self.sides[ID] = None

    def add_side(self, ID, side):
        """Adds side"""
        self.sides[ID] = side
        self.sides[ID]["teamname"] = None

    def get_sides(self):
        """Gets sides"""
        return self.sides

    ##########################################################################
    # TEAMS
    def add_team_name(self, ID, team_name):
        """Adds team name"""
        self.sides[ID]["teamname"] = team_name

    def get_team_name(self, ID):
        """Gets team name from id"""
        return self.sides[ID]["teamname"]

    def del_team_name(self, ID):
        """Deletes team name"""
        self.sides[ID]["teamname"] = None

    ##########################################################################
    # VIEWS
    # def addSelfView(self,_uuid,view):
    #     if _uuid not in self.self_views:
    #         self.self_views[_uuid]=[]
    #     self.self_views[_uuid].append(view)
    def add_comp_view(self, _uuid, view):
        """Adds component view"""
        if _uuid not in self.comp_views:
            self.comp_views[_uuid] = []

        self.comp_views[_uuid].append(view)

    ##########################################################################
    # ACTIONS
    def build_action_priority(self, config):
        """Builds action priority"""
        ap = config["action_priority"]
        for k, v in ap.items():
            self.action_priority_keys.append(v)
            self.action_priority[v] = k
            self.actions[k] = []
        self.action_priority_keys = sorted(self.action_priority_keys)

    def reset_action_dict(self):
        """Resets acionn dictionary"""
        for v in self.actions.values():
            v.clear()

    ##########################################################################
    # WIN STATE
    def set_all_win_states(self, ldr, ws_names):
        """Sets win states"""
        for wsname in ws_names:
            # Copy gstate
            win_states = ldr.copy_gstate_template(wsname)
            # Init using the objects/items on hand
            for ws in win_states:
                ws.init_state(self.objs, self.items)
                # Add
                self.add_win_state(ws)

    def add_win_state(self, ws):
        """Adds win state"""
        self.win_states.append(ws)

    ##########################################################################
    # BUILD SIM
    def build_sim(self, ldr):
        """Builds sim

        Builds map and set win state(s)
        """
        if not self.has_map():
            raise BuildException("No map was selected.")

        for k, v in self.sides.items():
            if v["teamname"] is None:
                raise BuildException("Side " + k + " has no team assignment.")

        # Get the main config dict
        config = ldr.copy_main_config()

        # Set the team directory
        team_dir = config["team_dir"]

        # Set the action Priority and sorted keys.
        self.build_action_priority(config)

        # Set the number of ticks per turn
        self.ticks_per_turn = config["ticks_per_turn"]
        self.tick = 0

        # Build the map grid
        self.map.build_map_grid()

        # Create the map border
        edge_obj_id = self.map.get_data("edge_obj_id")
        edge_coords = self.map.get_list_of_edge_coordinates()
        for ec in edge_coords:
            # Copy the obj
            new_obj = ldr.copy_obj_template(edge_obj_id)
            # Create obj place data
            data = {}
            data["x"] = ec[0]
            data["y"] = ec[1]
            data["uuid"] = uuid.uuid4()
            # Place, add to objDict and add to map
            new_obj.place(data)
            self.objs[data["uuid"]] = new_obj
            self.map.add_obj(data["x"], data["y"], data["uuid"])

        # Add all placed objects
        pl_objs = self.map.get_data("placed_objects")
        for oid, lst in pl_objs.items():
            for o in lst:
                # If an object entry in placed_objs does not
                # have a position, it is ignored.
                if "x" in o and "y" in o:
                    new_obj = ldr.copy_obj_template(oid)
                    data = o
                    data["uuid"] = uuid.uuid4()
                    if new_obj.place:
                        new_obj.place(data)
                    self.objs[data["uuid"]] = new_obj
                    self.map.add_obj(data["x"], data["y"], data["uuid"])

        # Add all placed items
        pl_items = self.map.get_data("placed_items")
        for iid, lst in pl_items.items():
            for i in lst:
                # If an item entry does not have a position, ignore.
                if "x" in i and "y" in i:
                    new_item = ldr.copy_item_template(iid)
                    data = i
                    data["uuid"] = uuid.uuid4()
                    new_item.place(data)
                    self.items[data["uuid"]] = new_item
                    self.map.add_item(data["x"], data["y"], data["uuid"])

        # Add teams and ai-controlled objs
        for k, v in self.sides.items():
            team_data = ldr.copy_team_template(v["teamname"])
            team_data["side"] = k
            team_data["agents"] = {}
            team_name = team_data["name"]
            # Copy so we don't f-up the original
            starting_locations = list(v["starting_locations"])

            for agent in team_data["agent_defs"]:
                new_obj = ldr.copy_obj_template(agent["object"])
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
                ai_file_name = agent["AI_file"]
                ai_spec = importlib.util.spec_from_file_location(
                    ai_file_name, team_dir + "/" + team_name + "/" + ai_file_name
                )
                ai_module = importlib.util.module_from_spec(ai_spec)
                ai_spec.loader.exec_module(ai_module)
                AI = ai_module.AI()
                AI.init_data(data)

                # Store the AI object after initialization
                # to avoid including it in the data dict passed
                # to the AI itself.
                data["ai"] = AI

                # Create and store components
                for c in new_obj.get_data("comp_ids"):
                    new_comp = ldr.build_comp(c)
                    new_comp.set_data("parent", new_obj)
                    new_obj.add_comp(new_comp)

                # Place and store and add to map
                new_obj.place(data)
                self.objs[data["uuid"]] = new_obj
                self.map.add_obj(data["x"], data["y"], data["uuid"])

                # Add agent obj to team dictionary of agents
                team_data["agents"][data["uuid"]] = new_obj

            # Add the team data to the side entry
            v["team"] = team_data

        # Set the Global States
        self.set_all_win_states(ldr, self.map.get_data("win_states"))

    ##########################################################################
    # Get the world view
    def get_general_view(self):
        """Gets general world view"""
        view = {}
        view["tick"] = self.tick
        return view

    ##########################################################################
    # CHECK END OF GAME
    def check_end_of_sim(self):
        """Checks if win state conditions have been met"""
        rtn = False

        # Run through all win conditions even if one is True.
        # Two win conditions could come up True in the same turn.
        for win_state in self.win_states:

            r = win_state.check_state()

            if r:
                self.imsgr.add_msg(
                    msgs.Msg(
                        self.tick,
                        "GAME OVER",
                        win_state.get_data("msg"),
                    )
                )
            rtn = rtn or r
        return rtn

        # Only 1 team remaining
        # teams_remaining = []
        # for name,data in self.sides.items():
        #     team_eliminated = True

        #     for obj in data['team']['agents'].values():
        #         if obj.get_data('alive'):
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

    def get_points_data(self):
        """Gets points data"""
        msg = ""
        for name, data in self.sides.items():
            msg += "  TEAM: " + name + "\n"
            total = 0
            for curr_obj in data["team"]["agents"].values():
                msg += (
                    "    "
                    + curr_obj.get_best_display_name()
                    + ": "
                    + str(curr_obj.get_data("points"))
                    + "\n"
                )
                total += curr_obj.get_data("points")
            msg += "    TOTAL: " + str(total) + "\n"

        m = msgs.Msg(str(self.tick), "CURRENT POINTS", msg)
        self.imsgr.add_msg(m)

    def get_final_scores(self):
        """Get final scores"""
        final_scores = {}
        for name, data in self.sides.items():
            team_scores = {"agents": {}, "total": 0}

            for agent_name, curr_obj in data["team"]["agents"].items():
                agent_score = curr_obj.get_data("points")
                team_scores["agents"][curr_obj.get_best_display_name()] = agent_score
                team_scores["total"] += agent_score

            final_scores[name] = team_scores

        return final_scores

    ##########################################################################
    # RUN SIM
    def run_sim(self, turns):
        """Runs sim

        For given number of turns:
        - update view and objects
        - get new sets of commands
        - run through each tick

        For each tick:
        - process commands to run
        - perform action based on action priority
        """
        for turn in range(turns):
            # A place to store the commands by uuid and tick
            cmds_by_uuid = {}

            # get the general view to pass onto objects.
            general_view = self.get_general_view()

            # Run all obj's updates, storing the returned commands
            # Don't need to shuffle order while getting commands
            for obj_uuid, curr_obj in self.objs.items():

                cmd = None
                view = {}
                view["general"] = general_view
                if obj_uuid in self.comp_views:
                    view["comp"] = self.comp_views[obj_uuid]

                # Call update and get commands
                cmd = curr_obj.update(view)

                # Validate commands
                cmd = self.command_validator.validate_commands(cmd)

                if cmd is not None:
                    if type(cmd) is dict and len(cmd) > 0:
                        cmds_by_uuid[obj_uuid] = cmd

            # Flush the obj_views, so no one gets old data.
            self.comp_views = {}

            # Get the list of obj uuids which have issued cmds.
            obj_uuids_list = list(cmds_by_uuid.keys())

            # Run each tick
            for tick in range(self.ticks_per_turn):
                self.imsgr.add_msg(msgs.Msg(self.tick, "---NEW TICK---", ""))

                # Advance turn order sequentially by rotating list of all active agents by 1.
                obj_uuids_list[1:]

                # Check all commands to see if there is
                # something to do this tick.
                # for objuuid,objcmds in cmds_by_uuid.items():
                for objuuid in obj_uuids_list:
                    objcmds = cmds_by_uuid[objuuid]
                    if str(tick) in objcmds:
                        cmds_this_tick = objcmds[str(tick)]
                        self.process_commands(objuuid, cmds_this_tick)

                self.process_updates()

                # Run all actions by type in the order specified in the main
                # config's action_priority
                for ap in self.action_priority_keys:
                    action_type = self.action_priority[ap]

                    cur_actions = self.actions[action_type]

                    # act is a tuple: (obj,action)
                    for act in cur_actions:
                        # Log the action with the object's logger.
                        act[0].log_info(zfunctions.action_to_string(act[1]))
                        # Execute action.
                        self.action_dispatch_table[action_type](act[0], act[1])

                # All actions have been run, now clear action dict.
                self.reset_action_dict()

                # Check if the sim is over.
                if self.check_end_of_sim():
                    return True
                else:
                    self.tick += 1

    def process_commands(self, obj_uuid, cmds):
        """Processes commands

        Only alive objects can perfrom commands
        For each alive object, turn commands into actions
        """
        # Prevents commands from objs destroyed in this tick
        # from taking place.
        if obj_uuid in self.objs:

            curr_obj = self.objs[obj_uuid]

            # Send the commands to the object so they can be
            # processed. This returns a list of actions.
            actions = self.objs[obj_uuid].process_commands(cmds)

            # Dispatch each action to the function that
            # handles its execution.
            for a in actions:

                # Add obj ref and action as a tuple.
                self.actions[a.get_type()].append((curr_obj, a))

                # self.action_dispatch_table[a.getType()](obj,a)

    def process_updates(self):
        """Process updates

        For each item, turn updates into actions
        """
        for objuuid, obj in self.objs.items():

            actions = obj.process_updates()

            for a in actions:

                # Add obj ref and action as a tuple.
                self.actions[a.get_type()].append((obj, a))

    ##########################################################################
    # ACTION PROCESSING FUNCTIONS
    # These handle the meat of turning actions into world changes.
    # All the sexy happens here.
    ##########################################################################

    def actn_highspeed_projectile(self, curr_obj, actn):
        """High-speed projectile action"""
        view = self.view_manager.get_view_template("projectile")
        view["compname"] = actn.get_data("compname")

        # Get list of cells through which the shell travels.
        cells_hit = zmath.get_cells_along_trajectory(
            curr_obj.get_data("x"),
            curr_obj.get_data("y"),
            actn.get_data("direction"),
            actn.get_data("range"),
        )

        # Get the list of cells through which the shell travels.
        damage = random.randint(
            actn.get_data("min_damage"), actn.get_data("max_damage")
        )

        # If there's something in a cell, damage the first thing
        # along the path and quit.
        for cell in cells_hit:
            id_in_cell = self.map.get_cell_occupant(cell[0], cell[1])
            if id_in_cell == curr_obj.get_data("uuid"):
                continue
            elif id_in_cell is not None:

                view["hit_x"] = cell[0]
                view["hit_y"] = cell[1]
                view["name"] = self.objs[id_in_cell].get_data("name")

                damage_str = (
                    curr_obj.get_best_display_name()
                    + " shot "
                    + self.objs[id_in_cell].get_best_display_name()
                    + " for "
                    + str(damage)
                    + " points of damage."
                )
                self.log_msg("DAMAGE", damage_str)

                points = self.damage_obj(id_in_cell, damage)

                curr_obj.set_data("points", points)

                break

        self.add_comp_view(curr_obj.get_data("uuid"), view)

    def actn_move(self, curr_obj, actn):
        """Move action"""
        # Get current data
        facing = curr_obj.get_data("facing")
        cur_speed = actn.get_data("speed")
        old_x = curr_obj.get_data("x")
        old_y = curr_obj.get_data("y")
        old_cell_x = curr_obj.get_data("cell_x")
        old_cell_y = curr_obj.get_data("cell_y")
        x = old_x + old_cell_x
        y = old_y + old_cell_y
        # translate and new data
        new_position = zmath.translate_point(x, y, facing, cur_speed)
        new_x = int(new_position[0])
        new_y = int(new_position[1])
        new_cell_x = abs(new_position[0] - abs(new_x))
        new_cell_y = abs(new_position[1] - abs(new_y))

        # see if move is possible.
        if new_x != old_x or new_y != old_y:

            # Might be moving more than 1 cell. Get trajectory.
            cell_path = zmath.get_cells_along_trajectory(x, y, facing, cur_speed)

            cur_cell = (old_x, old_y)
            collision = False

            # for all cells in the path, update if empty.
            for cell in cell_path:
                if cell == (old_x, old_y):
                    continue
                else:
                    if self.map.is_cell_empty(cell[0], cell[1]):
                        cur_cell = cell
                    else:
                        collision = True
                        break

            new_x = cur_cell[0]
            new_y = cur_cell[1]

            # Move the object
            self.map.move_obj_from_to(
                curr_obj.get_data("uuid"), old_x, old_y, new_x, new_y
            )
            curr_obj.set_data("x", new_x)
            curr_obj.set_data("y", new_y)
            curr_obj.set_data("cell_x", new_cell_x)
            curr_obj.set_data("cell_y", new_cell_y)

            # Update held item's locations
            item_uuids = curr_obj.get_all_held_stored_items()
            for _uuid in item_uuids:
                i = self.items[_uuid]
                i.set_data("x", new_x)
                i.set_data("y", new_y)

            if collision:
                # CRASH INTO SOMETHING

                # We need to move the obj to the edge
                # of the old cell to simulate that they reached the edge of it before
                # crashing.
                if new_x != old_x:
                    if new_x > old_x:
                        curr_obj.set_data("cell_x", 0.99)
                    else:
                        curr_obj.set_data("cell_x", 0.0)
                if new_y != old_y:
                    if new_y > old_y:
                        curr_obj.set_data("cell_y", 0.99)
                    else:
                        curr_obj.set_data("cell_y", 0.0)

        # Didn't leave the cell, update in-cell coords.
        else:
            curr_obj.set_data("cell_x", new_cell_x)
            curr_obj.set_data("cell_y", new_cell_y)
            pass

    # Turns the obj
    def actn_turn(self, curr_obj, actn):
        """Turn action"""
        cur_facing = curr_obj.get_data("facing")
        new_facing = cur_facing + actn.get_data("turnrate")
        while new_facing < 0:
            new_facing += 360
        while new_facing >= 360:
            new_facing -= 360
        curr_obj.set_data("facing", new_facing)

    # Performs a radar transmission
    def actn_transmit_radar(self, curr_obj, actn):
        """Radar transmission action"""
        view = self.view_manager.get_view_template("radar")
        view["tick"] = self.tick
        view["ctype"] = actn.get_data("ctype")
        view["compname"] = actn.get_data("compname")
        view["slot_id"] = actn.get_data("slot_id")

        # Set up the necessary data for easy access
        radar_facing = curr_obj.get_data("facing") + actn.get_data("offset_angle")
        start = radar_facing - actn.get_data("visarc")
        end = radar_facing + actn.get_data("visarc")
        angle = start
        jump = actn.get_data("resolution")
        x = curr_obj.get_data("x")
        y = curr_obj.get_data("y")
        _range = actn.get_data("range")

        temp_view = []

        # While we're in our arc of visibility
        while angle <= end:
            # Get all object/item pings along this angle
            pings = self.map.get_all_obj_uuid_along_trajectory(x, y, angle, _range)
            # Pings should be in order. Start adding if they're not there.
            # If the radar's level is less than the obj's density, stop. We can't see through.
            # Else keep going.
            obj_pings = pings["objects"]
            item_pings = pings["items"]

            for ping in obj_pings:

                # Pinged ourself
                if ping["x"] == curr_obj.get_data("x") and ping[
                    "y"
                ] == curr_obj.get_data("y"):
                    pass
                else:
                    # For now all we're giving the transmitting player
                    # the object name. Up to the player to figure out
                    # if this is a teammate.
                    ping["name"] = self.objs[ping["uuid"]].get_data("name")

                    # Make sure the reported direction is 0-360
                    direction = angle
                    if direction < 0:
                        direction += 360
                    if direction >= 360:
                        direction -= 360

                    ping["direction"] = direction
                    ping["cell_x"] = self.objs[ping["uuid"]].get_data("cell_x")
                    ping["cell_y"] = self.objs[ping["uuid"]].get_data("cell_y")
                    ping["alive"] = self.objs[ping["uuid"]].is_alive()
                    temp_view.append(ping)

                    # If our radar level can't penetrate the object, stop.
                    if actn.get_data("level") < self.objs[ping["uuid"]].get_data(
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
                ping["name"] = item.get_data("name")
                ping["weight"] = item.get_data("weight")
                ping["bulk"] = item.get_data("bulk")
                ping["owner"] = item.get_data("owner")
                temp_view.append(ping)

            if jump == 0:
                break
            else:
                angle += jump

        for ping in temp_view:
            del ping["uuid"]
            view["pings"].append(ping)

        self.add_comp_view(curr_obj.get_data("uuid"), view)

    def actn_broadcast_message(self, curr_obj, actn):
        """Broadcast message action"""
        view = {}
        view["vtype"] = "message"
        view["tick"] = self.tick
        view["message"] = actn.get_data("message")

        for curr_uuid, other_obj in self.objs.items():
            if curr_uuid != curr_obj.get_data("uuid"):

                distance = zmath.distance(
                    curr_obj.get_data("x"),
                    curr_obj.get_data("y"),
                    other_obj.get_data("x"),
                    other_obj.get_data("y"),
                )

                # if the distance to the other obj is less than
                # the broadcast range, add the view.
                if distance <= actn.get_data("range"):
                    self.add_comp_view(curr_uuid, view)

    def actn_take_item(self, curr_obj, actn):
        """Take item action"""
        take_location = actn.get_data("location")

        # If we're taking from the cell,
        # or if a take location was not provided, take from cell.
        if take_location == "cell" or take_location is None:

            obj_x = curr_obj.get_data("x")
            obj_y = curr_obj.get_data("y")
            items_in_obj_cell = self.map.get_items_in_cell(obj_x, obj_y)

            if len(items_in_obj_cell) > 0:
                item_name = actn.get_data("item_name")
                item_index = actn.get_data("item_index")
                item_uuid = actn.get_data("item_uuid")

                matching_item = None

                # If the action provided a specific uuid,
                # look only for that and ignore the other info.
                if item_uuid is not None:
                    if item_uuid in items_in_obj_cell:
                        matching_item = item_uuid

                elif item_name is not None:
                    for item_id in items_in_obj_cell:
                        item = self.items[item_id]
                        if item.get_data("name") == item_name:
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
                    arm_comp = curr_obj.get_comp(actn.get_data("slot_id"))
                    if arm_comp is None:
                        print("ArmComp is None")
                        return

                    if not arm_comp.is_holding_item():
                        if arm_comp.can_take_item(
                            item_to_take.get_data("weight"),
                            item_to_take.get_data("bulk"),
                        ):
                            arm_comp.set_data("item", matching_item)
                            self.map.remove_item(obj_x, obj_y, matching_item)
                            item_to_take.take_item(curr_obj.get_data("uuid"))
                            print("Take successful.")
                        else:
                            print("Item too heavy or bulky.")
                            pass
                    else:
                        print("Arm is already packing.")
                        pass

    def actn_drop_item(self, curr_obj, actn):
        """Drop item action"""
        print("Dropping item")
        obj_x = curr_obj.get_data("x")
        obj_y = curr_obj.get_data("y")

        arm_comp = curr_obj.get_comp(actn.get_data("slot_id"))
        if arm_comp is None:
            return

        if arm_comp.is_holding_item():
            held_item_uuid = arm_comp.get_data("item")
            held_item = self.items[held_item_uuid]

            drop_location = actn.get_data("location")

            # Action must specify a valid drop location before
            # the item is dropped.
            if drop_location == "cell":
                print("Drop successful")
                self.map.add_item(obj_x, obj_y, held_item_uuid)
                arm_comp.set_data("item", None)
                held_item.drop_item()

    ##########################################################################
    # ADDITIONAL HELPER FUNCTIONS
    # Some of the ACTN function do similar work.
    ##########################################################################

    def damage_obj(self, _uuid, damage):
        """Applies damage to object"""
        # Damage object
        points = self.objs[_uuid].damage_obj(damage)

        # If obj is dead, remove it.
        if not self.objs[_uuid].is_alive():

            dead_obj = self.objs[_uuid]

            # Check for held/stored items
            held_items_uuids = dead_obj.get_and_remove_all_held_stored_items()
            for i in held_items_uuids:
                self.map.add_item(dead_obj.get_data("x"), dead_obj.get_data("y"), i)

            # Remove from map
            self.map.remove_obj(
                dead_obj.get_data("x"),
                dead_obj.get_data("y"),
                dead_obj.get_data("uuid"),
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

    def get_obj_draw_data(self):
        """Gets object draw data"""
        dd = []
        for curr_obj in self.destroyed_objs.values():
            dd.append(curr_obj.get_draw_data())
        for curr_obj in self.objs.values():
            dd.append(curr_obj.get_draw_data())
        return dd

    def get_item_draw_data(self):
        """Gets item draw data"""
        dd = []
        for item in self.items.values():
            dd.append(item.get_draw_data())
        return dd

    ##########################################################################
    # SEND MESSAGE TO HANDLER
    ##########################################################################
    # Convenience function to create a message for the UI's log
    def log_msg(self, title, text):
        """Logs message"""
        self.imsgr.add_msg(msgs.Msg(self.tick, title, text))

import importlib.util
import random
import time
import uuid

import obj
import zmath
import msgs
import valid
import views
import zfunctions
import sprite_manager


class Sim:
    def __init__(
            self,
            ldr,
            logger,
            map_template,
            team_side_assignments,
            *args, **kwargs
    ):
        """Initializes default sim values and an empty action dispatch table"""
        self.ldr = ldr
        self.logger = logger
        self.map_template = map_template
        self.map = None
        self.team_side_assignments = team_side_assignments
        self.imsgr = kwargs["imsgr"]
        self.objects = {}
        self.items = {}
        self.destroyed_objs = {}
        self.sides = {}
        self.teams = []
        self.turn = 0
        self.win_states = []
        self.comp_views = {}
        self.actions = {}
        self.action_priority = {}
        self.action_priority_keys = []
        self.agent_turn_order = []
        self.cur_agent_index = None
        self.randomize_order = False
        self.randomise_order_every_turn = False
        self.command_validator = valid.CommandValidator()
        self.action_dispatch_table = {}
        self.build_action_dispatch_table()
        self.view_manager = views.ViewManager()
        self.config = self.ldr.copy_main_config()
        self.build_action_priority(self.config)

    def reset(self):
        """Resets default sim values"""
        self.map = None
        self.team_side_assignments = None
        self.objects = {}
        self.items = {}
        self.destroyed_objs = {}
        self.sides = {}
        self.turn = 0
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
    # def set_map(self, _map):
    #     """Sets map"""
    #     self.world = _map
    #     sides = self.world.get_data("sides")
    #     for k, v in sides.items():
    #         self.add_side(k, v)
    #
    def get_turn(self):
        return self.turn

    def get_map(self):
        """Gets map"""
        return self.map

    def get_objects(self):
        return self.objects

    def get_items(self):
        return self.items

    #
    # def has_map(self):
    #     """Determines if sim has map"""
    #     return self.world is not None
    #
    # ##########################################################################
    # # SIDES
    # def add_side_id(self, ID):
    #     """Adds side id"""
    #     self.sides[ID] = None
    #
    # def add_side(self, ID, side):
    #     """Adds side"""
    #     self.sides[ID] = side
    #     self.sides[ID]["teamname"] = None
    #
    # def get_sides(self):
    #     """Gets sides"""
    #     return self.sides
    #
    # ##########################################################################
    # # TEAMS
    # def add_team_name(self, ID, team_name):
    #     """Adds team name"""
    #     self.sides[ID]["teamname"] = team_name
    #
    # def get_team_name(self, ID):
    #     """Gets team name from id"""
    #     return self.sides[ID]["teamname"]
    #
    # def del_team_name(self, ID):
    #     """Deletes team name"""
    #     self.sides[ID]["teamname"] = None

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

    def build_sim(self):
        self.build_map()
        self.build_teams()

    # BUILD MAP
    def build_map(self):
        map_id = self.map_template["id"]
        self.map = self.ldr.build_map(map_id)

        # Add all edge objects
        edge_obj_id = self.map.get_edge_obj_id()
        map_width = self.map.get_width()
        map_height = self.map.get_height()
        for x in range(map_width):
            new_obj = self.ldr.build_obj(edge_obj_id)
            new_obj.init_basic_data(
                x=x,
                y=0,
                facing=0
            )
            self.objects[new_obj.get_uuid()] = new_obj
            self.map.add_object_to(x, 0, new_obj.get_uuid())

            new_obj = self.ldr.build_obj(edge_obj_id)
            new_obj.init_basic_data(
                x=x,
                y=map_height - 1,
                facing=0
            )
            self.objects[new_obj.get_uuid()] = new_obj
            self.map.add_object_to(x, map_height - 1, new_obj.get_uuid())

        for y in range(map_height):
            new_obj = self.ldr.build_obj(edge_obj_id)
            new_obj.init_basic_data(
                x=0,
                y=y,
                facing=0
            )
            self.objects[new_obj.get_uuid()] = new_obj
            self.map.add_object_to(0, y, new_obj.get_uuid())

            new_obj = self.ldr.build_obj(edge_obj_id)
            new_obj.init_basic_data(
                x=map_width - 1,
                y=y,
                facing=0
            )
            self.objects[new_obj.get_uuid()] = new_obj
            self.map.add_object_to(map_width - 1, y, new_obj.get_uuid())

        # Add all objects
        objects = self.map_template["objects"]
        for o in objects:
            new_obj = self.ldr.build_obj(o["id"])
            new_obj.x = o["x"]  # have to fill these in manually.
            new_obj.y = o["y"]  # probably a better way
            self.objects[new_obj.get_uuid()] = new_obj
            self.map.add_object_to(
                new_obj.get_cell_x(),
                new_obj.get_cell_y(),
                new_obj.get_uuid()
            )

        # Add all placed items
        items = self.map_template["items"]
        for i in items:
            item_id = i["id"]
            new_item = self.ldr.build_item(item_id)
            new_item.init_for_sim(**i)
            self.items[new_item.get_uuid()] = new_item
            self.map.add_item_to(
                new_item.get_cell_x(),
                new_item.get_cell_y(),
                new_item.get_uuid()
            )

    def build_teams(self):

        team_dir = self.config["team_dir"]
        self.sides = self.map_template["sides"]

        for side_id, team_id in self.team_side_assignments.items():

            # Get the side information
            side_data = self.sides[side_id]

            # Create new team object
            new_team = self.ldr.build_team(team_id)
            new_team.set_side_id(side_id)
            new_team.build_triggers(side_data["triggers"], self.items.values())

            # Get team data elements
            team_name = new_team.get_name()
            agent_defs = new_team.get_agent_defs()
            # triggers = new_team.get_triggers()

            starting_locations = side_data["starting_locations"]
            if side_data["random_placement"]:
                random.shuffle(starting_locations)

            for index, ad in enumerate(agent_defs):
                agent_object = self.ldr.build_obj(ad["object"])

                # Build all components
                agent_object.build_comps(self.ldr)

                # Load sprite for object
                agent_sprite_filename = agent_object.get_sprite_filename_based_on_damage()
                agent_sprite = sprite_manager.load_image(agent_sprite_filename)

                # Init sim data
                loc = starting_locations[index]
                # agent_object.init_for_sim(
                #     x=loc["x"],
                #     y=loc["y"],
                #     facing=loc["facing"]
                # )

                # Load and set AI
                ai_file_name = ad["AI_file"]
                ai_spec = importlib.util.spec_from_file_location(
                    ai_file_name,
                    f"{team_dir}/{team_name}/{ai_file_name}"
                )
                ai_module = importlib.util.module_from_spec(ai_spec)
                ai_spec.loader.exec_module(ai_module)
                ai_script = ai_module.AI()

                # Finalize any additional agent data. This also calls the
                # AI script's init and passes on a limited amount of
                # starting data in case AI authors want to do any setup.
                agent_object.init_basic_data(
                    x=loc["x"],
                    y=loc["y"],
                    facing=loc["facing"]
                )

                agent_object.init_agent_data(
                    damage=0,
                    sprite=agent_sprite,
                    ai_script=ai_script,
                    team_name=team_name,
                    callsign=ad["callsign"],
                    squad=ad["squad"]
                )

                ai_script.init_ai(**agent_object.get_self_view())

                # Add the agent to the turn order.
                self.agent_turn_order.append(agent_object)

                # Add to team
                new_team.add_agent(agent_object)

                # Add to objects
                self.objects[agent_object.get_uuid()] = agent_object

                # Add to map at starting location
                self.map.add_object_to(
                    agent_object.get_cell_x(),
                    agent_object.get_cell_y(),
                    agent_object.get_uuid()
                )

            self.teams.append(new_team)

    ##########################################################################
    # Get the world view
    def get_general_view(self):
        """Gets general world view"""
        view = {}
        view["turn"] = self.turn
        return view

    ##########################################################################
    # CHECK END OF GAME
    def calculate_team_points(self, _team):

        team_points_total = 0.0
        for _agent in _team.get_agents():
            team_points_total += _agent.get_points()
        return team_points_total

    def check_end_of_sim(self):
        """Checks if win state conditions have been met"""
        for _team in self.teams:
            side = self.sides[_team.get_side_id()]
            team_points_total = self.calculate_team_points(_team)

            if team_points_total >= side["points_to_win"]:
                return True

        return False

    def get_points_data(self):
        """Gets points data"""
        msg = ""

        for _team in self.teams:
            msg += f"TEAM: {_team.get_name()}\n"
            total_points = 0.0
            for _agent in _team.get_agents():
                agent_name = _agent.get_name()
                points = _agent.get_points()
                total_points += points
                msg += f"   {agent_name}: {points}\n"
            msg += f"   Total: {total_points}\n"

        m = msgs.Msg(str(self.turn), "Current points: ", msg)
        self.imsgr.add_msg(m)

    def get_final_scores(self):
        """Get final scores"""
        final_scores = {}

        for _team in self.teams:
            # side = self.sides[_team.get_side_id()]
            score = self.calculate_team_points(_team)
            final_scores[_team.get_name()] = score

        return final_scores
        #
        # for name, data in self.sides.items():
        #     team_scores = {"agents": {}, "total": 0}
        #
        #     for agent_name, curr_obj in data["team"]["agents"].items():
        #         agent_score = curr_obj.get_data("points")
        #         team_scores["agents"][curr_obj.get_best_display_name()] = \
        #             agent_score
        #         team_scores["total"] += agent_score
        #
        #     final_scores[name] = team_scores
        #
        # return final_scores

    ##########################################################################

    def check_triggers(self):
        """Checks all triggers and awards any points to the object that activated it."""
        for _team in self.teams:
            print(_team.get_name())
            for trgr in _team.get_triggers():
                print(trgr.get_name())
                _obj, points = trgr.check(self.objects)
                if _obj is not None:
                    _obj.add_points(points)
                    print(f"POINTS: {points}")

    def run_next_agent(self, cur_agent):
        cmds = []
        view = self.get_general_view()
        agent_uuid = cur_agent.get_uuid()
        if agent_uuid in self.comp_views:
            view["comp"] = self.comp_views[agent_uuid]
        cmds = cur_agent.update(view)
        return self.command_validator.validate_commands(cmds)

    # RUN SIM
    def run_sim(self, ui, turns, delay):
        """Runs sim

        For given number of turns:
        - update view and objects
        - get new sets of commands
        - run through each turn

        For each turn:
        - process commands to run
        - perform action based on action priority
        """
        for turn in range(turns):
            # A place to store the commands by uuid and turn
            cmds_by_uuid = {}

            # Run all obj's updates, storing the returned commands
            # Don't need to shuffle order while getting commands
            for cur_agent in self.agent_turn_order:
                agent_uuid = cur_agent.get_uuid()
                cmds = self.run_next_agent(cur_agent)
                if cmds is not None:
                    cmds_by_uuid[agent_uuid] = cmds
                ui.draw_object(cur_agent)

            # Flush the obj_views, so no one gets old data.
            self.comp_views = {}

            # Get the list of obj uuids which have issued cmds.
            # obj_uuids_list = list(cmds_by_uuid.keys())

            self.imsgr.add_msg(msgs.Msg(self.turn, "---NEW TURN---", ""))

            self.process_commands(cmds_by_uuid)

            # Check all commands to see if there is
            # something to do this turn.
            # for objuuid,objcmds in cmds_by_uuid.items():
            # for objuuid in obj_uuids_list:
            #     objcmds = cmds_by_uuid[objuuid]
            #     self.process_commands(objuuid, objcmds)

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

            # Check if any actions have completed any triggers
            self.check_triggers()

            # Check if the sim is over.
            if self.check_end_of_sim():
                return True
            else:
                self.turn += 1

    def process_commands(self, cmds):
        """Processes commands

        Only alive objects can perfrom commands
        For each alive object, turn commands into actions
        """
        # Prevents commands from objs destroyed in this turn
        # from taking place.
        for agent_uuid, commands in cmds.items():

            curr_obj = self.objects[agent_uuid]

            # Send the commands to the object so they can be
            # processed. This returns a list of actions.
            actions = curr_obj.process_commands(commands)

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
        for o in self.objects.values():

            actions = o.process_updates()

            for a in actions:
                # Add obj ref and action as a tuple.
                self.actions[a.get_type()].append((o, a))

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
            id_in_cell = self.world.get_cell_occupant(cell[0], cell[1])
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

                curr_obj.add_points(points)

                break

        self.add_comp_view(curr_obj.get_data("uuid"), view)

    def actn_move(self, curr_obj, actn):
        """Move action"""
        # Get current data
        facing = curr_obj.get_facing()
        cur_speed = actn.get_data("speed")
        old_cell_x = curr_obj.get_cell_x()
        old_cell_y = curr_obj.get_cell_y()
        # old_cell_x = curr_obj.get_data("cell_x")
        # old_cell_y = curr_obj.get_data("cell_y")
        x = curr_obj.get_x()
        y = curr_obj.get_y()
        # translate and new data
        new_position = zmath.translate_point(x, y, facing, cur_speed)
        new_x = new_position[0]
        new_y = new_position[1]
        new_cell_x = int(new_x)
        new_cell_y = int(new_y)

        # see if move is possible.
        if new_cell_x != old_cell_x or new_cell_y != old_cell_y:

            # Might be moving more than 1 cell. Get trajectory.
            cell_path = zmath.get_cells_along_trajectory(
                x, y, facing, cur_speed
            )

            cur_cell = (old_cell_x, old_cell_y)
            has_collided = False
            collided_cell = None

            # for all cells in the path, update if empty.
            for cell in cell_path:
                if cell == (old_cell_x, old_cell_y):
                    continue
                else:
                    if not self.map.contains_object(cell[0], cell[1]):
                        cur_cell = cell
                    else:
                        has_collided = True
                        collided_cell = cell
                        break

            new_cell_x = cur_cell[0]
            new_cell_y = cur_cell[1]

            # Move the object
            self.map.move_obj_from_to(
                curr_obj.get_uuid(), old_cell_x, old_cell_y, new_cell_x, new_cell_y
            )

            if has_collided:

                # CRASH INTO SOMETHING
                # dest_cell_x = int(new_x)
                # dest_cell_y = int(new_y)

                if new_x - x != 0.0:
                    a = (new_y - y) / (new_x - x)
                    b = y - a * x

                    # y = ax+b
                    if collided_cell[0] != new_cell_x and collided_cell[1] == new_cell_y:
                        if collided_cell[0] < new_cell_x:
                            new_x = float(new_cell_x)
                            new_y = a * new_x + b
                        else:
                            new_x = new_cell_x + 0.999
                            new_y = a * new_x + b
                    elif collided_cell[0] == new_cell_x and collided_cell[1] != new_cell_y:
                        if collided_cell[1] < new_cell_y:
                            new_y = float(new_cell_y)
                            new_x = (new_y - b) / a
                        else:
                            new_y = new_cell_y + 0.999
                            new_x = (new_y - b) / a
                    elif collided_cell[0] != new_cell_x and collided_cell[1] != new_cell_y:
                        if collided_cell[0] < new_cell_x:
                            new_x = float(new_cell_x)
                            new_y = a * new_x + b
                        else:
                            new_x = new_cell_x + 0.999
                            new_y = a * new_x + b
                        if collided_cell[1] < new_cell_y:
                            new_y = float(new_cell_y)
                            new_x = (new_y - b) / a
                        else:
                            new_y = new_cell_y + 0.999
                            new_x = (new_y - b) / a

                else:
                    new_x = x

            curr_obj.set_x(new_x)
            curr_obj.set_y(new_y)

            curr_obj.set_redraw(True)

            # Update held item's locations
            item_uuids = curr_obj.get_all_held_stored_items()
            for _uuid in item_uuids:
                i = self.items[_uuid]
                i.set_x(new_x)
                i.set_y(new_y)
                i.set_redraw(True)



        # Didn't leave the cell, update in-cell coords.
        else:
            curr_obj.set_x(new_x)
            curr_obj.set_y(new_y)

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
        curr_obj.set_redraw(True)

    # Performs a radar transmission
    def actn_transmit_radar(self, curr_obj, actn):
        """Radar transmission action"""
        view = self.view_manager.get_view_template("radar")
        view["turn"] = self.turn
        view["ctype"] = actn.get_data("ctype")
        view["compname"] = actn.get_data("compname")
        view["slot_id"] = actn.get_data("slot_id")

        # Set up the necessary data for easy access
        radar_facing = curr_obj.get_data("facing") + \
                       actn.get_data("offset_angle")
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
            pings = self.world.get_all_obj_uuid_along_trajectory(
                x, y, angle, _range
            )
            # Pings should be in order. Start adding if they're not there.
            # If the radar's level is less than the obj's density, stop.
            # We can't see through.
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
                    if actn.get_data("level") < \
                            self.objs[ping["uuid"]].get_data("density"):
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
        view["turn"] = self.turn
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
            items_in_obj_cell = self.world.get_items_in_cell(obj_x, obj_y)

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
                        # print("ArmComp is None")
                        return

                    if not arm_comp.is_holding_item():
                        if arm_comp.can_take_item(
                                item_to_take.get_data("weight"),
                                item_to_take.get_data("bulk"),
                        ):
                            arm_comp.set_data("item", matching_item)
                            self.world.remove_item(obj_x, obj_y, matching_item)
                            item_to_take.take_item(curr_obj.get_data("uuid"))
                            matching_item.redraw(True)
                            # print("Take successful.")
                        else:
                            # print("Item too heavy or bulky.")
                            pass
                    else:
                        # print("Arm is already packing.")
                        pass

    def actn_drop_item(self, curr_obj, actn):
        """Drop item action"""
        # print("Dropping item")
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
                # print("Drop successful")
                self.world.add_item(obj_x, obj_y, held_item_uuid)
                arm_comp.set_data("item", None)
                held_item.drop_item()
                held_item.redraw(True)

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
                self.world.add_item(
                    dead_obj.get_data("x"),
                    dead_obj.get_data("y"),
                    i
                )

            # Remove from map
            self.world.remove_obj(
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
    # SEND MESSAGE TO HANDLER
    ##########################################################################
    # Convenience function to create a message for the UI's log
    def log_msg(self, title, text):
        """Logs message"""
        self.imsgr.add_msg(msgs.Msg(self.turn, title, text))

import ai_helpers as aih
import random


class AI:
    def __init__(self):
        None

    def init_data(self, sim_data):
        # Store the sim_data in case we need to reference something.
        self.sim_data = sim_data

        # Create a CmdMaker obj
        self.cmd_maker = aih.CmdMaker()

        # Set our state
        self.state = 0

        # #################################
        # Stored data
        self.is_initd = False
        self.gamemap = {}
        self.slots_by_ctype = None
        self.tick = 0

    def init_run_time(self, view):
        self.is_initd = True
        self.slots_by_ctype = aih.get_slot_ids_by_ctype(view)

    def get_slot(self, ctype):
        return self.slots_by_ctype[ctype][0]

    def update_map(self, view):

        loc = (aih.get_x(view), aih.get_y(view))

        if loc not in self.gamemap:
            self.gamemap[loc] = None
        else:
            pass

    def distance(self, locA, locB):
        return ((locB[0] - locA[0]) ** 2 + (locB[1] - locA[1]) ** 2) ** 0.5

    def check_for_enemy_obj(self, view, objname):
        pings = aih.search_radar_for_obj_name(view, "Blue Tank")

        # If we see the blue tank, shoot!
        if len(pings) > 0:
            if aih.can_weapon_fire(view, self.get_slot("FixedGun")):
                self.cmd_maker.add_cmd(0, self.get_slot("FixedGun"), aih.cmd_fire())

        # Always check if we need to reload.
        if aih.does_weapon_need_reloading(view, self.get_slot("FixedGun")):
            self.cmd_maker.add_cmd(0, self.get_slot("FixedGun"), aih.cmd_reload())

    def determine_next_move(self, view):
        pings = aih.search_radar_for_obj_name(view, "Indestructible Block")
        myloc = (aih.get_x(view), aih.get_y(view))
        if len(pings) > 0:

            objloc = (pings[0]["x"], pings[0]["y"])
            dist = self.distance(objloc, myloc)
            engine_slots = self.slots_by_ctype["Engine"]
            turn_rate = 0.0
            speed = 0.0

            for es in engine_slots:
                engine_comp = aih.get_comp_by_slot_id(view, es)
                turn_rate += engine_comp["cur_turnrate"]
                speed += engine_comp["cur_speed"]

            # If we're far from an indestructible block...
            if dist > 2:
                # First, if we're turning, stop.
                if turn_rate < 0 or turn_rate > 0:
                    self.cmd_maker.add_cmd(
                        self.tick, self.get_slot("Engine"), aih.cmd_turn(0.0)
                    )
                # If we're standing still, move.
                elif speed == 0:
                    self.cmd_maker.add_cmd(
                        self.tick, self.get_slot("Engine"), aih.cmd_set_speed(1.0)
                    )
                # Otherwise, 10% of the time, turn a random amount left or right.
                elif random.random() < 0.1:
                    self.cmd_maker.add_cmd(
                        self.tick,
                        self.get_slot("Engine"),
                        aih.cmd_turn(random.uniform(-36.0, 36.0)),
                    )
            # If we're close to a block, we want to stop moving forward
            # and turn.
            elif dist <= 2:
                # Stop moving
                if speed > 0:
                    self.cmd_maker.add_cmd(
                        self.tick, self.get_slot("Engine"), aih.cmd_set_speed(0.0)
                    )
                # Turn in a random direction 18 deg per turn (or 1/20th of a circle).
                if turn_rate == 0:
                    self.cmd_maker.add_cmd(
                        self.tick,
                        self.get_slot("Engine"),
                        aih.cmd_turn(random.choice([-18.0, 18.0])),
                    )

    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def run_ai(self, view):

        self.cmd_maker.reset()

        if not self.is_initd:
            self.init_run_time(view)

            self.cmd_maker.add_cmd(
                self.tick, self.get_slot("Radar"), aih.cmd_activate_radar()
            )

        self.update_map(view)

        self.check_for_enemy_obj(view, "Blue Tank")

        self.determine_next_move(view)

        return self.cmd_maker.get_cmds()

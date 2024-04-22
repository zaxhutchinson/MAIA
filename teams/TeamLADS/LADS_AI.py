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
        self.start_performed = False
        self.cmd_start_iteration = 0
        self.cmd_iteration = 0
        self.start_cmd_set = []

        self.start_cmds_a = [
            aih.cmd_turn(-45),
            aih.cmd_turn(0),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(0),
            aih.cmd_turn(45),
            aih.cmd_turn(0),
            aih.cmd_turn(0),
        ]

        self.start_cmds_b = [
            aih.cmd_turn(90),
            aih.cmd_turn(45),
            aih.cmd_turn(0),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(0),
            aih.cmd_turn(45),
            aih.cmd_turn(0),
            aih.cmd_turn(0),
        ]

        self.cmd = [
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(1),
            aih.cmd_set_speed(0),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(30),
            aih.cmd_turn(0),
            aih.cmd_turn(0),
        ]

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
        pings = aih.search_radar_for_obj_name(view, "Red Tank")

        # If we see the blue tank, shoot!
        if len(pings) > 0:
            if aih.can_weapon_fire(view, self.get_slot("FixedGun")):
                self.cmd_maker.add_cmd(0, self.get_slot("FixedGun"), aih.cmd_fire())

        # Always check if we need to reload.
        if aih.does_weapon_need_reloading(view, self.get_slot("FixedGun")):
            self.cmd_maker.add_cmd(0, self.get_slot("FixedGun"), aih.cmd_reload())

    def determine_next_move(self, view):
        self.cmd_maker.add_cmd(
            self.tick, self.get_slot("Engine"), self.cmd[self.cmd_iteration]
        )
        self.cmd_iteration += 1
        if len(self.cmd) <= self.cmd_iteration:
            self.cmd_iteration = 0

    # Performs appropriate start actions based on starting location
    def startAction(self, view):
        self.cmd_maker.add_cmd(
            self.tick,
            self.get_slot("Engine"),
            self.start_cmd_set[self.cmd_start_iteration],
        )
        self.cmd_start_iteration += 1
        return len(self.start_cmd_set) <= self.cmd_start_iteration

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

        if (aih.get_x(view), aih.get_y(view)) == (1, 13):
            self.start_cmd_set = self.start_cmds_a
        elif (aih.get_x(view), aih.get_y(view)) == (13, 1):
            self.start_cmd_set = self.start_cmds_b

        if not (self.start_performed):
            self.start_performed = self.startAction(view)

        if self.start_performed:
            self.check_for_enemy_obj(view, "Red Tank")
            self.determine_next_move(view)

        return self.cmd_maker.get_cmds()

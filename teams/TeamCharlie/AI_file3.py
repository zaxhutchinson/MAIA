import ai_helpers as aih


class AI:
    def __init__(self):
        None

    def initData(self, sim_data):
        # Store the sim_data in case we need to reference something.
        self.sim_data = sim_data

        # Create a CmdMaker obj
        self.cmd_maker = aih.CmdMaker()

        # Set our state
        self.state = 0

    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def run_ai(self, view):

        self.cmd_maker.reset()

        # The prettyPrintView() function can be used to see what the agent
        # is receiving. Prints to the console.
        # aih.prettyPrintView(view)

        # Ping the radar.
        # print("--------------AI TURN--------------")

        if self.state == 0:
            self.cmd_maker.add_cmd(0, 2, aih.cmd_activate_radar())
            self.state += 1

        comp_views = aih.get_sub_view(view, "comp")

        if comp_views is not None:

            pings = []

            for cv in comp_views:
                if cv["vtype"] == "radar":

                    pings += cv["pings"]

            # self_view = aih.getSubView(view,'self')

            ############################################################
            # Have we run into an object?
            # If so turn...
            need_to_turn = False
            engine_view = aih.get_comp_by_slot_id(view, "1")

            for ping in pings:
                if ping["type"] == "object":
                    if ping["distance"] < 2.0:
                        if engine_view["cur_speed"] != 0:
                            self.cmd_maker.add_cmd(0, 1, aih.cmd_set_speed(0.0))
                        else:
                            self.cmd_maker.add_cmd(0, 1, aih.cmd_turn(90.0))
                        need_to_turn = True

            if not need_to_turn:
                if engine_view["cur_turnrate"] != 0:
                    self.cmd_maker.add_cmd(0, 1, aih.cmd_turn(0.0))
                else:
                    self.cmd_maker.add_cmd(0, 1, aih.cmd_set_speed(2.0))

            # # If not, make sure we're not turning.
            # if not turning:
            #     print("NULL TURNING")
            #     self.cmd_maker.add_cmd(0,1,aih.cmd_turm(0.0))

            #     # Since we're not turning, move forward.
            #     self.cmd_maker.add_cmd(0,1,aih.cmd_set_speed(1.0))

        return self.cmd_maker.get_cmds()

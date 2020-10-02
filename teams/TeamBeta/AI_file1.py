import ai_helpers as aih

class AI:
    def __init__(self):
        None
        
    def initData(self,sim_data):
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
    def runAI(self,view):

        self.cmd_maker.reset()

        # The prettyPrintView() function can be used to see what the agent
        # is receiving. Prints to the console.
        # aih.prettyPrintView(view)

        # Ping the radar.
        # print("--------------AI TURN--------------")

        if self.state == 0:
            self.cmd_maker.addCmd(0,2,aih.CMD_ActivateRadar())
            self.state+=1


        comp_views = aih.getSubView(view,'comp')
    
        if comp_views != None:

            pings = []

            for cv in comp_views:
                if cv['vtype']=='radar':
                    
                    pings+=cv['pings']

            #self_view = aih.getSubView(view,'self')

            ############################################################
            # Have we run into an object?
            # If so turn...
            need_to_turn = False
            engine_view = aih.getCompBySlotID(view,'1')

            for ping in pings:
                if ping['type']=='object':
                    if ping['distance'] < 2.0:
                        if engine_view['cur_speed'] != 0:
                            self.cmd_maker.addCmd(0,1,aih.CMD_SetSpeed(0.0))
                        else:
                            self.cmd_maker.addCmd(0,1,aih.CMD_Turn(90.0))
                        need_to_turn = True

            if not need_to_turn:
                if engine_view['cur_turnrate'] != 0:
                    self.cmd_maker.addCmd(0,1,aih.CMD_Turn(0.0))
                else:
                    self.cmd_maker.addCmd(0,1,aih.CMD_SetSpeed(1.0))

            # # If not, make sure we're not turning.
            # if not turning:
            #     print("NULL TURNING")
            #     self.cmd_maker.addCmd(0,1,aih.CMD_Turn(0.0))

            #     # Since we're not turning, move forward.
            #     self.cmd_maker.addCmd(0,1,aih.CMD_SetSpeed(1.0))

        return self.cmd_maker.getCmds()

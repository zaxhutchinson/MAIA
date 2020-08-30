import ai_helpers as aih

class AI:
    def __init__(self):
        None
        
    def initData(self,sim_data):
        self.sim_data = sim_data

        self.cmd_maker = aih.CmdMaker()

        self.state = 0
    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def runAI(self,data):
        #self.cmd_maker.addCmd(0,2,aih.CMD_SetSpeed(1.0))
        if self.state==0:
            self.cmd_maker.addCmd(0,5,aih.CMD_TakeItem('blue flag',0))
            self.cmd_maker.addCmd(0,2,aih.CMD_SetSpeed(1.0))
            self.state +=1
        elif self.state == 5:
            self.cmd_maker.addCmd(0,5,aih.CMD_DropItem('cell'))
            self.state+=1
        else:
            self.state+=1


        return self.cmd_maker.getCmds()

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
    def runAI(self, view):

        return self.cmd_maker.getCmds()

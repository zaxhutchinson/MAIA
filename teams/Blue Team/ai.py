import ai_helpers as aih
import random


class AI:
    # ===========================================================================================================
    # DO NOT ALTER THESE TWO FUNCTIONS
    def __init__(self):
        self.team_name = None
        self.callsign = None
        self.squad = None
        self.x = None
        self.y = None
        self.facing = None
        self.damage = None
        self.health = None

    def update(self, **kwargs):
        """Called every turn with updated information provided by the simulation.
        NOTE: if location data is disabled, x,y will be None.
        """
        self.team_name = kwargs["team_name"]
        self.callsign = kwargs["callsign"]
        self.squad = kwargs["squad"]
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.facing = kwargs["facing"]
        self.damage = kwargs["damage"]
        self.health = kwargs["health"]

    #
    # ===========================================================================================================

    def init_ai(self, **kwargs):
        """This function is called once the agent object has been fully configured for the match,
        but before the match actually starts. Use this function to initialize your ai. This function
        should not return anything.

        DO NOT ALTER THE HEADER OF THIS FUNCTION."""
        self.cmd_maker = aih.CmdMaker()

    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def run_ai(self, view):
        self.cmd_maker.reset()
        
        return self.cmd_maker.get_cmds()

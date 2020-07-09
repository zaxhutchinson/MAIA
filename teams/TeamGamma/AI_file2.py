class AI:
    def __init__(self):
        None
        
    def initData(self,team_name, sim_data, starting_region):
        self.team_name = team_name,
        self.sim_data = sim_data
        self.starting_region = starting_region
        print(team_name)
        print(sim_data)
        print(starting_region)

        # MUST PICK STARTING LOCATION BASED ON THE STARTING_REGION INFO
        # MUST RETURN THE STARTING X,Y COORD as tuple
        return (0.0,0.0)


    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def runAI(self,data):
        return {}


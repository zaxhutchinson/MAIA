from log import *
import agent

class Team:
    def __init__(self,data):
        self.data={}
        self.required_data=[]
        self.agents = {}

        self.setData(data)

        self.setAgents()

    def setData(self,data):

        req_data = [
            'name','size','agents'
        ]

        for rd in req_data:
            if rd in data:
                self.data[rd] = data[rd]
            else:
                self.data[rd] = None
                LogError("TEAM: Missing data "+rd)

        self.required_data += req_data

    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def setAgents(self):
        agents = self.getData('agents')
        
        if agents == None:
            LogError("AGENT: Agent data is missing.")
        else:
            for ID,data in agents.items():
                ID = int(ID)
                objid = data['object']
                ai_filename = data['AI_file']

                _agent = agent.Agent(ID,objid,ai_filename)
                

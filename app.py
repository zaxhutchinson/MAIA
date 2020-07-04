import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import importlib.util
import sys
import os

import sim
import loader

class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("MAIA - Maine AI Arena")

        self.sim = sim.Sim()
        self.loader = loader.Loader(self.sim)

        

        self.team_names = self.sim.getTeamNames()
        self.team_names_to_play = []
        self.map_names = self.sim.getMapNames()
        self.map_selection = None
        self.combat_log = []

        self.BuildUI()

    def Run(self):
        self.mainloop()

    def BuildUI(self):
        #######################################################################
        ## MAP UI
        #######################################################################
        self.mapSelectFrame = tk.Frame(self,relief=tk.RAISED,borderwidth=2)
        self.mapSelectFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.lbMaps = tk.Listbox(self.mapSelectFrame,selectmode=tk.SINGLE)
        self.lbMaps.pack(side=tk.LEFT,fill=tk.Y,expand=True)

        self.btnSelectMap = tk.Button(self.mapSelectFrame,text="Select Map",command=self.selectMap,bg='sky blue')
        self.btnSelectMap.pack(side=tk.LEFT,fill=tk.Y)

        self.txtMapInfo = tk.scrolledtext.ScrolledText(self.mapSelectFrame,wrap = tk.WORD)
        self.txtMapInfo.pack(side=tk.LEFT,fill=tk.Y)
        self.txtMapInfo.insert(tk.END,"No map info")

        self.updateMapNames()
        #######################################################################
        ## TEAM UI
        ######################################################################
        self.teamFrame = tk.Frame(self,relief=tk.RAISED,borderwidth=2)
        self.teamFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.teamPoolFrame = tk.Frame(self.teamFrame)
        self.teamPoolFrame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.lblTeamPool = tk.Label(self.teamPoolFrame,text="Team Pool")
        self.lblTeamPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbTeams = tk.Listbox(self.teamPoolFrame,selectmode=tk.SINGLE)
        self.lbTeams.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        self.playPoolFrame = tk.Frame(self.teamFrame)
        self.playPoolFrame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.lblPlayPool = tk.Label(self.playPoolFrame,text="Play Pool")
        self.lblPlayPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbTeamsToPlay = tk.Listbox(self.playPoolFrame,selectmode=tk.SINGLE)
        self.lbTeamsToPlay.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        self.updateTeamNames()

        self.pack(fill=tk.BOTH,expand=True)

        self.btnAddTeam = tk.Button(self.teamFrame, text="Add Team >>>", command=self.addTeam,bg='lime green')
        self.btnAddTeam.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.btnRemoveTeam = tk.Button(self.teamFrame,text="<<< Remove Team", command=self.removeTeam,bg='deep pink')
        self.btnRemoveTeam.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        #######################################################################
        ## SIM UI
        #######################################################################
        self.fmSimUI = tk.Frame(self,relief=tk.RAISED,borderwidth=2)
        self.fmSimUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.btnBuildSim = tk.Button(self.fmSimUI,text="Build Sim",command=self.buildSim)
        self.btnBuildSim.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.btnRunSim = tk.Button(self.fmSimUI,text="Run Sim",command=self.runSim)
        self.btnRunSim.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

    def updateTeamNames(self):
        self.lbTeams.delete(0,tk.END)
        self.lbTeamsToPlay.delete(0,tk.END)
        for name in self.team_names:
            self.lbTeams.insert(tk.END,name)
        for name in self.team_names_to_play:
            self.lbTeamsToPlay.insert(tk.END,name)

    def updateMapNames(self):
        self.lbMaps.delete(0,tk.END)
        for name in self.map_names:
            self.lbMaps.insert(tk.END,name)

    def addTeam(self):
        if self.sim.isMapReady():
            teams = self.map_selection.getData('teams')
            if teams > len(self.team_names_to_play):
                curselection = self.lbTeams.curselection()
                if len(curselection) > 0:
                    name_to_add = self.team_names.pop(curselection[0])
                    self.team_names_to_play.append(name_to_add)
                    self.updateTeamNames()
    def removeTeam(self):
        curselection = self.lbTeamsToPlay.curselection()
        if len(curselection) > 0:
            name_to_remove = self.team_names_to_play.pop(curselection[0])
            self.team_names.append(name_to_remove)
            self.updateTeamNames()
    def removeAllTeams(self):
        while len(self.team_names_to_play) > 0:
            t = self.team_names_to_play.pop()
            self.team_names.append(t)

    def selectMap(self):
        curselection = self.lbMaps.curselection()
        if len(curselection) > 0:
            self.sim.setMapInPlay(self.sim.getMapNames()[curselection[0]])
            self.map_selection = self.sim.mapInPlay
            mapInfoString =  "NAME:   "+self.map_selection.getData('name')+'\n'
            mapInfoString += "DESC:   "+self.map_selection.getData('desc')+'\n'
            mapInfoString += "WIDTH:  "+str(self.map_selection.getData('width'))+'\n'
            mapInfoString += "HEIGHT: "+str(self.map_selection.getData('height'))+'\n'
            mapInfoString += "TEAMS:  "+str(self.map_selection.getData('teams'))+'\n'
            mapInfoString += "AGENTS: "+str(self.map_selection.getData('agents'))+'\n'
            mapInfoString += "RANDOMLY PLACED OBJECTS:\n"
            if 'rand_objects' in self.map_selection.data:
                for k,v in self.map_selection.data['rand_objects'].items():
                    mapInfoString +='   ID:' + str(k) + ' AMT:'+str(v) + '\n'
            else:
                mapInfoString += '   NONE\n'
            mapInfoString += "HAND-PLACED OBJECTS\n"
            if 'placed_objects' in self.map_selection.data:
                for k,v in self.map_selection.data['placed_objects'].items():
                    mapInfoString += '   ID:' + str(k) + ' AMT:' + str(len(v)) + '\n'
            else:
                mapInfoString += '   NONE\n'
            self.txtMapInfo.delete('1.0',tk.END)
            self.txtMapInfo.insert(tk.END,mapInfoString)

            self.removeAllTeams()
            self.updateTeamNames()

    def buildSim(self):
        if self.sim.isMapReady():
            self.sim.clearTeamsInPlay()
            for t in self.team_names_to_play:
                self.sim.buildTeam(t)

    def runSim(self):
        pass
import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import importlib.util
import sys
import os

import sim
import loader
from log import *
import ui_map

class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("MAIA - Maine AI Arena")

        self.ldr = loader.Loader()
        self.sim = sim.Sim()

        self.combat_log = []

        self.BuildUI()

        self.UIMap = None

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

        self.lbTeams = tk.Listbox(self.teamPoolFrame,selectmode=tk.SINGLE,exportselection=0)
        self.lbTeams.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        self.playPoolFrame = tk.Frame(self.teamFrame)
        self.playPoolFrame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.lblPlayPool = tk.Label(self.playPoolFrame,text="Play Pool")
        self.lblPlayPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.subPlayPoolFrame = tk.Frame(self.playPoolFrame)
        self.subPlayPoolFrame.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

        self.lbSideNames = tk.Listbox(self.subPlayPoolFrame,selectmode=tk.SINGLE,exportselection=0)
        self.lbSideNames.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.lbTeamAssignments = tk.Listbox(self.subPlayPoolFrame,selectmode=tk.NONE)
        self.lbTeamAssignments.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

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

        self.btnRunSimWithUI = tk.Button(self.fmSimUI,text="Run Sim With UI",command=self.runSimWithUI)
        self.btnRunSimWithUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.btnRunSimWithoutUI = tk.Button(self.fmSimUI,text="Run Sim Without UI",command=self.runSimWithoutUI)
        self.btnRunSimWithoutUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

    def updateTeamNames(self):
        self.lbTeams.delete(0,tk.END)
        self.lbSideNames.delete(0,tk.END)
        self.lbTeamAssignments.delete(0,tk.END)
        for name in self.ldr.getTeamIDs():
            self.lbTeams.insert(tk.END,name)
        for k,v in self.sim.getSides().items():
            self.lbSideNames.insert(tk.END,k)
            self.lbTeamAssignments.insert(tk.END,str(self.sim.getTeam(k)))

    def updateMapNames(self):
        self.lbMaps.delete(0,tk.END)
        for name in self.ldr.getMapIDs():
            self.lbMaps.insert(tk.END,name)

    def selectMap(self):
        curselection = self.lbMaps.curselection()
        if len(curselection) > 0:
            # Reset the sim
            self.sim.reset()

            # Locate the map, copy and give to sim
            map_ids = self.ldr.getMapIDs()
            selected_map = self.ldr.copyMapTemplate(map_ids[curselection[0]])
            self.sim.setMap(selected_map)

            # Construct the map info string
            mapInfoString =  "NAME:   "+selected_map.getData('name')+'\n'
            mapInfoString += "DESC:   "+selected_map.getData('desc')+'\n'
            mapInfoString += "WIDTH:  "+str(selected_map.getData('width'))+'\n'
            mapInfoString += "HEIGHT: "+str(selected_map.getData('height'))+'\n'
            mapInfoString += "TEAMS:  "+str(selected_map.getData('teams'))+'\n'
            mapInfoString += "AGENTS: "+str(selected_map.getData('agents'))+'\n'
            mapInfoString += "RANDOMLY PLACED OBJECTS:\n"
            if 'rand_objects' in selected_map.data:
                for k,v in selected_map.data['rand_objects'].items():
                    mapInfoString +='   ID:' + str(k) + ' AMT:'+str(v) + '\n'
            else:
                mapInfoString += '   NONE\n'
            mapInfoString += "HAND-PLACED OBJECTS\n"
            if 'placed_objects' in selected_map.data:
                for k,v in selected_map.data['placed_objects'].items():
                    mapInfoString += '   ID:' + str(k) + ' AMT:' + str(len(v)) + '\n'
            else:
                mapInfoString += '   NONE\n'

            # Add string to the info text box
            self.txtMapInfo.delete('1.0',tk.END)
            self.txtMapInfo.insert(tk.END,mapInfoString)
            
            self.updateTeamNames()

    def addTeam(self):
        if self.sim.hasMap():
            team_index = self.lbTeams.curselection()
            side_index = self.lbSideNames.curselection()
            if len(team_index) > 0 and len(side_index) > 0:

                all_sides = self.lbSideNames.get(0,tk.END)
                side_selection = all_sides[side_index[0]]
                team_name = self.ldr.getTeamIDs()[team_index[0]]
                
                self.sim.addTeam(side_selection,team_name)
                self.updateTeamNames()
            else:
                LogError("App::addTeam() - No side or team selected.")
        else:
            LogError("App::addTeam() - Sim is missing the map.")
    def removeTeam(self):
        side_index = self.lbSideNames.curselection()
        if len(side_index) > 0:
            all_sides = self.lbSideNames.get(0,tk.END)
            side_ID = all_sides[side_index[0]]
            self.sim.delTeam(side_ID)
            self.updateTeamNames()




    def buildSim(self):
        self.sim.buildSim(self.ldr)

    def runSimWithUI(self):
        map_width=self.sim.getMap().getData('width')
        map_height=self.sim.getMap().getData('height')
        self.UIMap = ui_map.UIMap(map_width,map_height,self)

    def runSimWithoutUI(self):
        self.sim.runSim()
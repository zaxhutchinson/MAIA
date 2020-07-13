import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import importlib.util
import sys
import os
import queue

import sim
import loader
from log import *
import ui_map
import msgs
from zexceptions import *

class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master

        self.main_bgcolor='gray10'
        self.main_fgcolor='LightBlue1'
        
        self.configure(bg=self.main_bgcolor)
        self.pack()
        self.master.title("MAIA - Maine AI Arena")

        # Create the msgr objs
        self.msg_queue = queue.Queue()
        self.imsgr = msgs.IMsgr(self.msg_queue)
        self.omsgr = msgs.OMsgr(self.msg_queue)

        self.ldr = loader.Loader()
        self.sim = sim.Sim(self.imsgr)

        

        self.combat_log = []

        self.BuildUI()

        self.UIMap = None

    def Run(self):
        self.mainloop()

    def BuildUI(self):
        #######################################################################
        ## MAP UI
        #######################################################################
        self.mapSelectFrame = tk.Frame(self,relief=tk.FLAT,borderwidth=0,highlightthickness=0,highlightbackground="black")
        self.mapSelectFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.lbMaps = tk.Listbox(self.mapSelectFrame,selectmode=tk.SINGLE,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black",relief=tk.FLAT,selectforeground=self.main_bgcolor,selectbackground=self.main_fgcolor)
        self.lbMaps.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.btnSelectMap = tk.Button(self.mapSelectFrame,text="Select Map",command=self.selectMap,bg='midnight blue',fg='light sky blue',activeforeground='midnight blue',activebackground='light sky blue',highlightthickness=0,highlightbackground="black",relief=tk.FLAT)
        self.btnSelectMap.pack(side=tk.LEFT,fill=tk.BOTH,expand=False)

        self.txtMapInfo = tk.scrolledtext.ScrolledText(self.mapSelectFrame,wrap = tk.WORD,relief=tk.FLAT,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black")
        self.txtMapInfo.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.txtMapInfo.insert(tk.END,"No map info")

        self.updateMapNames()
        #######################################################################
        ## TEAM UI
        ######################################################################
        self.teamFrame = tk.Frame(self,relief=tk.FLAT,borderwidth=0)
        self.teamFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.teamPoolFrame = tk.Frame(self.teamFrame)
        self.teamPoolFrame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.teamPoolLeftFrame = tk.Frame(self.teamPoolFrame)
        self.teamPoolLeftFrame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.lblTeamPool = tk.Label(self.teamPoolLeftFrame,text="TEAM POOL",bg=self.main_bgcolor,fg=self.main_fgcolor)
        self.lblTeamPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbTeams = tk.Listbox(self.teamPoolLeftFrame,selectmode=tk.SINGLE,exportselection=0,relief=tk.FLAT,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black",selectforeground=self.main_bgcolor,selectbackground=self.main_fgcolor)
        self.lbTeams.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.teamPoolRightFrame = tk.Frame(self.teamPoolFrame)
        self.teamPoolRightFrame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.lblSides= tk.Label(self.teamPoolRightFrame,text="SIDES",bg=self.main_bgcolor,fg=self.main_fgcolor)
        self.lblSides.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbSideNames = tk.Listbox(self.teamPoolRightFrame,selectmode=tk.SINGLE,exportselection=0,relief=tk.FLAT,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black",selectforeground=self.main_bgcolor,selectbackground=self.main_fgcolor)
        self.lbSideNames.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)


        # self.lbTeams = tk.Listbox(self.teamPoolFrame,selectmode=tk.SINGLE,exportselection=0,relief=tk.FLAT,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black")
        # self.lbTeams.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        

        self.playPoolFrame = tk.Frame(self.teamFrame)
        self.playPoolFrame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.lblPlayPool = tk.Label(self.playPoolFrame,text="ASSIGNED TEAMS",bg=self.main_bgcolor,fg=self.main_fgcolor)
        self.lblPlayPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.subPlayPoolFrame = tk.Frame(self.playPoolFrame)
        self.subPlayPoolFrame.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

        

        self.lbTeamAssignments = tk.Listbox(self.subPlayPoolFrame,selectmode=tk.NONE,bg=self.main_bgcolor,fg=self.main_fgcolor,relief=tk.FLAT,highlightthickness=0,highlightbackground="black",selectforeground=self.main_bgcolor,selectbackground=self.main_fgcolor)
        self.lbTeamAssignments.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.updateTeamNames()

        self.pack(fill=tk.BOTH,expand=True)

        self.btnAddTeam = tk.Button(self.teamFrame, text="Add Team >>>",command=self.addTeam,bg='dark green',fg='pale green',activeforeground='dark green',activebackground='pale green',highlightthickness=0,highlightbackground="black",relief=tk.FLAT)
        self.btnAddTeam.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.btnRemoveTeam = tk.Button(self.teamFrame,text="<<< Remove Team", command=self.removeTeam,bg='red4',fg='tomato2',activeforeground='red4',activebackground='tomato2',highlightthickness=0,highlightbackground="black",relief=tk.FLAT)
        self.btnRemoveTeam.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        #######################################################################
        ## SIM UI
        #######################################################################
        self.fmSimUI = tk.Frame(self,relief=tk.FLAT,borderwidth=0)
        self.fmSimUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.btnBuildSim = tk.Button(self.fmSimUI,text="Build Sim",command=self.buildSim,bg='midnight blue',fg='light sky blue',activeforeground='midnight blue',activebackground='light sky blue',highlightthickness=0,highlightbackground="black",relief=tk.FLAT)
        self.btnBuildSim.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.btnRunSimWithUI = tk.Button(self.fmSimUI,text="Run Sim With UI",command=self.runSimWithUI,bg='midnight blue',fg='light sky blue',activeforeground='midnight blue',activebackground='light sky blue',highlightthickness=0,highlightbackground="black",relief=tk.FLAT)
        self.btnRunSimWithUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        # self.btnRunSimWithoutUI = tk.Button(self.fmSimUI,text="Run Sim Without UI",command=self.runSimWithoutUI)
        # self.btnRunSimWithoutUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

    def updateTeamNames(self):
        self.lbTeams.delete(0,tk.END)
        self.lbSideNames.delete(0,tk.END)
        self.lbTeamAssignments.delete(0,tk.END)
        for name in self.ldr.getTeamIDs():
            self.lbTeams.insert(tk.END,name)
        for k,v in self.sim.getSides().items():
            self.lbSideNames.insert(tk.END,k)
            self.lbTeamAssignments.insert(tk.END,str(self.sim.getTeamName(k)))

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
                
                self.sim.addTeamName(side_selection,team_name)
                self.updateTeamNames()
            else:
                LogError("App::addTeam() - No side or team selected.")
        else:
            LogError("App::addTeam() - Sim is missing the map.")
    def removeTeam(self):
        # side_index = self.lbSideNames.curselection()
        # if len(side_index) > 0:
        #     all_sides = self.lbSideNames.get(0,tk.END)
        #     side_ID = all_sides[side_index[0]]
        #     self.sim.delTeamName(side_ID)
        #     self.updateTeamNames()

        team_index = self.lbTeamAssignments.curselection()
        if len(team_index) > 0:
            all_sides = self.lbSideNames.get(0,tk.END)
            side_ID = all_sides[team_index[0]]
            self.sim.delTeamName(side_ID)
            self.updateTeamNames()


    def buildSim(self):
        try:
            self.sim.buildSim(self.ldr)
        except BuildException as e:
            tk.messagebox.showinfo(title="Build Exception",message=e)
        else:
            tk.messagebox.showinfo(title="Success",message="Sim build was successful.")

    def runSimWithUI(self):
        map_width=self.sim.getMap().getData('width')
        map_height=self.sim.getMap().getData('height')
        self.UIMap = ui_map.UIMap(map_width,map_height,self.sim,self.omsgr,self)

    def runSimWithoutUI(self):
        self.sim.runSim(self.ldr.getMainConfigData('no_ui_max_turns'))
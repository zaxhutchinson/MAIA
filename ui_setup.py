import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import importlib.util
import sys
import os
import queue
import logging

import sim
import loader
import ui_sim
import msgs
from zexceptions import *
from ui_widgets import *


class UISetup(tk.Frame):
    def __init__(self,master=None,logger=None,parent=None):
        tk.Frame.__init__(self,parent)
        self.master = master
        self.logger = logger

        self.configure(bg=DARKCOLOR)
        #self.pack()
        self.master.title("MAIA - Maine AI Arena")

        # Create the msgr objs
        self.msg_queue = queue.Queue()
        self.imsgr = msgs.IMsgr(self.msg_queue)
        self.omsgr = msgs.OMsgr(self.msg_queue)

        self.ldr = loader.Loader(self.logger)
        self.sim = sim.Sim(self.imsgr)

        # log.LogInit()
        # log_setting = self.ldr.getMainConfigData('debug')
        # if type(log_setting)==bool:
        #     log.LogSetDebug(log_setting)
        #     log.LogDebug("DEBUG IS ON")
        

        self.combat_log = []

        self.BuildUI()

        self.UIMap = None


    def BuildUI(self):
        #######################################################################
        ## MAP UI
        #######################################################################
        self.mapSelectFrame = uiQuietFrame(master=self)
        self.mapSelectFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.lbMaps = uiListBox(self.mapSelectFrame)
        self.lbMaps.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.btnSelectMap = uiButton(master=self.mapSelectFrame,command=self.selectMap,text="Select Map")
        self.btnSelectMap.pack(side=tk.LEFT,fill=tk.BOTH,expand=False)

        self.txtMapInfo = uiScrollText(self.mapSelectFrame)
        self.txtMapInfo.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.txtMapInfo.insert(tk.END,"No map info")

        self.updateMapNames()
        #######################################################################
        ## TEAM UI
        ######################################################################
        self.teamFrame = uiQuietFrame(master=self)
        self.teamFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.teamPoolFrame = uiQuietFrame(master=self.teamFrame)
        self.teamPoolFrame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.teamPoolLeftFrame = uiQuietFrame(master=self.teamPoolFrame)
        self.teamPoolLeftFrame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.lblTeamPool = uiLabel(master=self.teamPoolLeftFrame,text="TEAM POOL")
        self.lblTeamPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbTeams = uiListBox(self.teamPoolLeftFrame)
        self.lbTeams.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.teamPoolRightFrame = uiQuietFrame(master=self.teamPoolFrame)
        self.teamPoolRightFrame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.lblSides= uiLabel(master=self.teamPoolRightFrame,text="SIDES")
        self.lblSides.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbSideNames = uiListBox(self.teamPoolRightFrame)
        self.lbSideNames.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)


        # self.lbTeams = tk.Listbox(self.teamPoolFrame,selectmode=tk.SINGLE,exportselection=0,relief=tk.FLAT,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black")
        # self.lbTeams.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        

        self.playPoolFrame = uiQuietFrame(master=self.teamFrame)
        self.playPoolFrame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.lblPlayPool = uiLabel(master=self.playPoolFrame,text="ASSIGNED TEAMS")
        self.lblPlayPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.subPlayPoolFrame = uiQuietFrame(master=self.playPoolFrame)
        self.subPlayPoolFrame.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

        

        self.lbTeamAssignments = uiListBox(self.subPlayPoolFrame)
        self.lbTeamAssignments.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.updateTeamNames()

        self.pack(fill=tk.BOTH,expand=True)

        self.btnAddTeam = uiButton(master=self.teamFrame, text="Add Team >>>",command=self.addTeam)
        self.btnAddTeam.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.btnRemoveTeam = uiButton(master=self.teamFrame,text="<<< Remove Team", command=self.removeTeam)
        self.btnRemoveTeam.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        #######################################################################
        ## SIM UI
        #######################################################################
        self.fmSimUI = uiQuietFrame(master=self)
        self.fmSimUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True,padx=10,pady=10)

        self.btnBuildSim = uiButton(master=self.fmSimUI,command=self.buildSim,text="Build Sim")
        self.btnBuildSim.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.btnRunSimWithUI = uiButton(master=self.fmSimUI,command=self.runSimWithUI,text="Run Sim With UI")
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
                self.logger.error("App::addTeam() - No side or team selected.")
        else:
            self.logger.error("App::addTeam() - Sim is missing the map.")
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
        self.UIMap = ui_sim.UISim(map_width,map_height,self.sim,self.omsgr,self,self.logger)

    def runSimWithoutUI(self):
        self.sim.runSim(self.ldr.getMainConfigData('no_ui_max_turns'))
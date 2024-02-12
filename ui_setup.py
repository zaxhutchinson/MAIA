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
import ui_advanced_config
import msgs
from zexceptions import *
from ui_widgets import *


#Henry Taking some stuff from stack overflow:
def callback(event):
    selection = event.widget.curselection()
    if selection:

        print("Hello world") #okay so this works, but self.selectMap wont sork cuase on self

class UISetup(tk.Frame):
    def __init__(self,master=None,logger=None):
        super().__init__(master)
        self.master = master
        self.logger = logger

        self.configure(bg=BGCOLOR) #bg is background i think
        self.pack() 
        self.master.title("MAIA - Maine AI Arena") #top of window tool bar

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

    def Run(self):
        self.mainloop()

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
    # this function is what happens when you hit button "select map" #moved it up here so that it could be bound to selecting map in BuildUI
    def selectMap(self, event): 
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

    

    def BuildUI(self):

        ## PAGE TITLE

        self.pageTitle = uiLabel(master=self, text = "CONFIGURATION")
        self.pageTitle.pack(side=tk.TOP)


        #######################################################################
        ## SIM UI
        #######################################################################
        self.fmSimUI = uiQuietFrame(master=self)
        self.fmSimUI.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True,padx=10,pady=10) #maybe remove padding? maybe remove whole frame, and make button part of master frame?
        

        #below four lines were replaced by below fifth and sixth line

        # self.btnBuildSim = uiButton(master=self.fmSimUI,command=self.buildSim,text="Build Sim")
        # self.btnBuildSim.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        # self.btnRunSimWithUI = uiButton(master=self.fmSimUI,command=self.runSimWithUI,text="Run Sim With UI")
        # self.btnRunSimWithUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.startBtnFrame = uiQuietFrame(master=self.fmSimUI)
        self.startBtnFrame.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True) #expand without fill is a lot of black space

        self.advancedConfigBtnFrame = uiQuietFrame(master=self.fmSimUI)
        self.advancedConfigBtnFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) #having expand set to false is same as not having it

        self.btnBuildAndRunSim = uiButton(master=self.startBtnFrame,command=self.buildAndRunSim,text="Start Game") #Start Game Button
        self.btnBuildAndRunSim.pack(side=tk.RIGHT,padx=50,fill=tk.BOTH, expand=True)

        self.btnAdvancedConfig = uiButton(master=self.advancedConfigBtnFrame,command=self.runAdvancedSettings,text="Advanced Config") #have to change command later to navigate to advanced config
        self.btnAdvancedConfig.pack(side=tk.LEFT,padx=50,fill=tk.BOTH, expand =True)

        # self.btnRunSimWithoutUI = tk.Button(self.fmSimUI,text="Run Sim Without UI",command=self.runSimWithoutUI)
        # self.btnRunSimWithoutUI.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)


        #######################################################################
        ## MAP UI
        #######################################################################
        self.mapFrame = uiQuietFrame(master=self)  #map section 
        self.mapFrame.pack(side=tk.LEFT, fill=tk.BOTH,padx=10, pady=10) #HK set side to left 

        self.mapListFrame =uiQuietFrame(master=self.mapFrame) 
        self.mapListFrame.pack(side=tk.TOP, fill = tk.BOTH)

        self.lblMapList = uiLabel(master=self.mapListFrame,text="MAPS")
        self.lblMapList.pack(side=tk.TOP, fill=tk.BOTH)

        self.lbMaps = uiListBox(self.mapListFrame)  #this is the box that says Map 1 lbMaps
        self.lbMaps.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.lbMaps.bind("<<ListboxSelect>>", self.selectMap) #this calls selectMap(self, whateverMapIsSelectedInTheBox)

        #self.btnSelectMap = uiButton(master=self.mapSelectFrame,command=self.selectMap,text="Select Map") #button 
        #self.btnSelectMap.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=False)

        self.mapInfoFrame = uiQuietFrame(master=self.mapFrame)
        self.mapInfoFrame.pack(side=tk.BOTTOM)

        self.lblMapInfo = uiLabel(master=self.mapInfoFrame,text="MAP INFORMATION")
        self.lblMapInfo.pack(side=tk.TOP, fill=tk.BOTH)

        self.txtMapInfo = uiScrollText(self.mapInfoFrame) #info on selcted frame
        self.txtMapInfo.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        self.txtMapInfo.insert(tk.END,"No map info")

        self.updateMapNames()# this function call gets Map 1 (later other maps) into the box   
        
        #self.selectMap()

        #######################################################################
        ## TEAM UI
        ######################################################################
        self.teamFrame = uiQuietFrame(master=self) #team frame is everything team UI #top line creates frame
        self.teamFrame.pack_propagate(0)
        self.teamFrame.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True,padx=10,pady=10) #bottom line is frame settings

        self.teamPoolFrame = uiQuietFrame(master=self.teamFrame) #Left half of team frame
        self.teamPoolFrame.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.teamPoolLeftFrame = uiQuietFrame(master=self.teamPoolFrame) # part of pool frame, pool section
        self.teamPoolLeftFrame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.lblTeamPool = uiLabel(master=self.teamPoolLeftFrame,text="TEAM POOL") #label that says "Team Pool" section of pool left frame
        self.lblTeamPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbTeams = uiListBox(self.teamPoolLeftFrame)
        self.lbTeams.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        #self.lbTeams.bind("<<ListboxSelect>>", self.)

        self.teamPoolRightFrame = uiQuietFrame(master=self.teamPoolFrame) #pool right frame is the sides section, also part of Pool Frame
        self.teamPoolRightFrame.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        self.lblSides= uiLabel(master=self.teamPoolRightFrame,text="SIDES")
        self.lblSides.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.lbSideNames = uiListBox(self.teamPoolRightFrame)
        self.lbSideNames.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)


        # self.lbTeams = tk.Listbox(self.teamPoolFrame,selectmode=tk.SINGLE,exportselection=0,relief=tk.FLAT,bg=self.main_bgcolor,fg=self.main_fgcolor,highlightthickness=0,highlightbackground="black")
        # self.lbTeams.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        

        self.playPoolFrame = uiQuietFrame(master=self.teamFrame) # Assigned is other half of team frame, "Play pool" is teams that are playing
        self.playPoolFrame.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

        self.playPoolFrameRight = uiQuietFrame(master=self.playPoolFrame)
        self.playPoolFrameRight.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady = 5)

        self.lblPlayPool = uiLabel(master=self.playPoolFrameRight,text="ASSIGNED TEAMS")
        self.lblPlayPool.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        self.subPlayPoolFrame = uiQuietFrame(master=self.playPoolFrameRight)
        self.subPlayPoolFrame.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

        

        self.lbTeamAssignments = uiListBox(self.subPlayPoolFrame)
        self.lbTeamAssignments.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)

        self.updateTeamNames()

        self.pack(fill=tk.BOTH,expand=True)

        #self.playPoolFrameLeft = uiQuietFrame(master=self.playPoolFrame)
        #self.playPoolFrameLeft.pack(side=tk.LEFT)

        self.btnAddTeam = uiButton(master=self.playPoolFrame, text="Add Team >>>",command=self.addTeam)
        self.btnAddTeam.pack(side=tk.TOP,fill=tk.BOTH,expand=True, pady =5)

        self.btnRemoveTeam = uiButton(master=self.playPoolFrame,text="<<< Remove Team", command=self.removeTeam)
        self.btnRemoveTeam.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True, pady=5)

        
        
        
        

    def updateTeamNames(self):
        self.lbTeams.delete(0,tk.END)
        self.lbSideNames.delete(0,tk.END)
        self.lbTeamAssignments.delete(0,tk.END)
        for name in self.ldr.getTeamIDs():
            self.lbTeams.insert(tk.END,name)
        for k,v in self.sim.getSides().items():
            self.lbSideNames.insert(tk.END,k)
            self.lbTeamAssignments.insert(tk.END,str(self.sim.getTeamName(k)))

    def updateMapNames(self): #this function gets all maps from the JSON and puts them in the box list
        self.lbMaps.delete(0,tk.END)
        for name in self.ldr.getMapIDs():
            self.lbMaps.insert(tk.END,name)


   
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

    #def runSimWithUI(self):
     #   map_width=self.sim.getMap().getData('width')
      #  map_height=self.sim.getMap().getData('height')
       # self.UIMap = ui_sim.UISim(map_width,map_height,self.sim,self.omsgr,self,self.logger)


    #def runSimWithoutUI(self):
     #   self.sim.runSim(self.ldr.getMainConfigData('no_ui_max_turns'))

    def buildAndRunSim(self): #combined above two methods
        try:
            self.sim.buildSim(self.ldr)
            print("try")
        except BuildException as e:
            tk.messagebox.showinfo(title="Build Exception",message=e)
            print("except")
        else:
            #tk.messagebox.showinfo(title="Success",message="Sim build was successful.")    --this line makes a pop up
            map_width=self.sim.getMap().getData('width')
            map_height=self.sim.getMap().getData('height')
            self.UIMap = ui_sim.UISim(map_width,map_height,self.sim,self.omsgr,self,self.logger)
            print("else")


    def runAdvancedSettings(self):
        self.UIMap = ui_advanced_config.UISettings(self,self.logger)

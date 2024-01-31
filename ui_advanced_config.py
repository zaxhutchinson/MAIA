import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging
import loader
import json
import comp
import obj

from ui_widgets import *

class UISettings(tk.Toplevel):
    def __init__(self,master=None,logger=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=DARKCOLOR)
        self.title("MAIA - Advanced Configuration")
        self.geometry("800x600")
        self.logger=logger
        self.ldr = loader.Loader(self.logger)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.BuildUI()


    def BuildUI(self):
        
        #Make main containers
        self.titleFrame = uiQuietFrame(master=self)
        self.bottomFrame = uiQuietFrame(master=self)
        self.teamsColumn = uiQuietFrame(master=self.bottomFrame)
        self.componentsColumn = uiQuietFrame(master=self.bottomFrame)
        self.objectsColumn = uiQuietFrame(master=self.bottomFrame)
        self.mapsColumn = uiQuietFrame(master=self.bottomFrame)
        
        #Make Widgets
        self.titleLabel = uiLabel(master=self.bottomFrame, text="Advanced Settings")
        
        self.selectTeamCombo = uiComboBox(master=self.teamsColumn)
        self.teamsLabel = uiLabel(master=self.teamsColumn, text="Teams")
        self.teamSizeLabel = uiLabel(master=self.teamsColumn, text="Size:")
        self.teamSizeEntry = uiEntry(master=self.teamsColumn)
        self.teamNameLabel = uiLabel(master=self.teamsColumn,text="Name:")
        self.teamNameEntry = uiEntry(master=self.teamsColumn)
        
        self.selectComponentCombo = uiComboBox(master=self.componentsColumn)
        self.componentsLabel = uiLabel(master=self.componentsColumn, text="Components")
        self.componentsUpdateButton = uiButton(master=self.componentsColumn,command="",text="Update")
        self.componentsIDLabel = uiLabel(master=self.componentsColumn, text="ID:")
        self.componentsIDEntry = uiEntry(master=self.componentsColumn)
        self.componentsNameLabel = uiLabel(master=self.componentsColumn, text="Name:")
        self.componentsNameEntry = uiEntry(master=self.componentsColumn)
        self.componentsCTypeLabel = uiLabel(master=self.componentsColumn,text="CType:")
        self.componentsTypeLabel = uiLabel(master=self.componentsColumn,text="")
        self.componentsCmdPerTickLabel = uiLabel(master=self.componentsColumn,text="Max Commands Per Tick:")
        self.componentsCmdPerTickEntry = uiEntry(master=self.componentsColumn)
        self.componentsTypeCombo = uiComboBox(master=self.componentsColumn)

        self.selectObjectsCombo = uiComboBox(master=self.objectsColumn)
        self.objectsLabel = uiLabel(master=self.objectsColumn, text="Objects")
        self.objectsUpdateButton = uiButton(master=self.objectsColumn,command="",text="Update")
        self.objectsIDLabel = uiLabel(master=self.objectsColumn, text="ID:")
        self.objectsIDEntry = uiEntry(master=self.objectsColumn)
        self.objectsNameLabel = uiLabel(master=self.objectsColumn, text="Name:")
        self.objectsNameEntry = uiEntry(master=self.objectsColumn)
        self.objectsFillAliveLabel = uiLabel(master=self.objectsColumn, text="Fill Alive:")
        self.objectsFillAliveEntry = uiEntry(master=self.objectsColumn,)
        self.objectsFillDeadLabel = uiLabel(master=self.objectsColumn, text="Fill Dead:")
        self.objectsFillDeadEntry = uiEntry(master=self.objectsColumn)
        self.objectsTextLabel = uiLabel(master=self.objectsColumn, text="Text:")
        self.objectsTextEntry = uiEntry(master=self.objectsColumn)
        self.objectsHealthLabel = uiLabel(master=self.objectsColumn,text="Health:")
        self.objectsHealthEntry = uiEntry(master=self.objectsColumn)
        self.objectsDensityLabel = uiLabel(master=self.objectsColumn,text="Density:")
        self.objectsDensityEntry = uiEntry(master=self.objectsColumn)
        self.objectsCompIDsLabel = uiLabel(master=self.objectsColumn,text="Comp IDs:")
        self.objectsCompIDsEntry = uiEntry(master=self.objectsColumn)
        self.objectsPointsCountLabel = uiLabel(master=self.objectsColumn,text="Points Count:")
        self.objectsPointsCountEntry = uiEntry(master=self.objectsColumn)

        self.selectMapsCombo = uiComboBox(master=self.mapsColumn)
        self.mapsLabel = uiLabel(master=self.mapsColumn, text="Maps")
        self.mapsUpdateButton = uiButton(master=self.mapsColumn,command="",text="Update")
        self.mapsIDLabel = uiLabel(master=self.mapsColumn, text="ID:")
        self.mapsIDEntry = uiEntry(master=self.mapsColumn)
        self.mapsNameLabel = uiLabel(master=self.mapsColumn, text="Name:")
        self.mapsNameEntry = uiEntry(master=self.mapsColumn)
        self.mapsEdgeObjIDLabel = uiLabel(master=self.mapsColumn, text="Edge Object ID:")
        self.mapsEdgeObjIDEntry = uiEntry(master=self.mapsColumn)
        self.mapsDescLabel = uiLabel(master=self.mapsColumn,text="Desc:")
        self.mapsDescEntry = uiEntry(master=self.mapsColumn)
        self.mapsWidthLabel = uiLabel(master=self.mapsColumn,text="Width:")
        self.mapsWidthEntry = uiEntry(master=self.mapsColumn)
        self.mapsHeightLabel = uiLabel(master=self.mapsColumn,text="Height:")
        self.mapsHeightEntry = uiEntry(master=self.mapsColumn)



        #Set locations of widgets in containers
        
        self.bottomFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.titleLabel.pack(side=tk.TOP,fill=tk.BOTH,expand=False,padx=10,pady=10)
        

        self.selectComponentCombo.pack(side=tk.LEFT,padx=10,pady=10)
        self.selectObjectsCombo.pack(side=tk.LEFT,padx=10,pady=10)
        self.selectMapsCombo.pack(side=tk.LEFT,padx=10,pady=10)

        self.teamsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.selectTeamCombo.grid(row=1,column=1,columnspan=2,padx=10,pady=10,ipadx=10,ipady=10)
        self.teamsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.teamSizeLabel.grid(row=3,column=1,sticky="nsew")
        self.teamSizeEntry.grid(row=3,column=2,sticky="nsew")
        self.teamNameLabel.grid(row=4,column=1,sticky="nsew")
        self.teamNameEntry.grid(row=4,column=2,sticky="nsew")

        self.agentFrame = uiQuietFrame(master=self.teamsColumn, borderwidth=5,  relief="ridge",sticky="nsew")
        self.agentFrame.grid(row=5,column=1,columnspan=2,rowspan=2,sticky="nsew", ipadx=0,ipady=0)
        self.callsignLabel = uiLabel(master=self.agentFrame,text="Callsign:")
        self.callsignLabel.grid(row=1,column=1,sticky="nsew")
        self.callsignEntry = uiEntry(master=self.agentFrame)
        self.callsignEntry.grid(row=1,column=2,sticky="nsew")
        self.squadLabel = uiLabel(master=self.agentFrame,text="Squad:")
        self.squadLabel.grid(row=2,column=1,sticky="nsew")
        self.squadEntry = uiEntry(master=self.agentFrame)
        self.squadEntry.grid(row=2,column=2,sticky="nsew")
        self.agentObjectLabel = uiLabel(master=self.agentFrame,text="Object:")
        self.agentObjectLabel.grid(row=3,column=1,sticky="nsew")
        self.agentObjectEntry = uiEntry(master=self.agentFrame)
        self.agentObjectEntry.grid(row=3,column=2,sticky="nsew")
        self.aiFileLabel = uiLabel(master=self.agentFrame,text="AI File:")
        self.aiFileLabel.grid(row=4,column=1,sticky="nsew")
        self.aiFileEntry = uiEntry(master=self.agentFrame)
        self.aiFileEntry.grid(row=4,column=2,sticky="nsew")

        self.teamsUpdateButton = uiButton(master=self.teamsColumn,command=self.updateTeamsJSON, text="update")
        self.teamsUpdateButton.grid(row=7,column=1,columnspan=2,sticky="nsew",ipadx=10,ipady=10,padx=10,pady=10)


        self.componentsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.selectComponentCombo.grid(row=1,column=1,columnspan=2,padx=10,pady=10,ipadx=10,ipady=10)
        self.componentsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.componentsIDLabel.grid(row=3,column=1,sticky="nsew")
        self.componentsIDEntry.grid(row=3,column=2,sticky="nsew")
        self.componentsNameLabel.grid(row=4,column=1,sticky="nsew")
        self.componentsNameEntry.grid(row=4,column=2,sticky="nsew")
        self.componentsCTypeLabel.grid(row=5,column=1,sticky="nsew")
        self.componentsTypeLabel.grid(row=5,column=2,sticky="nsew")
        self.componentsCmdPerTickLabel.grid(row=6,column=1,sticky="nsew")
        self.componentsCmdPerTickEntry.grid(row=6,column=2,sticky="nsew")
        self.componentsTypeCombo.grid(row=7,column=1,columnspan=2,sticky="nsew")
        self.componentsUpdateButton.grid(row=8,column=1,columnspan=2,sticky="nsew")
 
        self.objectsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.selectObjectsCombo.grid(row=1,column=1,columnspan=2,padx=10,pady=10,ipadx=10,ipady=10)
        self.objectsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.objectsIDLabel.grid(row=3,column=1,sticky="nsew")
        self.objectsIDEntry.grid(row=3,column=2,sticky="nsew")
        self.objectsNameLabel.grid(row=4,column=1,sticky="nsew")
        self.objectsNameEntry.grid(row=4,column=2,sticky="nsew")
        self.objectsFillAliveLabel.grid(row=5,column=1,sticky="nsew")
        self.objectsFillAliveEntry.grid(row=5,column=2,sticky="nsew")
        self.objectsFillDeadLabel.grid(row=6,column=1,sticky="nsew")
        self.objectsFillDeadEntry.grid(row=6,column=2,sticky="nsew")
        self.objectsTextLabel.grid(row=7,column=1,sticky="nsew")
        self.objectsTextEntry.grid(row=7,column=2,sticky="nsew")
        self.objectsHealthLabel.grid(row=8,column=1,sticky="nsew")
        self.objectsHealthEntry.grid(row=8,column=2,sticky="nsew")
        self.objectsDensityLabel.grid(row=9,column=1,sticky="nsew")
        self.objectsDensityEntry.grid(row=9,column=2,sticky="nsew")
        self.objectsCompIDsLabel.grid(row=10,column=1,sticky="nsew")
        self.objectsCompIDsEntry.grid(row=10,column=2,sticky="nsew")
        self.objectsPointsCountLabel.grid(row=11,column=1,sticky="nsew")
        self.objectsPointsCountEntry.grid(row=11,column=2,sticky="nsew")
        self.objectsUpdateButton.grid(row=10,column=1,columnspan=2)
   
        self.mapsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.selectMapsCombo.grid(row=1,column=1,columnspan=2,padx=10,pady=10,ipadx=10,ipady=10)
        self.mapsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.mapsIDLabel.grid(row=3,column=1,sticky="nsew")
        self.mapsIDEntry.grid(row=3,column=2,sticky="nsew")
        self.mapsNameLabel.grid(row=4,column=1,sticky="nsew")
        self.mapsNameEntry.grid(row=4,column=2,sticky="nsew")
        self.mapsEdgeObjIDLabel.grid(row=5,column=1,sticky="nsew")
        self.mapsEdgeObjIDEntry.grid(row=5,column=2,sticky="nsew")
        self.mapsDescLabel.grid(row=6,column=1,sticky="nsew")
        self.mapsDescEntry.grid(row=6,column=2,sticky="nsew")
        self.mapsWidthLabel.grid(row=7,column=1,sticky="nsew")
        self.mapsWidthEntry.grid(row=7,column=2,sticky="nsew")
        self.mapsHeightLabel.grid(row=8,column=1,sticky="nsew")
        self.mapsHeightEntry.grid(row=8,column=2,sticky="nsew")
        self.mapsUpdateButton.grid(row=9,column=1,columnspan=2)

        self.initEntryWidgets()

    def initEntryWidgets(self):

        self.teamData=self.ldr.team_templates
        self.teamNames = self.ldr.getTeamNames()
        self.selectTeamCombo.configure(values=self.teamNames)
        self.selectTeamCombo.current(0)
        self.selectTeamCombo.bind("<<ComboboxSelected>>", self.updateTeamEntryWidgets)
        self.teamNameEntry.insert(0,self.teamNames[0])
        self.teamSizeEntry.insert(0,self.teamData[self.teamNames[0]]['size'])
        self.callsignEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['callsign'])
        self.squadEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['squad'])
        self.agentObjectEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['object'])
        self.aiFileEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['AI_file'])

        self.componentData=self.ldr.comp_templates
        self.componentIDs=self.ldr.getCompIDs()
        self.componentTypes=self.ldr.getCompTypes()
        self.selectComponentCombo.configure(values=self.componentIDs)
        self.selectComponentCombo.current(0)
        self.selectComponentCombo.bind("<<ComboboxSelected>>", self.updateComponentsEntryWidgets)
        self.componentsIDEntry.insert(0,self.componentIDs[0])
        self.componentsNameEntry.insert(0,self.componentData[self.componentIDs[0]].getData('name'))
        self.componentsTypeCombo.configure(values=self.componentTypes)
        self.componentsTypeCombo.set(self.componentData[self.componentIDs[0]].getData('ctype'))
        self.componentsCmdPerTickEntry.insert(0,self.componentData[self.componentIDs[0]].getData('max_cmds_per_tick'))

        self.objectData = self.ldr.obj_templates
        self.objectIDs = self.ldr.getObjIDs()
        self.selectObjectsCombo.configure(values=self.objectIDs, state='readonly')
        self.selectObjectsCombo.current(0)
        self.selectObjectsCombo.bind("<<ComboboxSelected>>", self.updateObjectsEntryWidgets)
        self.objectsIDEntry.insert(0,self.objectData[self.objectIDs[0]].getData('id'))
        self.objectsNameEntry.insert(0,self.objectData[self.objectIDs[0]].getData('name'))
        self.objectsFillAliveEntry.insert(0,self.objectData[self.objectIDs[0]].getData('fill_alive'))
        self.objectsFillDeadEntry.insert(0,self.objectData[self.objectIDs[0]].getData('fill_dead'))
        self.objectsTextEntry.insert(0,self.objectData[self.objectIDs[0]].getData('text'))
        self.objectsHealthEntry.insert(0,self.objectData[self.objectIDs[0]].getData('health'))
        self.objectsDensityEntry.insert(0,self.objectData[self.objectIDs[0]].getData('density'))
        self.objectsCompIDsEntry.insert(0,self.objectData[self.objectIDs[0]].getData('comp_ids'))
        self.objectsPointsCountEntry.insert(0,self.objectData[self.objectIDs[0]].getData('points_count'))

        self.mapData = self.ldr.map_templates
        self.mapIDs = self.ldr.getMapIDs()
        self.selectMapsCombo.configure(values=self.mapIDs)
        self.selectMapsCombo.current(0)
        self.selectMapsCombo.bind("<<ComboboxSelected>>", self.updateMapsEntryWidgets)
        self.mapsIDEntry.insert(0,self.mapIDs[0])
        self.mapsNameEntry.insert(0,self.mapData[self.mapIDs[0]].getData('name'))
        self.mapsEdgeObjIDEntry.insert(0,self.mapData[self.mapIDs[0]].getData('edge_obj_id'))
        self.mapsDescEntry.insert(0,self.mapData[self.mapIDs[0]].getData('desc'))
        self.mapsWidthEntry.insert(0,self.mapData[self.mapIDs[0]].getData('width'))
        self.mapsHeightEntry.insert(0,self.mapData[self.mapIDs[0]].getData('height'))


    def updateTeamEntryWidgets(self, v):
        currentTeamIdx = self.selectTeamCombo.current()
        self.teamNameEntry.delete(0,tk.END)
        self.teamNameEntry.insert(0,self.teamNames[currentTeamIdx])
        self.teamSizeEntry.delete(0,tk.END)
        self.teamSizeEntry.insert(0,self.teamData[self.teamNames[0]]['size'])
        self.callsignEntry.delete(0,tk.END)
        self.callsignEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['callsign'])
        self.squadEntry.delete(0,tk.END)
        self.squadEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['squad'])
        self.agentObjectEntry.delete(0,tk.END)
        self.agentObjectEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['object'])
        self.aiFileEntry.delete(0,tk.END)
        self.aiFileEntry.insert(0,self.teamData[self.teamNames[0]]['agent_defs'][0]['AI_file'])
   
    def updateComponentsEntryWidgets(self, v):
        currentComponentIdx = self.selectComponentCombo.current()
        self.componentsIDEntry.delete(0,tk.END)
        self.componentsIDEntry.insert(0,self.componentIDs[currentComponentIdx])
        self.componentsNameEntry.delete(0,tk.END)
        self.componentsNameEntry.insert(0,self.componentData[self.componentIDs[currentComponentIdx]].getData('name'))
        self.componentsTypeCombo.configure(values=self.componentTypes)
        self.componentsTypeCombo.set(self.componentData[self.componentIDs[currentComponentIdx]].getData('ctype'))
        self.componentsCmdPerTickEntry.delete(0,tk.END)
        self.componentsCmdPerTickEntry.insert(0,self.componentData[self.componentIDs[currentComponentIdx]].getData('max_cmds_per_tick'))

    def updateObjectsEntryWidgets(self, v):
        currentObjectIdx = self.selectObjectsCombo.current()
        self.objectsIDEntry.delete(0,tk.END)
        self.objectsIDEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('id'))
        self.objectsNameEntry.delete(0,tk.END)
        self.objectsNameEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('name'))
        self.objectsFillAliveEntry.delete(0,tk.END)
        self.objectsFillAliveEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('fill_alive'))
        self.objectsFillDeadEntry.delete(0,tk.END)
        self.objectsFillDeadEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('fill_dead'))
        self.objectsTextEntry.delete(0,tk.END)
        self.objectsTextEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('text'))
        self.objectsHealthEntry.delete(0,tk.END)
        self.objectsHealthEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('health'))
        self.objectsDensityEntry.delete(0,tk.END)
        self.objectsDensityEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('density'))
        self.objectsCompIDsEntry.delete(0,tk.END)
        self.objectsCompIDsEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('comp_ids'))
        self.objectsPointsCountEntry.delete(0,tk.END)
        self.objectsPointsCountEntry.insert(0,self.objectData[self.objectIDs[currentObjectIdx]].getData('points_count'))

    def updateMapsEntryWidgets(self, v):
        currentMapIdx = self.selectMapsCombo.current()
        self.mapsIDEntry.delete(0,tk.END)
        self.mapsIDEntry.insert(0,self.mapIDs[currentMapIdx])
        self.mapsNameEntry.delete(0,tk.END)
        self.mapsNameEntry.insert(0,self.mapData[self.mapIDs[currentMapIdx]].getData('name'))
        self.mapsEdgeObjIDEntry.delete(0,tk.END)
        self.mapsEdgeObjIDEntry.insert(0,self.mapData[self.mapIDs[currentMapIdx]].getData('edge_obj_id'))
        self.mapsDescEntry.delete(0,tk.END)
        self.mapsDescEntry.insert(0,self.mapData[self.mapIDs[currentMapIdx]].getData('desc'))
        self.mapsWidthEntry.delete(0,tk.END)
        self.mapsWidthEntry.insert(0,self.mapData[self.mapIDs[currentMapIdx]].getData('width'))
        self.mapsHeightEntry.delete(0,tk.END)
        self.mapsHeightEntry.insert(0,self.mapData[self.mapIDs[currentMapIdx]].getData('height'))



# TODO: update all functions to implement writing to each JSON file
    def updateTeamsJSON(self): 
        self.teamData[self.teamNameEntry.get()]['size'] = int(self.teamSizeEntry.get())
        self.teamData[self.teamNameEntry.get()]['agent_defs'][0]['callsign'] = self.callsignEntry.get()
        self.teamData[self.teamNameEntry.get()]['name'] = self.teamNameEntry.get()

        print(self.teamNameEntry.get())
        self.teamsJSON = json.dumps(self.teamData, indent=4)
        print(self.teamsJSON)

        with open('settings/teams.json', 'w') as f:
            f.write(self.teamsJSON)
        f.close()

    
    def updateComponentsJSON():
        return
    
    def updateObjectsJSON():
        return

    def updateMapsJSON():
        return
    



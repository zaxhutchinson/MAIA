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
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring

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
        
        #Make main widgets
        self.mainFrame = uiQuietFrame(master=self)
        self.teamsColumn = uiQuietFrame(master=self.mainFrame)
        self.componentsColumn = uiQuietFrame(master=self.mainFrame)
        self.objectsColumn = uiQuietFrame(master=self.mainFrame)
        self.mapsColumn = uiQuietFrame(master=self.mainFrame)
        self.titleLabel = uiLabel(master=self.mainFrame, text="Advanced Settings")
        
        #Place main widgets
        self.mainFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.titleLabel.pack(side=tk.TOP,fill=tk.BOTH,expand=False,padx=10,pady=10)
        
        
        #Make Team Widgets
        self.selectTeamCombo = uiComboBox(master=self.teamsColumn)
        self.teamsLabel = uiLabel(master=self.teamsColumn, text="Teams")
        self.teamSizeLabel = uiLabel(master=self.teamsColumn, text="Size:")
        self.teamSizeEntry = uiEntry(master=self.teamsColumn)
        self.teamNameLabel = uiLabel(master=self.teamsColumn,text="Name:")
        self.teamNameEntry = uiEntry(master=self.teamsColumn)
        self.agentFrame = uiQuietFrame(master=self.teamsColumn, borderwidth=5,  relief="ridge",sticky="nsew")
        self.callsignLabel = uiLabel(master=self.agentFrame,text="Callsign:")
        self.callsignEntry = uiEntry(master=self.agentFrame)
        self.squadLabel = uiLabel(master=self.agentFrame,text="Squad:")
        self.squadEntry = uiEntry(master=self.agentFrame)
        self.agentObjectLabel = uiLabel(master=self.agentFrame,text="Object:")
        self.agentObjectEntry = uiEntry(master=self.agentFrame)
        self.aiFileLabel = uiLabel(master=self.agentFrame,text="AI File:")
        self.aiFileEntry = uiEntry(master=self.agentFrame)
        self.teamsUpdateButton = uiButton(master=self.teamsColumn,command=self.updateTeamsJSON, text="update")
        self.teamsCreateButton = uiButton(master=self.teamsColumn,command=self.createTeam,text="Create")
        
        #Place Team Widgets
        self.teamsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.selectTeamCombo.grid(row=1,column=1,columnspan=2,padx=10,pady=10,ipadx=10,ipady=10)
        self.teamsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.teamSizeLabel.grid(row=3,column=1,sticky="nsew")
        self.teamSizeEntry.grid(row=3,column=2,sticky="nsew")
        self.teamNameLabel.grid(row=4,column=1,sticky="nsew")
        self.teamNameEntry.grid(row=4,column=2,sticky="nsew")
        self.agentFrame.grid(row=5,column=1,columnspan=2,rowspan=2,sticky="nsew", ipadx=0,ipady=0)        
        self.callsignLabel.grid(row=1,column=1,sticky="nsew")        
        self.callsignEntry.grid(row=1,column=2,sticky="nsew")        
        self.squadLabel.grid(row=2,column=1,sticky="nsew")       
        self.squadEntry.grid(row=2,column=2,sticky="nsew")        
        self.agentObjectLabel.grid(row=3,column=1,sticky="nsew")        
        self.agentObjectEntry.grid(row=3,column=2,sticky="nsew")       
        self.aiFileLabel.grid(row=4,column=1,sticky="nsew")       
        self.aiFileEntry.grid(row=4,column=2,sticky="nsew")
        self.teamsUpdateButton.grid(row=7,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)       
        self.teamsCreateButton.grid(row=8,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)


        #Make Component Widgets
        self.selectComponentCombo = uiComboBox(master=self.componentsColumn)
        self.componentsLabel = uiLabel(master=self.componentsColumn, text="Components")
        self.componentsUpdateButton = uiButton(master=self.componentsColumn,command=self.updateComponentsJSON,text="Update")
        self.componentsCreateButtom = uiButton(master=self.componentsColumn,command="",text="Create")
        self.componentsIDLabel = uiLabel(master=self.componentsColumn, text="ID:")
        self.componentsIDEntry = uiEntry(master=self.componentsColumn)
        self.componentsNameLabel = uiLabel(master=self.componentsColumn, text="Name:")
        self.componentsNameEntry = uiEntry(master=self.componentsColumn)
        self.componentsCTypeLabel = uiLabel(master=self.componentsColumn,text="CType:")
        self.componentsTypeLabel = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeCombo = uiComboBox(master=self.componentsColumn)
        self.componentsTypeAttr1Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr1Entry = uiEntry(master=self.componentsColumn)
        self.componentsTypeAttr2Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr2Entry = uiEntry(master=self.componentsColumn)
        self.componentsTypeAttr3Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr3Entry = uiEntry(master=self.componentsColumn)
        self.componentsTypeAttr4Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr4Entry = uiEntry(master=self.componentsColumn)
        self.componentsTypeAttr5Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr5Entry = uiEntry(master=self.componentsColumn)
        self.componentsTypeAttr6Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr6Entry = uiEntry(master=self.componentsColumn)
        self.componentsTypeAttr7Label = uiLabel(master=self.componentsColumn,text="")
        self.componentsTypeAttr7Entry = uiEntry(master=self.componentsColumn)

        #Place Component Widgets
        self.componentsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.selectComponentCombo.grid(row=1,column=1,columnspan=2,padx=10,pady=10,ipadx=10,ipady=10)
        self.componentsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.componentsIDLabel.grid(row=3,column=1,sticky="nsew")
        self.componentsIDEntry.grid(row=3,column=2,sticky="nsew")
        self.componentsNameLabel.grid(row=4,column=1,sticky="nsew")
        self.componentsNameEntry.grid(row=4,column=2,sticky="nsew")
        self.componentsCTypeLabel.grid(row=5,column=1,sticky="nsew")
        self.componentsTypeLabel.grid(row=5,column=2,sticky="nsew")
        self.componentsTypeCombo.grid(row=6,column=1,columnspan=2,sticky="nsew")
        self.componentsTypeAttr1Label.grid(row=7,column=1,sticky="nsew")
        self.componentsTypeAttr1Entry.grid(row=7,column=2,sticky="nsew")
        self.componentsTypeAttr2Label.grid(row=8,column=1,sticky="nsew")
        self.componentsTypeAttr2Entry.grid(row=8,column=2,sticky="nsew")
        self.componentsTypeAttr3Label.grid(row=9,column=1,sticky="nsew")
        self.componentsTypeAttr3Entry.grid(row=9,column=2,sticky="nsew")
        self.componentsTypeAttr4Label.grid(row=10,column=1,sticky="nsew")
        self.componentsTypeAttr4Entry.grid(row=10,column=2,sticky="nsew")
        self.componentsTypeAttr5Label.grid(row=11,column=1,sticky="nsew")
        self.componentsTypeAttr5Entry.grid(row=11,column=2,sticky="nsew")
        self.componentsTypeAttr6Label.grid(row=12,column=1,sticky="nsew")
        self.componentsTypeAttr6Entry.grid(row=12,column=2,sticky="nsew")
        self.componentsTypeAttr7Label.grid(row=13,column=1,sticky="nsew")
        self.componentsTypeAttr7Entry.grid(row=13,column=2,sticky="nsew")
        self.componentsUpdateButton.grid(row=14,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)
        self.componentsCreateButtom.grid(row=15,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)


        #Make Object Widgets
        self.selectObjectsCombo = uiComboBox(master=self.objectsColumn)
        self.objectsLabel = uiLabel(master=self.objectsColumn, text="Objects")
        self.objectsUpdateButton = uiButton(master=self.objectsColumn,command="",text="Update")
        self.objectsCreateButton = uiButton(master=self.objectsColumn,command="",text="Create")
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

        #Place Object Widgets
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
        self.objectsUpdateButton.grid(row=12,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)
        self.objectsCreateButton.grid(row=13,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)


        #Make Map Widgets
        self.selectMapsCombo = uiComboBox(master=self.mapsColumn)
        self.mapsLabel = uiLabel(master=self.mapsColumn, text="Maps")
        self.mapsUpdateButton = uiButton(master=self.mapsColumn,command="",text="Update")
        self.mapsCreateButton = uiButton(master=self.mapsColumn,command="",text="Create")
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
        
        #Place Map Widgets
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
        self.mapsUpdateButton.grid(row=9,column=1,columnspan=2,sticky="nsew",ipadx=2,ipady=2,padx=10,pady=10)

        self.initEntryWidgets()


    def initEntryWidgets(self):
        #TEAM
        self.teamData=self.ldr.team_templates
        self.teamNames = self.ldr.getTeamNames()
        self.currentTeamData = self.teamData[self.teamNames[0]]

        self.selectTeamCombo.configure(values=self.teamNames)
        self.selectTeamCombo.current(0)
        self.selectTeamCombo.bind("<<ComboboxSelected>>", self.changeTeamEntryWidgets)
        self.teamNameEntry.insert(0,self.currentTeamData['name'])
        self.teamSizeEntry.insert(0,self.currentTeamData['size'])
        self.callsignEntry.insert(0,self.currentTeamData['agent_defs'][0]['callsign'])
        self.squadEntry.insert(0,self.currentTeamData['agent_defs'][0]['squad'])
        self.agentObjectEntry.insert(0,self.currentTeamData['agent_defs'][0]['object'])
        self.aiFileEntry.insert(0,self.currentTeamData['agent_defs'][0]['AI_file'])

        #COMPONENT
        self.componentData=self.ldr.comp_templates
        self.componentIDs=self.ldr.getCompIDs()
        self.componentTypes=self.ldr.getCompTypes()
        self.componentTypeAttr=self.componentData[self.componentIDs[0]].view_keys
        self.currentComponentData=self.componentData[self.componentIDs[0]]

        self.selectComponentCombo.configure(values=self.componentIDs)
        self.selectComponentCombo.current(0)
        self.selectComponentCombo.bind("<<ComboboxSelected>>", self.changeComponentsEntryWidgets)
        self.componentsIDEntry.insert(0,self.componentIDs[0])
        self.componentsNameEntry.insert(0,self.currentComponentData.getData('name'))
        self.componentsTypeCombo.configure(values=self.componentTypes)
        self.componentsTypeCombo.set(self.currentComponentData.getData('ctype'))
        self.componentsTypeCombo.bind("<<ComboboxSelected>>",self.changeComponentAttributeWidgets)
        self.componentsTypeLabel.config(text=self.currentComponentData.getData('ctype'))

        if self.currentComponentData.getData('ctype') == 'CnC':
            self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
            self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
        elif self.componentData[self.componentIDs[0]].getData('ctype') == 'FixedGun':
            self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
            self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
            self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
            self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
            self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
            self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))
            self.componentsTypeAttr4Label.config(text=self.componentTypeAttr[7])
            self.componentsTypeAttr4Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[7]))
            self.componentsTypeAttr5Label.config(text=self.componentTypeAttr[8])
            self.componentsTypeAttr5Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[8]))
            self.componentsTypeAttr6Label.config(text=self.componentTypeAttr[9])
            self.componentsTypeAttr6Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[9]))
            self.componentsTypeAttr7Label.config(text=self.componentTypeAttr[10])
            self.componentsTypeAttr7Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[10]))
        elif self.currentComponentData.getData('ctype') == 'Engine':
            self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
            self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
            self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
            self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
            self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
            self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))
            self.componentsTypeAttr4Label.config(text=self.componentTypeAttr[7])
            self.componentsTypeAttr4Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[7]))
            self.componentsTypeAttr5Label.config(text=self.componentTypeAttr[8])
            self.componentsTypeAttr5Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[8]))
        elif self.currentComponentData.getData('ctype') == 'Radar':
            self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
            self.componentsTypeAttr1Entry.insert(0,self.currentComponentData[self.componentTypeAttr[4]])
            self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
            self.componentsTypeAttr2Entry.insert(0,self.currentComponentData[self.componentTypeAttr[5]])
            self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
            self.componentsTypeAttr3Entry.insert(0,self.currentComponentData[self.componentTypeAttr[6]])
            self.componentsTypeAttr4Label.config(text=self.componentTypeAttr[7])
            self.componentsTypeAttr4Entry.insert(0,self.currentComponentData[self.componentTypeAttr[7]])
            self.componentsTypeAttr5Label.config(text=self.componentTypeAttr[8])
            self.componentsTypeAttr5Entry.insert(0,self.currentComponentData[self.componentTypeAttr[8]])
            self.componentsTypeAttr6Label.config(text=self.componentTypeAttr[9])
            self.componentsTypeAttr6Entry.insert(0,self.currentComponentData[self.componentTypeAttr[9]])
        elif self.currentComponentData.getData('ctype') == 'Radio':
            self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
            self.componentsTypeAttr1Entry.insert(0,self.currentComponentData[self.componentTypeAttr[4]])
            self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
            self.componentsTypeAttr2Entry.insert(0,self.currentComponentData[self.componentTypeAttr[5]])
            self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
            self.componentsTypeAttr3Entry.insert(0,self.currentComponentData[self.componentTypeAttr[6]])
        elif self.currentComponentData.getData('ctype') == 'Arm':
            self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
            self.componentsTypeAttr1Entry.insert(0,self.currentComponentData[self.componentTypeAttr[4]])
            self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
            self.componentsTypeAttr2Entry.insert(0,self.currentComponentData[self.componentTypeAttr[5]])
            self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
            self.componentsTypeAttr3Entry.insert(0,self.currentComponentData[self.componentTypeAttr[6]])

        #OBJECT
        self.objectData = self.ldr.obj_templates  
        self.objectIDs = self.ldr.getObjIDs()
        self.currentObjectData = self.objectData[self.objectIDs[0]]
        print(self.currentObjectData.getSelfView())
        
        self.selectObjectsCombo.configure(values=self.objectIDs, state='readonly')
        self.selectObjectsCombo.current(0)
        self.selectObjectsCombo.bind("<<ComboboxSelected>>", self.changeObjectsEntryWidgets)
        
        self.objectsIDEntry.insert(0,self.currentObjectData.getData('id'))
        self.objectsNameEntry.insert(0,self.currentObjectData.getData('name'))
        self.objectsFillAliveEntry.insert(0,self.currentObjectData.getData('fill_alive'))
        self.objectsFillDeadEntry.insert(0,self.currentObjectData.getData('fill_dead'))
        self.objectsTextEntry.insert(0,self.currentObjectData.getData('text'))
        self.objectsHealthEntry.insert(0,self.currentObjectData.getData('health'))
        self.objectsDensityEntry.insert(0,self.currentObjectData.getData('density'))
        self.objectsCompIDsEntry.insert(0,self.currentObjectData.getData('comp_ids'))
        self.objectsPointsCountEntry.insert(0,self.currentObjectData.getData('points_count'))

        #MAP
        self.mapData = self.ldr.map_templates
        self.mapIDs = self.ldr.getMapIDs()
        self.currentMapData = self.mapData[self.mapIDs[0]]


        self.selectMapsCombo.configure(values=self.mapIDs)
        self.selectMapsCombo.current(0)
        self.selectMapsCombo.bind("<<ComboboxSelected>>", self.changeMapsEntryWidgets)
        self.mapsIDEntry.insert(0,self.mapIDs[0])
        self.mapsNameEntry.insert(0,self.currentMapData.getData('name'))
        self.mapsEdgeObjIDEntry.insert(0,self.currentMapData.getData('edge_obj_id'))
        self.mapsDescEntry.insert(0,self.currentMapData.getData('desc'))
        self.mapsWidthEntry.insert(0,self.currentMapData.getData('width'))
        self.mapsHeightEntry.insert(0,self.currentMapData.getData('height'))

    def changeComponentAttributeWidgets(self,event=None):
        return

    def changeTeamEntryWidgets(self, event=None, fromCreate=False):
        #the answer variable defaults to true
        self.answer=True

        #if any of the team entry values differ from their starting values, the user is warned that they could be overwritten
        if not(((self.teamNameEntry.get()==self.currentTeamData['name']) and (int(self.teamSizeEntry.get())==self.currentTeamData['size']) and (self.callsignEntry.get()==self.currentTeamData['agent_defs'][0]['callsign'])) or fromCreate):
            self.answer = askyesno(title='confirmation', message='Warning: You have modified Team values and have not Updated. Your changes will not be saved. Are you sure you would like continue?')
        
        #the current team is successfully changed if the user made no changes, or if the user confirms they are fine with their changes being overwritten
        if self.answer:
            currentTeamIdx = self.selectTeamCombo.current()
            if not(fromCreate):
                self.currentTeamData = self.teamData[self.selectTeamCombo.get()]
            self.teamNameEntry.delete(0,tk.END)
            self.teamNameEntry.insert(0,self.teamNames[currentTeamIdx])
            self.teamSizeEntry.delete(0,tk.END)
            self.teamSizeEntry.insert(0, self.currentTeamData['size'])
            self.callsignEntry.delete(0,tk.END)
            self.callsignEntry.insert(0, self.currentTeamData['agent_defs'][0]['callsign'])
            self.squadEntry.delete(0,tk.END)
            self.squadEntry.insert(0, self.currentTeamData['agent_defs'][0]['squad'])
            self.agentObjectEntry.delete(0,tk.END)
            self.agentObjectEntry.insert(0, self.currentTeamData['agent_defs'][0]['object'])
            self.aiFileEntry.delete(0,tk.END)
            self.aiFileEntry.insert(0, self.currentTeamData['agent_defs'][0]['AI_file'])
   
    def changeComponentsEntryWidgets(self, v):
        self.answer=True

        if not(((self.componentsIDEntry.get()==self.currentComponentData.getData('id')) and (self.componentsNameEntry.get()==self.currentComponentData.getData('name')) and (self.componentsTypeCombo.get()==self.currentComponentData.getData('ctype')))):        
            self.answer = askyesno(title='confirmation', message='Warning: You have modified Component values and have not Updated. Your changes will not be saved. Are you sure you would like continue?')
        
        
        if self.answer == True:
            currentComponentIdx = self.selectComponentCombo.current()
            self.componentTypeAttr=self.componentData[self.componentIDs[currentComponentIdx]].view_keys
            self.currentComponentData=self.componentData[self.componentIDs[currentComponentIdx]]
            
            self.componentsIDEntry.delete(0,tk.END)
            self.componentsIDEntry.insert(0,self.componentIDs[currentComponentIdx])
            self.componentsNameEntry.delete(0,tk.END)
            self.componentsNameEntry.insert(0,self.componentData[self.componentIDs[currentComponentIdx]].getData('name'))
            self.componentsTypeCombo.configure(values=self.componentTypes)
            self.componentsTypeCombo.set(self.componentData[self.componentIDs[currentComponentIdx]].getData('ctype'))
            self.componentsTypeLabel.config(text=self.componentData[self.componentIDs[currentComponentIdx]].getData('ctype'))
            self.componentsTypeAttr1Label.config(text="")
            self.componentsTypeAttr2Label.config(text="")
            self.componentsTypeAttr3Label.config(text="")
            self.componentsTypeAttr4Label.config(text="")
            self.componentsTypeAttr5Label.config(text="")
            self.componentsTypeAttr6Label.config(text="")
            self.componentsTypeAttr7Label.config(text="")
            self.componentsTypeAttr1Entry.delete(0,tk.END)
            self.componentsTypeAttr2Entry.delete(0,tk.END)
            self.componentsTypeAttr3Entry.delete(0,tk.END)
            self.componentsTypeAttr4Entry.delete(0,tk.END)
            self.componentsTypeAttr5Entry.delete(0,tk.END)
            self.componentsTypeAttr6Entry.delete(0,tk.END)
            self.componentsTypeAttr7Entry.delete(0,tk.END)
            if self.currentComponentData.getData('ctype') == 'CnC':
                self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
                self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
            elif self.componentData[self.componentIDs[currentComponentIdx]].getData('ctype') == 'FixedGun':
                self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
                self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
                self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
                self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
                self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
                self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))
                self.componentsTypeAttr4Label.config(text=self.componentTypeAttr[7])
                self.componentsTypeAttr4Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[7]))
                self.componentsTypeAttr5Label.config(text=self.componentTypeAttr[8])
                self.componentsTypeAttr5Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[8]))
                self.componentsTypeAttr6Label.config(text=self.componentTypeAttr[9])
                self.componentsTypeAttr6Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[9]))
                self.componentsTypeAttr7Label.config(text=self.componentTypeAttr[10])
                self.componentsTypeAttr7Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[10]))
            elif self.currentComponentData.getData('ctype') == 'Engine':
                self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
                self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
                self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
                self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
                self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
                self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))
                self.componentsTypeAttr4Label.config(text=self.componentTypeAttr[7])
                self.componentsTypeAttr4Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[7]))
                self.componentsTypeAttr5Label.config(text=self.componentTypeAttr[8])
                self.componentsTypeAttr5Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[8]))
            elif self.currentComponentData.getData('ctype') == 'Radar':
                self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
                self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
                self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
                self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
                self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
                self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))
                self.componentsTypeAttr4Label.config(text=self.componentTypeAttr[7])
                self.componentsTypeAttr4Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[7]))
                self.componentsTypeAttr5Label.config(text=self.componentTypeAttr[8])
                self.componentsTypeAttr5Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[8]))
                self.componentsTypeAttr6Label.config(text=self.componentTypeAttr[9])
                self.componentsTypeAttr6Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[9]))
            elif self.currentComponentData.getData('ctype') == 'Radio':
                self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
                self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
                self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
                self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
                self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
                self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))
            elif self.currentComponentData.getData('ctype') == 'Arm':
                self.componentsTypeAttr1Label.config(text=self.componentTypeAttr[4])
                self.componentsTypeAttr1Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[4]))
                self.componentsTypeAttr2Label.config(text=self.componentTypeAttr[5])
                self.componentsTypeAttr2Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[5]))
                self.componentsTypeAttr3Label.config(text=self.componentTypeAttr[6])
                self.componentsTypeAttr3Entry.insert(0,self.currentComponentData.getData(self.componentTypeAttr[6]))

    def changeObjectsEntryWidgets(self, event=None, fromCreate=False):
        currentObject = self.selectObjectsCombo.get()
        print(currentObject)
        self.currentObjectData=self.objectData[currentObject]

        self.objectsIDEntry.delete(0,tk.END)
        self.objectsIDEntry.insert(0,self.currentObjectData.getData('id'))
        self.objectsNameEntry.delete(0,tk.END)
        self.objectsNameEntry.insert(0,self.currentObjectData.getData('name'))
        self.objectsFillAliveEntry.delete(0,tk.END)
        self.objectsFillAliveEntry.insert(0,self.currentObjectData.getData('fill_alive'))
        self.objectsFillDeadEntry.delete(0,tk.END)
        self.objectsFillDeadEntry.insert(0,self.currentObjectData.getData('fill_dead'))
        self.objectsTextEntry.delete(0,tk.END)
        self.objectsTextEntry.insert(0,self.currentObjectData.getData('text'))
        self.objectsHealthEntry.delete(0,tk.END)
        self.objectsHealthEntry.insert(0,self.currentObjectData.getData('health'))
        self.objectsDensityEntry.delete(0,tk.END)
        self.objectsDensityEntry.insert(0,self.currentObjectData.getData('density'))
        self.objectsCompIDsEntry.delete(0,tk.END)
        self.objectsCompIDsEntry.insert(0,self.currentObjectData.getData('comp_ids'))
        self.objectsPointsCountEntry.delete(0,tk.END)
        self.objectsPointsCountEntry.insert(0,self.currentObjectData.getData('points_count'))

    def changeMapsEntryWidgets(self, v):
        
        self.answer = askyesno(title='confirmation', message='Warning: You have modified Map values and have not Updated. Your changes will not be saved. Are you sure you would like continue?')
        currentMap = self.selectMapsCombo.get()
        print(currentMap)
        self.currentMapData=self.mapData[currentMap]
        print(self.currentMapData)
        if self.answer == True:
            self.mapsIDEntry.delete(0,tk.END)
            self.mapsIDEntry.insert(0,currentMap)
            self.mapsNameEntry.delete(0,tk.END)
            self.mapsNameEntry.insert(0,self.currentMapData.getData('name'))
            self.mapsEdgeObjIDEntry.delete(0,tk.END)
            self.mapsEdgeObjIDEntry.insert(0,self.currentMapData.getData('edge_obj_id'))
            self.mapsDescEntry.delete(0,tk.END)
            self.mapsDescEntry.insert(0,self.currentMapData.getData('desc'))
            self.mapsWidthEntry.delete(0,tk.END)
            self.mapsWidthEntry.insert(0,self.currentMapData.getData('width'))
            self.mapsHeightEntry.delete(0,tk.END)
            self.mapsHeightEntry.insert(0,self.currentMapData.getData('height'))

# TODO: update all functions to implement writing to each JSON file
    def updateTeamsJSON(self): 
        self.currentTeamData['size'] = int(self.teamSizeEntry.get())
        self.currentTeamData['agent_defs'][0]['callsign'] = self.callsignEntry.get()
        self.currentTeamData['name'] = self.teamNameEntry.get()
        self.currentTeamData['agent_defs'][0]['squad'] = self.squadEntry.get()
        self.currentTeamData['agent_defs'][0]['object'] = self.agentObjectEntry.get()
        self.currentTeamData['agent_defs'][0]['AI_file'] = self.aiFileEntry.get()

        self.teamData.update({self.currentTeamData['name']: self.currentTeamData})

        print(self.teamNameEntry.get())
        self.teamsJSON = json.dumps(self.teamData, indent=4)
        print(self.teamsJSON)

        with open('settings/teams.json', 'r') as f:
           teamJSON=json.load(f)  
        teamJSON[self.selectTeamCombo.get()] =self.currentTeamData 
        f.close()

        with open('settings/teams.json', 'w') as f:
            json.dump(teamJSON,f,indent=4)
        f.close()

    
    def updateComponentsJSON(self):
        self.currentComponentData.setData('id',self.componentsIDEntry.get())
        self.currentComponentData.setData('name',self.componentsNameEntry.get())
        self.currentComponentData.setData('ctype',self.componentsTypeCombo.get())
        
        with open('settings/components.json', 'r') as f:
           componentJSON=json.load(f)  
        componentJSON[self.currentComponentData.getData('id')] =self.currentComponentData.getSelfView()   
        f.close()

        with open('settings/components.json', 'w') as f:
            json.dump(componentJSON,f,indent=4)
        f.close()

    
    def updateObjectsJSON(self):
        self.currentObjectData.setData('id',self.objectsIDEntry.get())
        self.currentObjectData.setData('name',self.objectsNameEntry.get())
        self.currentObjectData.setData('fill_alive',self.objectsFillAliveEntry.get())
        self.currentObjectData.setData('fill_dead',self.objectsFillDeadEntry.get())
        self.currentObjectData.setData('text',self.objectsTextEntry.get())
        self.currentObjectData.setData('health',self.objectsHealthEntry.get())
        self.currentObjectData.setData('density',self.objectsDensityEntry.get())
        self.currentObjectData.setData('comp_ids',self.objectsCompIDsEntry.get())
        self.currentObjectData.setData('points_count',self.objectsPointsCountEntry.get())

        with open('settings/objects.json', 'r') as f:
           objectJSON=json.load(f)  
        objectJSON[self.currentObjectData.getData('id')] =self.currentObjectData.getJSONView()
        objectJSON[self.currentObjectData.getData('id')].pop('slot_id')
        f.close()

        with open('settings/objects.json', 'w') as f:
            json.dump(objectJSON,f,indent=4)
        f.close()

    def updateMapsJSON():
        return
    
    def createTeam(self):
        self.teamID = askstring('Team ID','Please enter an ID for the new team.')   
        self.teamNames.append(self.teamID)
        self.selectTeamCombo.configure(values=self.teamNames)
        self.selectTeamCombo.current(len(self.teamNames)-1)
        self.currentTeamData =  {'size': "", 'name': "", 'agent_defs': [{'callsign': "", 'squad': "", 'object': "", 'AI_file': ""}]}
        self.changeTeamEntryWidgets(fromCreate=True)
    
    def createComponent(self):
        self.componentID = askstring('Component ID','Please enter an ID for the new component.')
        self.componentIDs.append(self.componentID)
        self.selectComponentCombo.configure(values=self.componentIDs)
        self.selectComponentCombo.current(len(self.componentIDs)-1)
        self.currentComponentData
    
    def createObject(self):
        self.objectID = askstring('Object ID','Please enter an ID for the new object.')
        self.objectIDs.append(self.objectID)
        self.selectObjectsCombo.configure(values=self.objectIDs)
        self.selectObjectsCombo.current(len(self.objectIDs)-1)    
        self.currentObjectData = {"id": "","name": "", "fill_alive": "", "fill_dead": "", "text": "", "health" : "", "density": "", "comp_ids": [], "points_count": ""}
        self.changeObjectsEntryWidgets()
    
    def createMap(self):
        return

import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging
import loader

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
        
        self.teamsLabel = uiLabel(master=self.teamsColumn, text="Teams")
        self.teamsUpdateButton = uiButton(master=self.teamsColumn,command="", text="update")
        self.teamSizeLabel = uiLabel(master=self.teamsColumn, text="Size:")
        self.teamSizeEntry = uiEntry(master=self.teamsColumn)
        self.teamNameLabel = uiLabel(master=self.teamsColumn,text="Name:")
        self.teamNameEntry = uiEntry(master=self.teamsColumn)

        self.componentsLabel = uiLabel(master=self.componentsColumn, text="Components")
        self.componentsUpdateButton = uiButton(master=self.componentsColumn,command="",text="Update")
        self.componentsIDLabel = uiLabel(master=self.componentsColumn, text="ID:")
        self.componentsIDEntry = uiEntry(master=self.componentsColumn)
        self.componentsNameLabel = uiLabel(master=self.componentsColumn, text="Name:")
        self.componentsNameEntry = uiEntry(master=self.componentsColumn)

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


        #Set locations of widgets in containers
        self.bottomFrame.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.titleLabel.pack(side=tk.TOP,fill=tk.BOTH,expand=False,padx=10,pady=10)
        
        self.teamsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.teamsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.teamSizeLabel.grid(row=3,column=1,sticky="nsew")
        self.teamSizeEntry.grid(row=3,column=2,sticky="nsew")
        self.teamNameLabel.grid(row=4,column=1,sticky="nsew")
        self.teamNameEntry.grid(row=4,column=2,sticky="nsew")
        self.teamsUpdateButton.grid(row=8,column=1,columnspan=2,sticky="nsew")

        self.squadFrame = uiQuietFrame(master=self.teamsColumn, borderwidth=5,  relief="ridge",sticky="nsew")
        self.squadFrame.grid(row=5,column=1,columnspan=2,rowspan=2,sticky="nsew", ipadx=0,ipady=0)
        self.callsignLabel = uiLabel(master=self.squadFrame,text="Callsign:")
        self.callsignLabel.grid(row=1,column=1,sticky="nsew")
        self.callsignEntry = uiEntry(master=self.squadFrame)
        self.callsignEntry.grid(row=1,column=2,sticky="nsew")
        self.squadLabel = uiLabel(master=self.squadFrame,text="Squad:")
        self.squadLabel.grid(row=2,column=1,sticky="nsew")
        self.squadEntry = uiEntry(master=self.squadFrame)
        self.squadEntry.grid(row=2,column=2,sticky="nsew")
        self.squadObjectLabel = uiLabel(master=self.squadFrame,text="Object:")
        self.squadObjectLabel.grid(row=3,column=1,sticky="nsew")
        self.squadObjectEntry = uiEntry(master=self.squadFrame)
        self.squadObjectEntry.grid(row=3,column=2,sticky="nsew")


        
        self.componentsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.componentsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.componentsIDLabel.grid(row=3,column=1,sticky="nsew")
        self.componentsIDEntry.grid(row=3,column=2,sticky="nsew")
        self.componentsNameLabel.grid(row=4,column=1,sticky="nsew")
        self.componentsNameEntry.grid(row=4,column=2,sticky="nsew")

        self.objectsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
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

        self.mapsColumn.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.mapsLabel.grid(row=1,column=1,columnspan=2,sticky="nsew")
        self.mapsIDLabel.grid(row=2,column=1,sticky="nsew")
        self.mapsIDEntry.grid(row=2,column=2,sticky="nsew")
        self.mapsNameLabel.grid(row=3,column=1,sticky="nsew")
        self.mapsNameEntry.grid(row=3,column=2,sticky="nsew")
        self.mapsEdgeObjIDLabel.grid(row=4,column=1,sticky="nsew")
        self.mapsEdgeObjIDEntry.grid(row=4,column=2,sticky="nsew")
        self.mapsDescLabel.grid(row=5,column=1,sticky="nsew")
        self.mapsDescEntry.grid(row=5,column=2,sticky="nsew")

        teamName = self.ldr.getTeamNames()[0]
        self.mapsNameEntry.insert(0,teamName)


    def updateTeamsJSON():
        return
    
    def updateComponentsJSON():
        return
    
    def updateObjectsJSON():
        return

    def updateMapsJSON():
        return
    



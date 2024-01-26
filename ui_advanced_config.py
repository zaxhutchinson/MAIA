import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging

from ui_widgets import *

class UISettings(tk.Toplevel):
    def __init__(self,master=None,logger=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=DARKCOLOR)
        self.title("MAIA - Advanced Configuration")
        self.geometry("700x800")
        self.logger=logger
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
        
        #Make Widgets
        self.titleLabel = uiLabel(master=self.titleFrame, text="Advanced Settings")
        self.teamsLabel = uiLabel(master=self.teamsColumn, text="Teams")
        self.teamSizeLabel = uiLabel(master=self.teamsColumn, text="Size:")
        self.teamSizeEntry = uiEntry(master=self.teamsColumn)
        self.teamNameLabel = uiLabel(master=self.teamsColumn,text="Name:")
        self.teamNameEntry = uiEntry(master=self.teamsColumn)

        self.componentsLabel = uiLabel(master=self.componentsColumn, text="Components")
        self.componentsIDLabel = uiLabel(master=self.componentsColumn, text="ID:")
        self.componentsIDEntry = uiEntry(master=self.componentsColumn)
        self.componentsNameLabel = uiLabel(master=self.componentsColumn, text="Name:")
        self.componentsNameEntry = uiEntry(master=self.componentsColumn)

        self.objectsLabel = uiLabel(master=self.objectsColumn, text="Objects")
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

        #Set locations of widgets in containers
        self.titleFrame.grid(row=0,column=0,columnspan=3, sticky="nsew")
        self.titleLabel.grid(row=0,columnspan=3)
        self.bottomFrame.grid(row=1,column=0,columnspan=3, sticky="nsew")
        
        self.teamsColumn.grid(row=1,column = 0,columnspan=1 ,pady=2,sticky="nsew")
        self.teamsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.teamSizeLabel.grid(row=3,column=1,sticky="nsew")
        self.teamSizeEntry.grid(row=3,column=2,sticky="nsew")
        self.teamNameLabel.grid(row=4,column=1,sticky="nsew")
        self.teamNameEntry.grid(row=4,column=2,sticky="nsew")
        
        self.componentsColumn.grid(row=1,column = 1,sticky="nsew")
        self.componentsLabel.grid(row=2,column=1,columnspan=2,sticky="nsew")
        self.componentsIDLabel.grid(row=3,column=1,sticky="nsew")
        self.componentsIDEntry.grid(row=3,column=2,sticky="nsew")
        self.componentsNameLabel.grid(row=4,column=1,sticky="nsew")
        self.componentsNameEntry.grid(row=4,column=2,sticky="nsew")

        self.objectsColumn.grid(row=1,column = 3,  pady=2,sticky="nsew")
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

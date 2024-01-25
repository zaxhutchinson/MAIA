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
        self.componentsLabel = uiLabel(master=self.teamsColumn, text="Components")
        self.objectsLabel = uiLabel(master=self.objectsColumn, text="Objects")

        #Set locations of widgets in containers
        self.titleFrame.grid(row=0,column=0,columnspan=3, sticky="nsew")
        self.titleLabel.grid(row=0,columnspan=3)
        self.bottomFrame.grid(row=1,column=0,columnspan=3, sticky="nsew")
        self.teamsColumn.grid(row=1,column = 0,columnspan=1 ,pady=2,sticky="nsew")
        self.teamsLabel.grid(row=2,column=1,sticky="nsew")
        self.componentsColumn.grid(row=1,column = 1,sticky="nsew")
        self.componentsLabel.grid(row=2,column=2,sticky="nsew")
        self.objectsColumn.grid(row=1,column = 3,  pady=2,sticky="nsew")
        self.objectsLabel.grid(row=2,column=1,sticky="nsew")

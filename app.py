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
        self.map_names = []
        self.combat_log = []

        self.BuildUI()

    def Run(self):
        self.mainloop()

    def BuildUI(self):
        self.teamFrame = tk.Frame(self,relief=tk.RAISED,borderwidth=1)
        self.teamFrame.pack(fill=tk.BOTH,expand=True)

        self.lbTeams = tk.Listbox(self.teamFrame,selectmode=tk.SINGLE)
        self.lbTeams.pack(side=tk.LEFT)

        self.lbTeamsToPlay = tk.Listbox(self.teamFrame,selectmode=tk.SINGLE)
        self.lbTeamsToPlay.pack(side=tk.RIGHT)

        self.updateTeamNames()

        self.pack(fill=tk.BOTH,expand=True)

        self.btnAddTeam = tk.Button(self, text="Add Team", command=self.addTeam)
        self.btnAddTeam.pack(side=tk.LEFT)

        self.btnRemoveTeam = tk.Button(self,text="Remove Team", command=self.removeTeam)
        self.btnRemoveTeam.pack(side=tk.RIGHT)

    def updateTeamNames(self):
        self.lbTeams.delete(0,tk.END)
        self.lbTeamsToPlay.delete(0,tk.END)
        for name in self.team_names:
            self.lbTeams.insert(tk.END,name)
        for name in self.team_names_to_play:
            self.lbTeamsToPlay.insert(tk.END,name)

    def addTeam(self):
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

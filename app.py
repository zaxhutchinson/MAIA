import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import importlib.util
import sys
import os

class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=500,height=600)
        self.master = master
        self.pack()
        self.master.title("MAIA - Maine AI Arena")

        self.BuildUI()

        self.teams = {}
        self.map = None
        self.combat_log = []

    def BuildUI(self):
        pass
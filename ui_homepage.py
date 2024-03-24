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
import ui_about
import main
from main import *
import ui_advanced_config


class UIHomepage(tk.Frame):
    def __init__(self, controller, master=None, logger=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.logger = logger
        self.controller = controller

        # Create the msgr objs
        self.msg_queue = queue.Queue()
        self.imsgr = msgs.IMsgr(self.msg_queue)
        self.omsgr = msgs.OMsgr(self.msg_queue)

        self.ldr = loader.Loader(self.logger)
        self.sim = sim.Sim(self.imsgr)

        self.combat_log = []

        self.BuildUI()
        self.UIMap = None

    def Run(self):
        self.mainloop()

    def BuildUI(self):
        # self.mainFrame = uiQuietFrame(master=self)
        self.MAIALabel = uiLabel(master=self, text="Maine AI Arena")
        self.MAIALabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.btnStartGame = uiButton(
            master=self,
            text="Start Game",
            command=lambda: self.controller.show_frame("SetupPage"),
        )
        self.btnStartGame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.btnAdvancedConfig = uiButton(
            master=self,
            command=lambda: ui_advanced_config.UISettings(self, self.logger),
            text="Advanced Config",
        )
        self.btnAdvancedConfig.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.btnAbout = uiButton(
            master=self,
            text="About MAIA",
            command=lambda: self.controller.show_frame("AboutPage"),
        )
        self.btnAbout.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

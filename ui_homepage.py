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
        """Sets window and frame information and calls function to build UI"""
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

        self.build_ui()
        self.UIMap = None

    def run(self):
        self.mainloop()

    def build_ui(self):
        """Generates the homepage UI

        Places label, places start game button,
        places adv config button, places about button
        """
        # self.mainFrame = uiQuietFrame(master=self)
        self.maia_label = uiLabel(master=self, text="Maine AI Arena")
        self.maia_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.start_game_button = uiButton(
            master=self,
            text="Start Game",
            command=lambda: self.controller.show_frame("SetupPage"),
        )
        self.start_game_button.config(width=400)
        self.start_game_button.pack(side=tk.BOTTOM, fill="y", expand=True)

        self.adv_config_button = uiButton(
            master=self,
            command=lambda: ui_advanced_config.UISettings(self, self.logger),
            text="Advanced Config",
        )
        self.adv_config_button.config(width=400)
        self.adv_config_button.pack(side=tk.BOTTOM, fill="y", expand=True)

        self.about_button = uiButton(
            master=self,
            text="About MAIA",
            command=lambda: self.controller.show_frame("AboutPage"),
        )
        self.about_button.config(width=400)
        self.about_button.pack(side=tk.BOTTOM, fill="y", expand=True)

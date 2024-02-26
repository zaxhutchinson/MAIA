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
import re
import loader
import ui_sim
import msgs
from zexceptions import *
from ui_widgets import *
import ui_setup
import ui_homepage
from main import *


class aboutPage(tk.Frame):
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

        self.combat_log = []

        self.BuildUI()

        self.UIMap = None

    def BuildUI(self):
        descText = "MAIA is a platform designed for AI competitions that provides a modular 2D \
            simulation environment for which students write AI to control competing agents.\n\
            The goal is to give coders all the tools necessary so that they can focus \
            primarily on analysis of information and decision-making.\n\n\
            MAIA was developed by Dr. Zachary Hutchinson during his graduate studies \
            at the University of Maine, Orono.\n Version 0.22, the most current version of MAIA,\
            was released in October of 2020.\n Further documentation, including overviews of the \
            AI scripts, can be found in the docs directory."
        # descText = re.sub(r"  +", "", descText)
        descText2 = descText.replace("            ", "")
        descText = descText2
        self.MAIALabel = uiLabel(master=self, text="Maine AI Arena")
        self.MAIALabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.description = uiTextbox(master=self, width=60)
        self.description.insert(1.0, descText)
        self.description.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.description.config(state="disabled")
        self.btnHome = uiButton(
            master=self,
            text="Home",
            command=lambda: self.controller.show_frame("HomePage"),
        )
        self.btnHome.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

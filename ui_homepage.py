import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import importlib.util
import sys
import os
import queue
import logging
from PIL import ImageTk, Image

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

        self.build_ui()
        self.UIMap = None

    def build_ui(self):
        """Generates the homepage UI

        Places label, places start game button,
        places adv config button, places about button
        """
        # self.mainFrame = uiQuietFrame(master=self)

        self.maia_image = ImageTk.PhotoImage(Image.open("images/maia.png"))
        self.maia_image_label = uiLabel(
            master=self, image=self.maia_image
        )  # text="Maine AI Arena")
        self.maia_image_label.pack(side=tk.TOP, fill="x")
        self.maia_text_label = uiLabel(
            master=self, text="Maine AI Arena", font=("Arial", 24)
        )
        self.maia_text_label.pack(side=tk.TOP, fill="x")

        self.general_frame = tk.LabelFrame(
            self, text="General", labelanchor="n", font=("Arial", 15)
        )
        self.config_frame = tk.LabelFrame(
            self, text="Config", labelanchor="n", font=("Arial", 15)
        )
        self.match_frame = tk.LabelFrame(
            self, text="Match", labelanchor="n", font=("Arial", 15)
        )
        self.general_frame.pack(side=tk.TOP)
        self.config_frame.pack(side=tk.TOP)
        self.match_frame.pack(side=tk.TOP)

        self.about_button = uiButton(
            master=self.general_frame,
            text="About MAIA",
            command=lambda: self.controller.show_frame("about_page"),
        )
        self.about_button.config(width=400, height=100)
        self.about_button.pack(side=tk.TOP)

        self.config_teams_button = uiButton(
            master=self.config_frame,
            command=lambda: self.controller.show_frame("config_team"),
            text="Team Config",
        )
        self.config_teams_button.config(width=400, height=100)
        self.config_teams_button.grid(row=0,column=0,sticky="nsew")

        self.config_component_button = uiButton(
            master=self.config_frame,
            command=lambda: self.controller.show_frame("config_component"),
            text="Component Config",
        )
        self.config_component_button.config(width=400, height=100)
        self.config_component_button.grid(row=0,column=1,sticky="nsew")

        self.config_object_button = uiButton(
            master=self.config_frame,
            command=lambda: self.controller.show_frame("config_object"),
            text="Object Config",
        )
        self.config_object_button.config(width=400, height=100)
        self.config_object_button.grid(row=1,column=0,sticky="nsew")

        self.config_item_button = uiButton(
            master=self.config_frame,
            command=lambda: self.controller.show_frame("config_item"),
            text="Item Config"
        )
        self.config_item_button.config(width=400, height=100)
        self.config_item_button.grid(row=1, column=1, sticky="nsew")

        self.config_map_button = uiButton(
            master=self.config_frame,
            command=lambda: self.controller.show_frame("config_map"),
            text="Map Config",
        )
        self.config_map_button.config(width=400, height=100)
        self.config_map_button.grid(row=2, column=0, sticky="nsew")

        self.start_game_button = uiButton(
            master=self.match_frame,
            text="Match Setup",
            command=lambda: self.controller.show_frame("setup_page"),
        )
        self.start_game_button.config(width=400, height=100)
        self.start_game_button.pack(side=tk.TOP)

        # self.adv_config_button = uiButton(
        #     master=self,
        #     command=lambda: ui_advanced_config.UISettings(self, self.logger),
        #     text="Advanced Config",
        # )
        # self.adv_config_button.config(width=400, height=100)
        # self.adv_config_button.pack(side=tk.TOP)

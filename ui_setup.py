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
import ui_advanced_config
import msgs
from zexceptions import *
from ui_widgets import *


class UISetup(tk.Frame):
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

    def update_team_names(self):
        """Updates team names"""
        self.teams_list.delete(0, tk.END)
        self.sides_list.delete(0, tk.END)
        self.team_assignments_list.delete(0, tk.END)
        for name in self.ldr.get_team_ids():
            self.teams_list.insert(tk.END, name)
        for k, v in self.sim.get_sides().items():
            self.sides_list.insert(tk.END, k)
            self.team_assignments_list.insert(tk.END, str(self.sim.getTeamName(k)))

    def update_map_names(self):
        """Updates map names"""
        self.maps_list.delete(0, tk.END)
        for name in self.ldr.get_map_ids():
            self.maps_list.insert(tk.END, name)

    """this function is what happens when you hit button "select map"
    moved it up here so that it can be bound to selecting map in build_ui"""

    def select_map(self, event):
        """Selects map for sim

        Located here so that it can be bound to selecting map in build_ui
        """
        cur_selection = self.maps_list.curselection()
        if len(cur_selection) > 0:
            # Reset the sim
            self.sim.reset()

            # Locate the map, copy and give to sim
            map_ids = self.ldr.get_map_ids()
            selected_map = self.ldr.copy_map_template(map_ids[cur_selection[0]])
            self.sim.set_map(selected_map)

            # Construct the map info string
            map_info = "NAME:   " + selected_map.get_data("name") + "\n"
            map_info += "DESC:   " + selected_map.get_data("desc") + "\n"
            map_info += "WIDTH:  " + str(selected_map.get_data("width")) + "\n"
            map_info += "HEIGHT: " + str(selected_map.get_data("height")) + "\n"
            map_info += "TEAMS:  " + str(selected_map.get_data("teams")) + "\n"
            map_info += "AGENTS: " + str(selected_map.get_data("agents")) + "\n"
            map_info += "RANDOMLY PLACED OBJECTS:\n"
            if "rand_objects" in selected_map.data:
                for k, v in selected_map.data["rand_objects"].items():
                    map_info += "   ID:" + str(k) + " AMT:" + str(v) + "\n"
            else:
                map_info += "   NONE\n"
            map_info += "HAND-PLACED OBJECTS\n"
            if "placed_objects" in selected_map.data:
                for k, v in selected_map.data["placed_objects"].items():
                    map_info += "   ID:" + str(k) + " AMT:" + str(len(v)) + "\n"
            else:
                map_info += "   NONE\n"

            # Add string to the info text box
            self.map_info_text.delete("1.0", tk.END)
            self.map_info_text.insert(tk.END, map_info)

            self.update_team_names()

    def build_ui(self):
        """Generates the setup UI

        Places map select, places team/side assignments,
        places adv config button, places start button
        """
        ## PAGE TITLE

        self.title_label = uiLabel(master=self, text="CONFIGURATION")
        self.title_label.pack(side=tk.TOP)

        #######################################################################
        ## SIM UI
        #######################################################################
        self.sim_frame = uiQuietFrame(master=self)
        self.sim_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.start_button_frame = uiQuietFrame(master=self.sim_frame)
        self.start_button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.adv_config_button_frame = uiQuietFrame(master=self.sim_frame)
        self.adv_config_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.start_button = uiButton(
            master=self.start_button_frame,
            command=self.build_and_run_sim,
            text="Start Game",
        )  # Start Game Button
        self.start_button.pack(side=tk.RIGHT, padx=50, fill=tk.BOTH, expand=True)

        self.adv_config_button = uiButton(
            master=self.adv_config_button_frame,
            command=self.run_advanced_settings,
            text="Advanced Config",
        )
        self.adv_config_button.pack(side=tk.LEFT, padx=50, fill=tk.BOTH, expand=True)

        #######################################################################
        ## MAP UI
        #######################################################################
        self.maps_frame = uiQuietFrame(master=self)  # map section
        self.maps_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.maps_list_frame = uiQuietFrame(master=self.maps_frame)
        self.maps_list_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.maps_label = uiLabel(master=self.maps_list_frame, text="MAPS")
        self.maps_label.pack(side=tk.TOP, fill=tk.BOTH)

        self.maps_list = uiListBox(
            self.maps_list_frame
        )  # this is the box that says Map 1 maps_list
        self.maps_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.maps_list.bind(
            "<<ListboxSelect>>", self.select_map
        )  # this calls select_map(self, whateverMapIsSelectedInTheBox)

        self.map_info_frame = uiQuietFrame(master=self.maps_frame)
        self.map_info_frame.pack(side=tk.BOTTOM)

        self.map_info_label = uiLabel(
            master=self.map_info_frame, text="MAP INFORMATION"
        )
        self.map_info_label.pack(side=tk.TOP, fill=tk.BOTH)

        self.map_info_text = uiScrollText(self.map_info_frame)  # info on selected frame
        self.map_info_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.map_info_text.insert(tk.END, "No map info")

        self.update_map_names()  # this function call gets Map 1 (later other maps) into the box

        #######################################################################
        ## TEAM UI
        ######################################################################
        self.team_frame = uiQuietFrame(
            master=self
        )  # team frame is everything team UI #top line creates frame
        self.team_frame.pack_propagate(0)
        self.team_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )  # bottom line is frame settings

        self.team_pool_frame = uiQuietFrame(
            master=self.team_frame
        )  # Left half of team frame
        self.team_pool_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.team_pool_left_frame = uiQuietFrame(
            master=self.team_pool_frame
        )  # part of pool frame, pool section
        self.team_pool_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.team_pool_label = uiLabel(
            master=self.team_pool_left_frame, text="TEAM POOL"
        )  # label that says "Team Pool" section of pool left frame
        self.team_pool_label.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.teams_list = uiListBox(self.team_pool_left_frame)
        self.teams_list.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.team_pool_right_frame = uiQuietFrame(
            master=self.team_pool_frame
        )  # pool right frame is the sides section, also part of Pool Frame
        self.team_pool_right_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.sides_label = uiLabel(master=self.team_pool_right_frame, text="SIDES")
        self.sides_label.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.sides_list = uiListBox(self.team_pool_right_frame)
        self.sides_list.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.play_pool_frame = uiQuietFrame(
            master=self.team_frame
        )  # Assigned is other half of team frame, "Play pool" is teams that are playing
        self.play_pool_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.play_pool_right_frame = uiQuietFrame(master=self.play_pool_frame)
        self.play_pool_right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5
        )

        self.play_pool_label = uiLabel(
            master=self.play_pool_right_frame, text="ASSIGNED TEAMS"
        )
        self.play_pool_label.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.sub_play_pool_frame = uiQuietFrame(master=self.play_pool_right_frame)
        self.sub_play_pool_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

        self.team_assignments_list = uiListBox(self.sub_play_pool_frame)
        self.team_assignments_list.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.update_team_names()

        self.pack(fill=tk.BOTH, expand=True)

        self.add_team_button = uiButton(
            master=self.play_pool_frame, text="Add Team >>>", command=self.add_team
        )
        self.add_team_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

        self.remove_team_button = uiButton(
            master=self.play_pool_frame,
            text="<<< Remove Team",
            command=self.remove_team,
        )
        self.remove_team_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=5)

    def add_team(self):
        """Adds team/side assignment to sim"""
        if self.sim.has_map():
            team_index = self.teams_list.curselection()
            side_index = self.sides_list.curselection()
            if len(team_index) > 0 and len(side_index) > 0:

                all_sides = self.sides_list.get(0, tk.END)
                side_selection = all_sides[side_index[0]]
                team_name = self.ldr.get_team_ids()[team_index[0]]

                self.sim.add_team_name(side_selection, team_name)
                self.update_team_names()
            else:
                self.logger.error("App::add_team() - No side or team selected.")
        else:
            self.logger.error("App::add_team() - Sim is missing the map.")

    def remove_team(self):
        """Removes team/side assignment from sim"""
        team_index = self.team_assignments_list.curselection()
        if len(team_index) > 0:
            all_sides = self.sides_list.get(0, tk.END)
            side_ID = all_sides[team_index[0]]
            self.sim.del_team_name(side_ID)
            self.update_team_names()

    def build_and_run_sim(self):
        """Builds and runs sim"""
        try:
            self.sim.build_sim(self.ldr)
        except BuildException as e:
            tk.messagebox.showinfo(title="Build Exception", message=e)
        else:
            # tk.messagebox.showinfo(title="Success",message="Sim build was successful.")    --this line makes a pop up
            map_width = self.sim.get_map().get_data("width")
            map_height = self.sim.get_map().get_data("height")
            self.UIMap = ui_sim.UISim(
                map_width,
                map_height,
                self.sim,
                self.omsgr,
                self.controller,
                self,
                self.logger,
            )

    def run_advanced_settings(self):
        """Opens advanced config settings"""
        self.UIMap = ui_advanced_config.UISettings(self, self.logger)

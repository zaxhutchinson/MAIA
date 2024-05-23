import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging
import loader
import json
import comp
import obj
import zmap
from tkinter.messagebox import askyesno
from tkinter.messagebox import showwarning
from tkinter.simpledialog import askstring

import ui_map_config
from ui_widgets import *


class UITeamConfig(tk.Frame):
    def __init__(self, controller, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=BGCOLOR)
        # self.title("MAIA - Advanced Configuration")

        # self.geometry("1450x700")
        # self.minsize(width=1400, height=700)
        self.logger = logger
        self.ldr = loader.Loader(self.logger)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.fixed_gun_keys = [
            "reload_ticks",
            "reload_ticks_remaining",
            "reloading",
            "ammunition",
            "min_damage",
            "max_damage",
            "range",
        ]
        self.engine_keys = [
            "min_speed",
            "max_speed",
            "cur_speed",
            "max_turnrate",
            "cur_turnrate",
        ]
        self.radar_keys = [
            "active",
            "range",
            "level",
            "visarc",
            "offset_angle",
            "resolution",
        ]
        self.cnc_keys = ["max_cmds_per_tick"]
        self.radio_keys = ["max_range", "cur_range", "message"]
        self.arm_keys = ["max_weight", "max_bulk", "item"]

        self.prev_component_combo = None

        self.build_ui()

        self.ui_map = None

    def validate_number_entry(self, input):
        """
        Validates each entered value (input) to ensure it is a number.
        """
        input.replace(".", "", 1)
        input.replace("-", "", 1)
        if input.isdigit() or input == "" or "-" in input or "." in input:
            return True

        else:
            return False

    def get_focused_entry(self):
        """
        Returns the currently focused entry in advanced config.
        """
        focused_entry = self.focus_get()
        return focused_entry

    def build_ui(self):
        """
        Initializes all widgets and places them.
        """
        # Make main widgets

        self.main_frame = uiQuietFrame(master=self)
        self.teams_column = uiQuietFrame(master=self.main_frame)
        self.components_column = uiQuietFrame(master=self.main_frame)
        self.objects_column = uiQuietFrame(master=self.main_frame)
        self.maps_column = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Advanced Settings")

        self.validate_num = self.teams_column.register(self.validate_number_entry)

        # Place main widgets
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Make Team Widgets

        self.select_team_combo = uiComboBox(master=self.teams_column)
        self.select_team_combo.configure(state="readonly")
        self.teams_label = uiLabel(master=self.teams_column, text="Teams")
        self.team_size_label = uiLabel(master=self.teams_column, text="Size:")
        self.team_size_entry = EntryHelp(
            master=self.teams_column,
            text=(
                "The team size field represents how many agents you want in the selected team."
                " This field takes numeric values only."
            ),
        )
        self.team_size_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.team_name_label = uiLabel(master=self.teams_column, text="Name:")
        self.team_name_entry = EntryHelp(master=self.teams_column, text="To be added.")
        self.agent_frame = uiQuietFrame(
            master=self.teams_column, borderwidth=5, relief="ridge", sticky="nsew"
        )
        self.callsign_label = uiLabel(master=self.agent_frame, text="Callsign:")
        self.callsign_entry = EntryHelp(master=self.agent_frame, text="To be added.")
        self.squad_label = uiLabel(master=self.agent_frame, text="Squad:")
        self.squad_entry = EntryHelp(master=self.agent_frame, text="To be added.")
        self.agent_object_label = uiLabel(master=self.agent_frame, text="Object:")
        self.agent_object_entry = EntryHelp(
            master=self.agent_frame, text="To be added."
        )
        self.ai_file_label = uiLabel(master=self.agent_frame, text="AI File:")
        self.ai_file_entry = EntryHelp(master=self.agent_frame, text="To be added.")
        self.teams_update_button = uiButton(
            master=self.teams_column, command=self.update_teams_json, text="Update"
        )
        self.teams_create_button = uiButton(
            master=self.teams_column, command=self.create_team, text="Create"
        )
        self.teams_delete_button = uiButton(
            master=self.teams_column, command=self.delete_team, text="Delete"
        )

        # Place Team Widgets
        self.teams_column.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )
        self.select_team_combo.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10
        )
        self.teams_label.grid(row=2, column=1, columnspan=2, sticky="nsew")
        self.team_size_label.grid(row=3, column=1, sticky="nsew")
        self.team_size_entry.frame.grid(row=3, column=2, sticky="nsew")
        self.team_name_label.grid(row=4, column=1, sticky="nsew")
        self.team_name_entry.frame.grid(row=4, column=2, sticky="nsew")
        self.agent_frame.grid(
            row=5, column=1, columnspan=2, rowspan=2, sticky="nsew", ipadx=0, ipady=0
        )
        self.callsign_label.grid(row=1, column=1, sticky="nsew")
        self.callsign_entry.frame.grid(row=1, column=2, sticky="nsew")
        self.squad_label.grid(row=2, column=1, sticky="nsew")
        self.squad_entry.frame.grid(row=2, column=2, sticky="nsew")
        self.agent_object_label.grid(row=3, column=1, sticky="nsew")
        self.agent_object_entry.frame.grid(row=3, column=2, sticky="nsew")
        self.ai_file_label.grid(row=4, column=1, sticky="nsew")
        self.ai_file_entry.frame.grid(row=4, column=2, sticky="nsew")
        self.teams_update_button.grid(
            row=7,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.teams_create_button.grid(
            row=8,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.teams_delete_button.grid(
            row=9,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        

        self.init_entry_widgets()

    def init_entry_widgets(self):
        """
        Gets information from the loader and assigns current values for each setting type.
        """
        # TEAM
        self.team_data = self.ldr.team_templates
        self.team_names = self.ldr.get_team_names()
        self.current_team_data = self.team_data[self.team_names[0]]

        self.select_team_combo.configure(values=self.team_names)
        self.select_team_combo.current(0)
        self.select_team_combo.bind(
            "<<ComboboxSelected>>", self.change_team_entry_widgets
        )
        self.select_team_combo.bind("<Enter>", self.get_previous_team_combo)
        self.show_team_entry(self.current_team_data)

    ### DELETE ###

    def delete_team(self):
        """
        Deletes the currently selected team from the JSON and team dictionary.
        """
        if self.select_team_combo.get() in self.team_data:
            self.team_data.pop(self.select_team_combo.get())
            self.team_names.pop(self.select_team_combo.current())

            with open("settings/teams.json", "r") as f:
                team_json = json.load(f)
            f.close()
            team_json.pop(self.select_team_combo.get())
            with open("settings/teams.json", "w") as f:
                json.dump(team_json, f, indent=4)
            f.close()

            self.select_team_combo.configure(values=self.team_names)
            self.select_team_combo.current(len(self.team_names) - 1)
            self.change_team_entry_widgets()

        



    def get_previous_team_combo(self, event):
        self.prev_team_combo = self.select_team_combo.current()

    def change_team_entry_widgets(self, event=None):
        """
        Gets the correct team data for the currently selected team.
        """
        # the answer variable defaults to true
        self.answer = True
        self.get_focused_entry()
        # if any of the team entry values differ from their starting values,
        # the user is warned that they could be overwritten
        if not (
            (
                (self.team_name_entry.entry.get() == self.current_team_data["name"])
                and (
                    self.team_size_entry.entry.get()
                    == str(self.current_team_data["size"])
                )
                and (
                    self.callsign_entry.entry.get()
                    == self.current_team_data["agent_defs"][0]["callsign"]
                )
                and (
                    self.squad_entry.entry.get()
                    == self.current_team_data["agent_defs"][0]["squad"]
                )
                and (
                    self.agent_object_entry.entry.get()
                    == self.current_team_data["agent_defs"][0]["object"]
                )
                and (
                    self.ai_file_entry.entry.get()
                    == self.current_team_data["agent_defs"][0]["AI_file"]
                )
            )
        ):
            self.answer = askyesno(
                title="confirmation",
                message="""Warning: You have modified Team values and have not Updated.
                  Your changes will not be saved. Are you sure you would like continue?""",
            )

        # the current team is successfully changed if the user made no changes,
        # or if the user confirms they are fine with their changes being overwritten
        if self.answer:
            # currentTeamIdx = self.selectTeamCombo.current()
            self.current_team_data = self.team_data[self.select_team_combo.get()]
            self.show_team_entry(self.current_team_data)
        else:
            self.select_team_combo.current(self.prev_team_combo)

    

    def show_team_entry(self, current_team):
        """
        Updates the values stored in the team entry widgets.
        """
        self.team_name_entry.entry.delete(0, tk.END)
        self.team_name_entry.entry.insert(0, current_team["name"])
        self.team_size_entry.entry.delete(0, tk.END)
        self.team_size_entry.entry.insert(0, current_team["size"])
        self.callsign_entry.entry.delete(0, tk.END)
        self.callsign_entry.entry.insert(
            0, self.current_team_data["agent_defs"][0]["callsign"]
        )
        self.squad_entry.entry.delete(0, tk.END)
        self.squad_entry.entry.insert(0, current_team["agent_defs"][0]["squad"])
        self.agent_object_entry.entry.delete(0, tk.END)
        self.agent_object_entry.entry.insert(0, current_team["agent_defs"][0]["object"])
        self.ai_file_entry.entry.delete(0, tk.END)
        self.ai_file_entry.entry.insert(0, current_team["agent_defs"][0]["AI_file"])

    

    ### UPDATE JSON FILES###
    def update_teams_json(self):
        """
        Updates the teams JSON values.
        """
        if (
            self.team_name_entry.entry.get() in self.team_data.keys()
            and self.team_name_entry.entry.get() != self.select_team_combo.get()
        ):
            showwarning(
                title="Warning",
                message="The name you are trying to use is already in use by another team. Please use another name.",
            )
        else:
            if (
                self.team_size_entry.entry.get() != ""
                and self.callsign_entry.entry.get() != ""
                and self.team_name_entry.entry.get() != ""
                and self.squad_entry.entry.get() != ""
                and self.agent_object_entry.entry.get() != ""
                and self.ai_file_entry.entry.get() != ""
            ):
                self.current_team_data["size"] = int(self.team_size_entry.entry.get())
                self.current_team_data["agent_defs"][0][
                    "callsign"
                ] = self.callsign_entry.entry.get()
                self.current_team_data["name"] = self.team_name_entry.entry.get()
                self.current_team_data["agent_defs"][0][
                    "squad"
                ] = self.squad_entry.entry.get()
                self.current_team_data["agent_defs"][0][
                    "object"
                ] = self.agent_object_entry.entry.get()
                self.current_team_data["agent_defs"][0][
                    "AI_file"
                ] = self.ai_file_entry.entry.get()

                self.team_data.update(
                    {self.current_team_data["name"]: self.current_team_data}
                )

                self.teams_json = json.dumps(self.team_data, indent=4)

                with open("settings/teams.json", "r") as f:
                    team_json = json.load(f)

                if self.current_team_data["name"] != self.select_team_combo.get():
                    if self.select_team_combo.get() in team_json:
                        team_json.pop(self.select_team_combo.get())
                    if self.select_team_combo.get() in self.team_data:
                        self.team_data.pop(self.select_team_combo.get())
                    self.team_names.pop(self.select_team_combo.current())
                    self.team_names.append(self.current_team_data["name"])
                    self.select_team_combo.config(values=self.team_names)
                    self.select_team_combo.current(len(self.team_names) - 1)

                team_json[self.current_team_data["name"]] = self.current_team_data

                self.team_data[self.current_team_data["name"]] = self.current_team_data

                f.close()

                with open("settings/teams.json", "w") as f:
                    json.dump(team_json, f, indent=4)
                f.close()

    

    ### CREATE NEW ###

    def create_team(self):
        """
        Creates a new team and adds it to the team dictionary.
        """
        self.team_id = askstring("Team ID", "Please enter an ID for the new team.")
        while len(self.team_id) == 0 or self.team_id in self.team_data.keys():
            if len(self.team_id) == 0:
                messagebox.showwarning(
                    "Warning", "You must enter a team ID to continue"
                )
            else:
                messagebox.showwarning(
                    "Warning", "This ID already exists, please enter a new ID."
                )
            self.team_id = askstring("Team ID", "Please enter an ID for the new team.")
        if len(self.team_id) != 0:
            self.team_names.append(self.team_id)
            self.select_team_combo.configure(values=self.team_names)
            self.select_team_combo.current(len(self.team_names) - 1)
            self.current_team_data = {
                "size": "",
                "name": self.team_id,
                "agent_defs": [
                    {"callsign": "", "squad": "", "object": "", "AI_file": ""}
                ],
            }
            self.team_data.update({self.team_id: self.current_team_data})
            self.show_team_entry(self.current_team_data)

    

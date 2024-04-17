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


class UISettings(tk.Toplevel):
    def __init__(self, master=None, logger=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=BGCOLOR)
        self.title("MAIA - Advanced Configuration")

        self.geometry("1450x700")
        self.minsize(width=1400, height=700)
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
        self.agent_object_entry = EntryHelp(master=self.agent_frame, text="To be added.")
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
        self.teams_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
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

        # Make Component Widgets
        self.select_component_combo = uiComboBox(master=self.components_column)
        self.select_component_combo.configure(state="readonly")
        self.components_label = uiLabel(master=self.components_column, text="Components")
        self.components_update_button = uiButton(
            master=self.components_column,
            command=self.update_components_json,
            text="Update",
        )
        self.components_create_button = uiButton(
            master=self.components_column, command=self.create_component, text="Create"
        )
        self.components_delete_button = uiButton(
            master=self.components_column, command=self.delete_components, text="Delete"
        )
        self.components_id_label = uiLabel(master=self.components_column, text="ID:")
        self.components_id_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_name_label = uiLabel(master=self.components_column, text="Name:")
        self.components_name_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_ctype_label = uiLabel(master=self.components_column, text="CType:")
        self.components_type_label = uiLabel(master=self.components_column, text="")
        self.components_type_combo = uiComboBox(master=self.components_column)
        self.components_type_attr1_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr1_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr2_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr2_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr3_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr3_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr4_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr4_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr5_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr5_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr6_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr6_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr7_label = uiLabel(master=self.components_column, text="")
        self.components_type_attr7_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )

        # Place Component Widgets
        self.components_column.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )
        self.select_component_combo.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10
        )
        self.components_label.grid(row=2, column=1, columnspan=2, sticky="nsew")
        self.components_id_label.grid(row=3, column=1, sticky="nsew")
        self.components_id_entry.frame.grid(row=3, column=2, sticky="nsew")
        self.components_name_label.grid(row=4, column=1, sticky="nsew")
        self.components_name_entry.frame.grid(row=4, column=2, sticky="nsew")
        self.components_ctype_label.grid(row=5, column=1, sticky="nsew")
        self.components_type_label.grid(row=5, column=2, sticky="nsew")

        self.components_type_attr1_label.grid(row=6, column=1, sticky="nsew")
        self.components_type_attr1_entry.frame.grid(row=6, column=2, sticky="nsew")
        self.components_type_attr1_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr2_label.grid(row=7, column=1, sticky="nsew")
        self.components_type_attr2_entry.frame.grid(row=7, column=2, sticky="nsew")
        self.components_type_attr2_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr3_label.grid(row=8, column=1, sticky="nsew")
        self.components_type_attr3_entry.frame.grid(row=8, column=2, sticky="nsew")
        self.components_type_attr3_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr4_label.grid(row=9, column=1, sticky="nsew")
        self.components_type_attr4_entry.frame.grid(row=9, column=2, sticky="nsew")
        self.components_type_attr4_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr5_label.grid(row=10, column=1, sticky="nsew")
        self.components_type_attr5_entry.frame.grid(row=10, column=2, sticky="nsew")
        self.components_type_attr5_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr6_label.grid(row=11, column=1, sticky="nsew")
        self.components_type_attr6_entry.frame.grid(row=11, column=2, sticky="nsew")
        self.components_type_attr6_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr7_label.grid(row=12, column=1, sticky="nsew")
        self.components_type_attr7_entry.frame.grid(row=12, column=2, sticky="nsew")
        self.components_type_attr7_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_combo.grid(row=13, column=1, columnspan=2, sticky="nsew")
        self.components_update_button.grid(
            row=14,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.components_create_button.grid(
            row=15,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.components_delete_button.grid(
            row=16,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )

        # Make Object Widgets
        self.select_objects_combo = uiComboBox(master=self.objects_column)
        self.select_objects_combo.configure(state="readonly")
        self.objects_label = uiLabel(master=self.objects_column, text="Objects")
        self.objects_update_button = uiButton(
            master=self.objects_column, command=self.update_objects_json, text="Update"
        )
        self.objects_create_button = uiButton(
            master=self.objects_column, command=self.create_object, text="Create"
        )
        self.objects_delete_button = uiButton(
            master=self.objects_column, command=self.delete_object, text="Delete"
        )
        self.objects_id_label = uiLabel(master=self.objects_column, text="ID:")
        self.objects_id_entry = EntryHelp(master=self.objects_column, text="To be added.")
        self.objects_name_label = uiLabel(master=self.objects_column, text="Name:")
        self.objects_name_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_fill_alive_label = uiLabel(
            master=self.objects_column, text="Fill Alive:"
        )
        self.objects_fill_alive_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_fill_dead_label = uiLabel(
            master=self.objects_column, text="Fill Dead:"
        )
        self.objects_fill_dead_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_text_label = uiLabel(master=self.objects_column, text="Text:")
        self.objects_text_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_health_label = uiLabel(master=self.objects_column, text="Health:")
        self.objects_health_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_health_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.objects_density_label = uiLabel(master=self.objects_column, text="Density:")
        self.objects_density_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_density_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.objects_comp_ids_label = uiLabel(master=self.objects_column, text="Comp IDs:")
        self.objects_comp_ids_combo = ComboBoxHelp(master=self.objects_column, text="To be Added.")
        self.objects_points_count_label = uiLabel(
            master=self.objects_column, text="Points Count:"
        )
        self.objects_points_count_combo = ComboBoxHelp(master=self.objects_column, text="To be Added.")

        # Place Object Widgets
        self.objects_column.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )
        self.select_objects_combo.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10
        )
        self.objects_label.grid(row=2, column=1, columnspan=2, sticky="nsew")
        self.objects_id_label.grid(row=3, column=1, sticky="nsew")
        self.objects_id_entry.frame.grid(row=3, column=2, sticky="nsew")
        self.objects_name_label.grid(row=4, column=1, sticky="nsew")
        self.objects_name_entry.frame.grid(row=4, column=2, sticky="nsew")
        self.objects_fill_alive_label.grid(row=5, column=1, sticky="nsew")
        self.objects_fill_alive_entry.frame.grid(row=5, column=2, sticky="nsew")
        self.objects_fill_dead_label.grid(row=6, column=1, sticky="nsew")
        self.objects_fill_dead_entry.frame.grid(row=6, column=2, sticky="nsew")
        self.objects_text_label.grid(row=7, column=1, sticky="nsew")
        self.objects_text_entry.frame.grid(row=7, column=2, sticky="nsew")
        self.objects_health_label.grid(row=8, column=1, sticky="nsew")
        self.objects_health_entry.frame.grid(row=8, column=2, sticky="nsew")
        self.objects_density_label.grid(row=9, column=1, sticky="nsew")
        self.objects_density_entry.frame.grid(row=9, column=2, sticky="nsew")
        self.objects_comp_ids_label.grid(row=10, column=1, sticky="nsew")
        self.objects_comp_ids_combo.frame.grid(row=10, column=2, sticky="nsew")
        self.objects_points_count_label.grid(row=11, column=1, sticky="nsew")
        self.objects_points_count_combo.frame.grid(row=11, column=2, sticky="nsew")
        self.objects_update_button.grid(
            row=12,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.objects_create_button.grid(
            row=13,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.objects_delete_button.grid(
            row=14,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )

        # Make Map Widgets
        self.select_maps_combo = uiComboBox(master=self.maps_column)
        self.select_maps_combo.configure(state="readonly")
        self.maps_label = uiLabel(master=self.maps_column, text="Maps")
        self.maps_show_button = uiButton(
            master=self.maps_column, command=self.show_map, text="Show"
        )
        self.maps_update_button = uiButton(
            master=self.maps_column, command=self.update_maps_json, text="Update"
        )
        self.maps_create_button = uiButton(
            master=self.maps_column, command=self.create_map, text="Create"
        )
        self.maps_delete_button = uiButton(
            master=self.maps_column, command=self.delete_map, text="Delete"
        )
        self.maps_id_label = uiLabel(master=self.maps_column, text="ID:")
        self.maps_id_entry = EntryHelp(master=self.maps_column, text="To be added.")
        self.maps_name_label = uiLabel(master=self.maps_column, text="Name:")
        self.maps_name_entry = EntryHelp(master=self.maps_column, text="To be added.")
        self.maps_edge_obj_id_label = uiLabel(
            master=self.maps_column, text="Edge Object ID:"
        )
        self.maps_edge_obj_id_entry = EntryHelp(master=self.maps_column, text="To be added.")
        self.maps_desc_label = uiLabel(master=self.maps_column, text="Desc:")
        self.maps_desc_entry = EntryHelp(master=self.maps_column, text="To be added.")
        self.maps_width_label = uiLabel(master=self.maps_column, text="Width:")
        self.maps_width_entry = EntryHelp(master=self.maps_column, text="To be added.")
        self.maps_height_label = uiLabel(master=self.maps_column, text="Height:")
        self.maps_height_entry = EntryHelp(master=self.maps_column, text="To be added.")

        # Place Map Widgets
        self.maps_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.select_maps_combo.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10
        )
        self.maps_label.grid(row=2, column=1, columnspan=2, sticky="nsew")
        self.maps_id_label.grid(row=3, column=1, sticky="nsew")
        self.maps_id_entry.frame.grid(row=3, column=2, sticky="nsew")
        self.maps_name_label.grid(row=4, column=1, sticky="nsew")
        self.maps_name_entry.frame.grid(row=4, column=2, sticky="nsew")
        self.maps_edge_obj_id_label.grid(row=5, column=1, sticky="nsew")
        self.maps_edge_obj_id_entry.frame.grid(row=5, column=2, sticky="nsew")
        self.maps_desc_label.grid(row=6, column=1, sticky="nsew")
        self.maps_desc_entry.frame.grid(row=6, column=2, sticky="nsew")
        self.maps_width_label.grid(row=7, column=1, sticky="nsew")
        self.maps_width_entry.frame.grid(row=7, column=2, sticky="nsew")
        self.maps_width_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.maps_height_label.grid(row=8, column=1, sticky="nsew")
        self.maps_height_entry.frame.grid(row=8, column=2, sticky="nsew")
        self.maps_height_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.maps_show_button.grid(
            row=9,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.maps_update_button.grid(
            row=10,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.maps_create_button.grid(
            row=11,
            column=1,
            columnspan=2,
            sticky="nsew",
            ipadx=2,
            ipady=2,
            padx=10,
            pady=10,
        )
        self.maps_delete_button.grid(
            row=12,
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
        self.team_names = self.ldr.getTeamNames()
        self.current_team_data = self.team_data[self.team_names[0]]

        self.select_team_combo.configure(values=self.team_names)
        self.select_team_combo.current(0)
        self.select_team_combo.bind(
            "<<ComboboxSelected>>", self.change_team_entry_widgets
        )
        self.select_team_combo.bind("<Enter>", self.get_previous_team_combo)
        self.show_team_entry(self.current_team_data)

        # COMPONENT
        self.component_data = self.ldr.comp_templates
        self.component_ids = self.ldr.getCompIDs()
        self.component_names = self.ldr.getCompNames()
        for i in range(len(self.component_ids)):
            self.component_ids[i] = self.component_ids[i] + ": " + self.component_names[i]
        self.component_types = self.ldr.getCompTypes()
        self.current_component_data = self.component_data[
            self.component_ids[0].split(":")[0]
        ]
        self.component_type_attr = self.current_component_data.view_keys

        self.select_component_combo.configure(values=self.component_ids)
        self.select_component_combo.current(0)
        self.select_component_combo.bind(
            "<<ComboboxSelected>>", self.change_components_entry_widgets
        )
        self.select_component_combo.bind("<Enter>", self.get_previous_component_combo)

        self.show_component_entries(self.current_component_data)

        # OBJECT
        self.object_data = self.ldr.obj_templates
        self.object_ids = self.ldr.getObjIDs()
        self.current_object_data = self.object_data[self.object_ids[0]]
        self.object_names = self.ldr.getObjNames()
        for i in range(len(self.object_ids)):
            self.object_ids[i] = self.object_ids[i] + ": " + self.object_names[i]
        self.current_object_data = self.object_data[self.object_ids[0].split(":")[0]]
        self.select_objects_combo.configure(values=self.object_ids)
        self.select_objects_combo.current(0)
        self.select_objects_combo.bind(
            "<<ComboboxSelected>>", self.change_objects_entry_widgets
        )
        self.select_objects_combo.bind("<Enter>", self.get_previous_object_combo)

        self.show_object_entry(self.current_object_data)

        # MAP
        self.map_data = self.ldr.map_templates
        self.map_ids = self.ldr.getMapIDs()
        self.current_map_data = self.map_data[self.map_ids[0]]

        self.select_maps_combo.configure(values=self.map_ids)
        self.select_maps_combo.current(0)
        self.select_maps_combo.bind(
            "<<ComboboxSelected>>", self.change_maps_entry_widgets
        )
        self.select_maps_combo.bind("<Enter>", self.get_previous_map_combo)

        self.show_map_entry(self.current_map_data)

    def get_previous_component_combo(self, event):
        self.prev_component_combo = self.select_component_combo.current()

    def get_previous_object_combo(self, event):
        self.prev_object_combo = self.select_objects_combo.current()

    def get_previous_map_combo(self, event):
        self.prev_map_combo = self.select_maps_combo.current()

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
                    self.team_size_entry.entry.get() == str(self.current_team_data["size"])
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

    def change_components_entry_widgets(self, event=None):
        """
        Gets the correct component data for the currently selected team.
        """
        self.answer = True

        if self.current_component_data.getData("ctype") == "CnC":
            ctype_attributes = self.cnc_keys
        elif self.current_component_data.getData("ctype") == "FixedGun":
            ctype_attributes = self.fixed_gun_keys
        elif self.current_component_data.getData("ctype") == "Engine":
            ctype_attributes = self.engine_keys
        elif self.current_component_data.getData("ctype") == "Radar":
            ctype_attributes = self.radar_keys
        elif self.current_component_data.getData("ctype") == "Radio":
            ctype_attributes = self.radio_keys
        elif self.current_component_data.getData("ctype") == "Arm":
            ctype_attributes = self.arm_keys

        if not (
            (
                (
                    self.components_id_entry.entry.get()
                    == self.current_component_data.getData("id")
                )
                and (
                    self.components_name_entry.entry.get()
                    == self.current_component_data.getData("name")
                )
                and (
                    self.components_type_combo.get()
                    == self.current_component_data.getData("ctype")
                )
                and (
                    self.components_type_attr1_entry.entry.get()
                    == str(self.current_component_data.getData(ctype_attributes[0]))
                )
                and (
                    (len(ctype_attributes) < 2)
                    or (
                        self.components_type_attr2_entry.entry.get()
                        == str(self.current_component_data.getData(ctype_attributes[1]))
                    )
                )
                and (
                    (len(ctype_attributes) < 3)
                    or self.current_component_data.getData(ctype_attributes[2]) is None
                    or (
                        self.components_type_attr3_entry.entry.get()
                        == str(self.current_component_data.getData(ctype_attributes[2]))
                    )
                )
                and (
                    (len(ctype_attributes) < 4)
                    or (
                        self.components_type_attr4_entry.entry.get()
                        == str(self.current_component_data.getData(ctype_attributes[3]))
                    )
                )
                and (
                    (len(ctype_attributes) < 5)
                    or (
                        self.components_type_attr5_entry.entry.get()
                        == str(self.current_component_data.getData(ctype_attributes[4]))
                    )
                )
                and (
                    (len(ctype_attributes) < 6)
                    or (
                        self.components_type_attr6_entry.entry.get()
                        == str(self.current_component_data.getData(ctype_attributes[5]))
                    )
                )
                and (
                    (len(ctype_attributes) < 7)
                    or (
                        self.components_type_attr7_entry.entry.get()
                        == str(self.current_component_data.getData(ctype_attributes[6]))
                    )
                )
            )
        ):
            self.answer = askyesno(
                title="confirmation",
                message="""Warning: You have modified Component values and have not Updated.
                 Your changes will not be saved. Are you sure you would like continue?""",
            )

        if self.answer is True:
            current_component_idx = self.select_component_combo.current()
            self.component_type_attr = self.component_data[
                self.component_ids[current_component_idx].split(":")[0]
            ].view_keys
            self.current_component_data = self.component_data[
                self.component_ids[current_component_idx].split(":")[0]
            ]
            self.show_component_entries(self.current_component_data)
        else:
            self.select_component_combo.current(self.prev_component_combo)

    def change_objects_entry_widgets(self, event=None):
        """
        Gets the correct object data for the currently selected team.
        """
        self.answer = True
        comp_ids = self.current_comp_ids
        if len(comp_ids) != 0:
            if comp_ids[-1] == "Add New Comp ID":
                comp_ids.pop(-1)
        if not (
            (
                (
                    self.objects_id_entry.entry.get()
                    == self.current_object_data.getData("id")
                )
                and (
                    self.objects_name_entry.entry.get()
                    == self.current_object_data.getData("name")
                )
                and (
                    self.objects_fill_alive_entry.entry.get()
                    == self.current_object_data.getData("fill_alive")
                )
                and (
                    self.objects_fill_dead_entry.entry.get()
                    == self.current_object_data.getData("fill_dead")
                )
                and (
                    self.objects_text_entry.entry.get()
                    == self.current_object_data.getData("text")
                )
                and (
                    self.objects_health_entry.entry.get()
                    == str(self.current_object_data.getData("health"))
                )
                and (
                    self.objects_density_entry.entry.get()
                    == str(self.current_object_data.getData("density"))
                )
                and (comp_ids == self.current_object_data.getData("comp_ids"))
                and (
                    bool(self.objects_points_count_combo.combobox.current())
                    == self.current_object_data.getData("points_count")
                )
            )
        ):
            self.answer = askyesno(
                title="confirmation",
                message="""Warning: You have modified Object values and have not Updated.
                 Your changes will not be saved. Are you sure you would like continue?""",
            )

        if self.answer:
            current_object = self.select_objects_combo.get()
            self.current_object_data = self.object_data[current_object.split(":")[0]]

            self.show_object_entry(self.current_object_data)
        else:
            self.select_objects_combo.current(self.prev_object_combo)

    def change_maps_entry_widgets(self, event=None):
        """
        Gets the correct map data for the currently selected team.
        """
        self.answer = True

        if not (
            (
                (self.maps_name_entry.entry.get() == self.current_map_data.getData("name"))
                and (
                    self.maps_edge_obj_id_entry.entry.get()
                    == self.current_map_data.getData("edge_obj_id")
                )
                and (
                    self.maps_desc_entry.entry.get()
                    == self.current_map_data.getData("desc")
                )
                and (
                    int(self.maps_width_entry.entry.get())
                    == self.current_map_data.getData("width")
                )
                and (
                    int(self.maps_height_entry.entry.get())
                    == self.current_map_data.getData("height")
                )
            )
        ):
            self.answer = askyesno(
                title="confirmation",
                message="""Warning: You have modified Map values and have not Updated.
                 Your changes will not be saved. Are you sure you would like continue?""",
            )
        if self.answer is True:
            current_map_id = self.select_maps_combo.get()
            self.current_map_data = self.map_data[current_map_id]

            self.show_map_entry(self.current_map_data)
        else:
            self.select_maps_combo.current()

    def show_component_entries(self, current_comp):
        """
        Updates the values in the component entry widgets.
        """
        self.component_type_attr = current_comp.view_keys
        self.components_id_entry.entry.delete(0, tk.END)
        self.components_id_entry.entry.insert(0, current_comp.getData("id"))
        self.components_name_entry.entry.delete(0, tk.END)
        self.components_name_entry.entry.insert(
            0,
            current_comp.getData("name"),
        )
        self.components_type_combo.configure(values=self.component_types)
        self.components_type_combo.set(current_comp.getData("ctype"))
        self.components_type_label.config(text=current_comp.getData("ctype"))
        self.components_type_attr1_entry.entry.configure(state="normal")
        self.components_type_attr2_entry.entry.configure(state="normal")
        self.components_type_attr3_entry.entry.configure(state="normal")
        self.components_type_attr4_entry.entry.configure(state="normal")
        self.components_type_attr5_entry.entry.configure(state="normal")
        self.components_type_attr6_entry.entry.configure(state="normal")
        self.components_type_attr7_entry.entry.configure(state="normal")
        self.components_type_attr1_entry.help_button.configure(state="normal")
        self.components_type_attr2_entry.help_button.configure(state="normal")
        self.components_type_attr3_entry.help_button.configure(state="normal")
        self.components_type_attr4_entry.help_button.configure(state="normal")
        self.components_type_attr5_entry.help_button.configure(state="normal")
        self.components_type_attr6_entry.help_button.configure(state="normal")
        self.components_type_attr7_entry.help_button.configure(state="normal")
        self.components_type_attr1_label.config(text="")
        self.components_type_attr2_label.config(text="")
        self.components_type_attr3_label.config(text="")
        self.components_type_attr4_label.config(text="")
        self.components_type_attr5_label.config(text="")
        self.components_type_attr6_label.config(text="")
        self.components_type_attr7_label.config(text="")
        self.components_type_attr1_entry.entry.delete(0, tk.END)
        self.components_type_attr1_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr2_entry.entry.delete(0, tk.END)
        self.components_type_attr3_entry.entry.delete(0, tk.END)
        self.components_type_attr3_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.components_type_attr4_entry.entry.delete(0, tk.END)
        self.components_type_attr5_entry.entry.delete(0, tk.END)
        self.components_type_attr6_entry.entry.delete(0, tk.END)
        self.components_type_attr7_entry.entry.delete(0, tk.END)

        if current_comp.getData("ctype") == "CnC":
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[4])
            )
            self.components_type_attr2_entry.entry.configure(state="readonly")
            self.components_type_attr3_entry.entry.configure(state="readonly")
            self.components_type_attr4_entry.entry.configure(state="readonly")
            self.components_type_attr5_entry.entry.configure(state="readonly")
            self.components_type_attr6_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr2_entry.help_button.configure(state="disabled")
            self.components_type_attr3_entry.help_button.configure(state="disabled")
            self.components_type_attr4_entry.help_button.configure(state="disabled")
            self.components_type_attr5_entry.help_button.configure(state="disabled")
            self.components_type_attr6_entry.help_button.configure(state="disabled")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        elif current_comp.getData("ctype") == "FixedGun":
            self.components_type_attr3_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[4])
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0,
                (
                    current_comp.getData(self.component_type_attr[6])
                    if current_comp.getData("reloading") is not False
                    else "False"
                ),
            )
            self.components_type_attr3_entry.entry.configure(
                state="readonly", validate="none"
            )
            self.components_type_attr4_label.config(text=self.component_type_attr[7])
            self.components_type_attr4_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[7])
            )
            self.components_type_attr5_label.config(text=self.component_type_attr[8])
            self.components_type_attr5_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[8])
            )
            self.components_type_attr6_label.config(text=self.component_type_attr[9])
            self.components_type_attr6_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[9])
            )
            self.components_type_attr7_label.config(text=self.component_type_attr[10])
            self.components_type_attr7_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[10])
            )
        elif current_comp.getData("ctype") == "Engine":
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[4])
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[6])
            )
            self.components_type_attr4_label.config(text=self.component_type_attr[7])
            self.components_type_attr4_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[7])
            )
            self.components_type_attr5_label.config(text=self.component_type_attr[8])
            self.components_type_attr5_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[8])
            )
            self.components_type_attr6_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr6_entry.help_button.configure(state="disabled")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        elif current_comp.getData("ctype") == "Radar":
            self.components_type_attr1_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0,
                (
                    current_comp.getData(self.component_type_attr[4])
                    if current_comp.getData("active") is not False
                    else "False"
                ),
            )
            self.components_type_attr1_entry.entry.configure(
                state="readonly", validate="none"
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[6])
            )
            self.components_type_attr4_label.config(text=self.component_type_attr[7])
            self.components_type_attr4_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[7])
            )
            self.components_type_attr5_label.config(text=self.component_type_attr[8])
            self.components_type_attr5_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[8])
            )
            self.components_type_attr6_label.config(text=self.component_type_attr[9])
            self.components_type_attr6_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[9])
            )
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        elif current_comp.getData("ctype") == "Radio":
            self.components_type_attr3_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text="max_range")
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.getData("max_range")
            )
            self.components_type_attr2_label.config(text="cur_range")
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.getData("cur_range")
            )
            self.components_type_attr3_label.config(text="message")
            self.components_type_attr3_entry.entry.insert(
                0,
                (
                    current_comp.getData("message")
                    if current_comp.getData("message") is not None
                    else "null"
                ),
            )
            self.components_type_attr3_entry.entry.configure(state="readonly")
            self.components_type_attr4_entry.entry.configure(state="readonly")
            self.components_type_attr5_entry.entry.configure(state="readonly")
            self.components_type_attr6_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr4_entry.help_button.configure(state="disabled")
            self.components_type_attr5_entry.help_button.configure(state="disabled")
            self.components_type_attr6_entry.help_button.configure(state="disabled")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        elif self.current_component_data.getData("ctype") == "Arm":
            self.components_type_attr3_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[4])
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.getData(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0,
                (
                    current_comp.getData(self.component_type_attr[6])
                    if current_comp.getData(self.component_type_attr[6]) is not None
                    else "null"
                ),
            )
            self.components_type_attr3_entry.entry.configure(state="readonly")
            self.components_type_attr4_entry.entry.configure(state="readonly")
            self.components_type_attr5_entry.entry.configure(state="readonly")
            self.components_type_attr6_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr4_entry.help_button.configure(state="disabled")
            self.components_type_attr5_entry.help_button.configure(state="disabled")
            self.components_type_attr6_entry.help_button.configure(state="disabled")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        self.components_column.update_idletasks()

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

    def show_map_entry(self, current_map):
        """
        Updates the values stored in the map entry widgets.
        """
        self.maps_id_entry.entry.delete(0, tk.END)
        self.maps_id_entry.entry.insert(0, self.select_maps_combo.get())
        self.maps_name_entry.entry.delete(0, tk.END)
        self.maps_name_entry.entry.insert(0, current_map.getData("name"))
        self.maps_edge_obj_id_entry.entry.delete(0, tk.END)
        self.maps_edge_obj_id_entry.entry.insert(
            0, self.current_map_data.getData("edge_obj_id")
        )
        self.maps_desc_entry.entry.delete(0, tk.END)
        self.maps_desc_entry.entry.insert(0, current_map.getData("desc"))
        self.maps_width_entry.entry.delete(0, tk.END)
        self.maps_width_entry.entry.insert(0, current_map.getData("width"))
        self.maps_height_entry.entry.delete(0, tk.END)
        self.maps_height_entry.entry.insert(0, current_map.getData("height"))

    def show_object_entry(self, current_obj):
        """
        Updates the values stored in the object entry widgets.
        """
        self.objects_id_entry.entry.delete(0, tk.END)
        self.objects_id_entry.entry.insert(0, current_obj.getData("id"))
        self.objects_name_entry.entry.delete(0, tk.END)
        self.objects_name_entry.entry.insert(0, current_obj.getData("name"))
        self.objects_fill_alive_entry.entry.delete(0, tk.END)
        self.objects_fill_alive_entry.entry.insert(0, current_obj.getData("fill_alive"))
        self.objects_fill_dead_entry.entry.delete(0, tk.END)
        self.objects_fill_dead_entry.entry.insert(0, current_obj.getData("fill_dead"))
        self.objects_text_entry.entry.delete(0, tk.END)
        self.objects_text_entry.entry.insert(0, current_obj.getData("text"))
        self.objects_health_entry.entry.delete(0, tk.END)
        self.objects_health_entry.entry.insert(0, current_obj.getData("health"))
        self.objects_density_entry.entry.delete(0, tk.END)
        self.objects_density_entry.entry.insert(0, current_obj.getData("density"))
        self.current_comp_ids = current_obj.getData("comp_ids")[:]
        self.objects_comp_ids_combo.combobox.set("")
        self.objects_comp_ids_combo.combobox.configure(values=self.current_comp_ids)
        if len(self.current_comp_ids) != 0:
            self.objects_comp_ids_combo.combobox.current(0)
        self.objects_comp_ids_combo.combobox.bind("<<ComboboxSelected>>", self.get_current_comp_id)
        self.objects_comp_ids_combo.combobox.bind("<Enter>", self.add_empty_comp_id)
        self.objects_comp_ids_combo.combobox.bind("<Return>", self.add_new_comp_id)
        self.objects_comp_ids_combo.combobox.bind("<KeyRelease>", self.delete_comp_id)
        self.objects_points_count_combo.combobox.configure(values=["False", "True"])
        self.objects_points_count_combo.combobox.config(state="normal")
        if bool(current_obj.getData("points_count")) is True:
            self.objects_points_count_combo.combobox.current(1)
        else:
            self.objects_points_count_combo.combobox.current(0)
        self.objects_points_count_combo.combobox.config(state="readonly")

    def add_empty_comp_id(self, event):
        """
        Adds an empty component ID for users to select to add new component ID.
        """
        if len(self.current_comp_ids) == 0:
            self.current_comp_ids.append("Add New Comp ID")
            self.objects_comp_ids_combo.combobox.configure(values=self.current_comp_ids)
        elif self.current_comp_ids[-1] != "Add New Comp ID":
            self.current_comp_ids.append("Add New Comp ID")
            self.objects_comp_ids_combo.combobox.configure(values=self.current_comp_ids)

    def get_current_comp_id(self, event):
        """
        Gets the current comp id selected for the current object.
        """
        self.current_comp_id_idx = self.objects_comp_ids_combo.combobox.current()
        self.current_comp_id = self.objects_comp_ids_combo.combobox.get()

    def delete_comp_id(self, event):
        """
        Removes the current component ID from the list.
        """
        current_comp_id = self.objects_comp_ids_combo.combobox.get()
        if len(current_comp_id) == 0:
            if self.current_comp_id_idx != len(self.current_comp_ids) - 1:
                self.current_comp_ids.pop(self.current_comp_id_idx)
                self.objects_comp_ids_combo.combobox.configure(values=self.current_comp_ids)

    def add_new_comp_id(self, event):
        """
        Adds the a new component ID to the list.
        """
        new_combo_id = self.objects_comp_ids_combo.combobox.get()
        new_combo_id_index = self.current_comp_id_idx
        if new_combo_id not in self.current_comp_ids and new_combo_id.strip() != "":
            self.current_comp_ids[new_combo_id_index] = new_combo_id
            self.objects_comp_ids_combo.combobox.configure(values=self.current_comp_ids)
            self.objects_comp_ids_combo.combobox.set(new_combo_id)

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

    def update_components_json(self):
        """
        Updates the components JSON. values
        """
        if (
            self.components_id_entry.entry.get() in self.component_data.keys()
            and self.components_id_entry.entry.get() != self.select_component_combo.get().split(":")[0]
        ):
            showwarning(
                title="Warning",
                message="The ID you are trying to use is already in use by another component. Please use another ID.",
            )
        else:
            if (
                self.components_id_entry.entry.get() != ""
                and self.components_name_entry.entry.get() != ""
                and self.components_type_attr1_entry.entry.get() != ""
            ):
                self.current_component_data.setData(
                    "id", self.components_id_entry.entry.get()
                )
                self.current_component_data.setData(
                    "name", self.components_name_entry.entry.get()
                )
                self.current_component_data.setData(
                    "ctype", self.components_type_combo.get()
                )
                if self.current_component_data.getData("ctype") == "CnC":
                    self.current_component_data.setData(
                        "max_cmds_per_tick",
                        int(self.components_type_attr1_entry.entry.get()),
                    )
                if self.current_component_data.getData("ctype") == "FixedGun":
                    self.current_component_data.setData(
                        "reload_ticks", int(self.components_type_attr1_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "reload_ticks_remaining",
                        int(self.components_type_attr2_entry.entry.get()),
                    )
                    self.current_component_data.setData(
                        "reloading",
                        (
                            self.components_type_attr3_entry.entry.get()
                            if self.components_type_attr3_entry.entry.get() != "False"
                            else False
                        ),
                    )
                    self.current_component_data.setData(
                        "ammunition", int(self.components_type_attr4_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "min_damage", int(self.components_type_attr5_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "max_damage", int(self.components_type_attr6_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "range", int(self.components_type_attr7_entry.entry.get())
                    )
                if self.current_component_data.getData("ctype") == "Engine":
                    self.current_component_data.setData(
                        "min_speed", float(self.components_type_attr1_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "max_speed", float(self.components_type_attr2_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "cur_speed", float(self.components_type_attr3_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "max_turnrate", float(self.components_type_attr4_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "cur_turnrate", float(self.components_type_attr5_entry.entry.get())
                    )
                if self.current_component_data.getData("ctype") == "Radar":
                    self.current_component_data.setData(
                        "active",
                        (
                            self.components_type_attr1_entry.entry.get()
                            if self.components_type_attr1_entry.entry.get() != "False"
                            else False
                        ),
                    )
                    self.current_component_data.setData(
                        "range", int(self.components_type_attr2_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "level", int(self.components_type_attr3_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "visarc", int(self.components_type_attr4_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "offset_angle", int(self.components_type_attr5_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "resolution", int(self.components_type_attr6_entry.entry.get())
                    )
                if self.current_component_data.getData("ctype") == "Radio":
                    self.current_component_data.setData(
                        "max_range", int(self.components_type_attr1_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "cur_range", int(self.components_type_attr2_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "message",
                        (
                            self.components_type_attr3_entry.entry.get()
                            if self.components_type_attr3_entry.entry.get() != ""
                            else None
                        ),
                    )
                if self.current_component_data.getData("ctype") == "Arm":
                    self.current_component_data.setData(
                        "max_weight", int(self.components_type_attr1_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "max_bulk", int(self.components_type_attr2_entry.entry.get())
                    )
                    self.current_component_data.setData(
                        "item",
                        (
                            self.components_type_attr3_entry.entry.get()
                            if self.components_type_attr3_entry.entry.get() != "null"
                            else None
                        ),
                    )

                with open("settings/components.json", "r") as f:
                    component_json = json.load(f)

                if (
                    self.current_component_data.getData("id")
                    != self.select_component_combo.get().split(":")[0]
                ):
                    if self.select_component_combo.get().split(":")[0] in component_json:
                        component_json.pop(self.select_component_combo.get().split(":")[0])
                    if (
                        self.select_component_combo.get().split(":")[0]
                        in self.component_data
                    ):
                        self.component_data.pop(
                            self.select_component_combo.get().split(":")[0]
                        )
                    self.component_ids.pop(self.select_component_combo.current())
                    self.component_ids.append(
                        self.current_component_data.getData("id")
                        + ": "
                        + self.current_component_data.getData("name")
                    )
                    self.select_component_combo.configure(values=self.component_ids)
                    self.select_component_combo.current(len(self.component_ids) - 1)

                component_json[self.current_component_data.getData("id")] = (
                    self.current_component_data.getSelfView()
                )
                f.close()

                self.component_data[self.current_component_data.getData("id")] = (
                    self.current_component_data
                )

                if self.select_component_combo.get().split(":")[1] != "" or (
                    self.current_component_data.getData("name")
                    != component_json[self.current_component_data.getData("id")]["name"]
                ):
                    self.component_ids.pop(self.select_component_combo.current())
                    self.component_ids.append(
                        self.current_component_data.getData("id")
                        + ": "
                        + self.current_component_data.getData("name")
                    )
                    self.select_component_combo.configure(values=self.component_ids)
                    self.select_component_combo.current(len(self.component_ids) - 1)
                if self.current_component_data.getData("name") != self.component_data[
                    self.select_component_combo.get().split(":")[0]
                ].getData("name"):
                    comp_idx = self.select_component_combo.current()
                    self.current_comp_ids[comp_idx] = ": ".join(
                        [
                            self.current_comp_ids[comp_idx].split(":")[0],
                            self.current_component_data.getData("name"),
                        ]
                    )
                    self.select_component_combo.configure(values=self.component_ids)
                    self.select_component_combo.current(len(self.component_ids) - 1)
                if (
                    "slot_id"
                    in component_json[self.current_component_data.getData("id")].keys()
                ):
                    component_json[self.current_component_data.getData("id")].pop(
                        "slot_id"
                    )
                with open("settings/components.json", "w") as f:
                    json.dump(component_json, f, indent=4)
                f.close()

    def update_objects_json(self):
        """
        Updates the objects JSON values.
        """
        if (
            self.objects_id_entry.entry.get() in self.object_data.keys()
            and self.objects_id_entry.entry.get() != self.select_objects_combo.get().split(":")[0]
        ):
            showwarning(
                title="Warning",
                message="The ID you are trying to use is already in use by another object. Please use another ID.",
            )
        else:
            if (
                self.objects_id_entry.entry.get() != ""
                and self.objects_name_entry.entry.get() != ""
                and self.objects_fill_dead_entry.entry.get() != ""
                and self.objects_fill_alive_entry.entry.get() != ""
                and self.objects_text_entry.entry.get() != ""
                and self.objects_health_entry.entry.get() != ""
                and self.objects_density_entry.entry.get() != ""
            ):
                self.current_object_data.setData("id", self.objects_id_entry.entry.get())
                self.current_object_data.setData(
                    "name", self.objects_name_entry.entry.get()
                )
                self.current_object_data.setData(
                    "fill_alive", self.objects_fill_alive_entry.entry.get()
                )
                self.current_object_data.setData(
                    "fill_dead", self.objects_fill_dead_entry.entry.get()
                )
                self.current_object_data.setData(
                    "text", self.objects_text_entry.entry.get()
                )
                self.current_object_data.setData(
                    "health", int(self.objects_health_entry.entry.get())
                )
                self.current_object_data.setData(
                    "density", int(self.objects_density_entry.entry.get())
                )
                if len(self.current_comp_ids) != 0:
                    if self.current_comp_ids[-1] == "Add New Comp ID":
                        self.current_comp_ids.pop(-1)
                self.current_object_data.setData("comp_ids", self.current_comp_ids)
                self.current_object_data.setData(
                    "points_count", bool(self.objects_points_count_combo.combobox.current())
                )

                with open("settings/objects.json", "r") as f:
                    object_json = json.load(f)

                if (
                    self.current_object_data.getData("id")
                    != self.select_objects_combo.get().split(":")[0]
                ):
                    if self.select_objects_combo.get().split(":")[0] in object_json:
                        object_json.pop(self.select_objects_combo.get().split(":")[0])
                    if self.select_objects_combo.get() in self.object_data:
                        self.object_data.pop(self.select_objects_combo.get())
                    self.object_ids.pop(self.select_objects_combo.current())
                    self.object_ids.append(
                        self.current_object_data.getData("id")
                        + ": "
                        + self.current_object_data.getData("name")
                    )
                    self.select_objects_combo.configure(values=self.object_ids)
                    self.select_objects_combo.current(len(self.object_ids) - 1)

                object_json[self.current_object_data.getData("id")] = (
                    self.current_object_data.getJSONView()
                )
                f.close()

                self.object_data[self.current_object_data.getData("id")] = (
                    self.current_object_data
                )

                if self.select_objects_combo.get().split(":")[1] != "" or (
                    self.current_object_data.getData("name")
                    != object_json[self.current_object_data.getData("id")]["name"]
                ):
                    self.object_ids.pop(self.select_objects_combo.current())
                    self.object_ids.append(
                        self.current_object_data.getData("id")
                        + ": "
                        + self.current_object_data.getData("name")
                    )
                    self.select_objects_combo.configure(values=self.object_ids)
                    self.select_objects_combo.current(len(self.object_ids) - 1)

                if self.current_object_data.getData("name") != self.object_data[
                    self.select_objects_combo.get().split(":")[0]
                ].getData("name"):
                    obj_idx = self.select_objects_combo.current()
                    self.object_ids[obj_idx] = ": ".join(
                        [
                            self.object_ids[obj_idx].split(":")[0],
                            self.current_object_data.getData("name"),
                        ]
                    )
                    self.select_objects_combo.configure(values=self.object_ids)
                    self.select_objects_combo.current(len(self.object_ids) - 1)

                with open("settings/objects.json", "w") as f:
                    json.dump(object_json, f, indent=4)
                f.close()

    def update_maps_json(self):
        """
        Updates the maps JSON values.
        """
        if (
            self.maps_id_entry.entry.get() in self.map_data.keys()
            and self.maps_id_entry.entry.get() != self.select_maps_combo.get()
        ):
            showwarning(
                title="Warning",
                message="The ID you are trying to use is already in use by another map. Please use another ID.",
            )
        else:
            if (
                self.maps_name_entry.entry.get() != ""
                and self.maps_edge_obj_id_entry.entry.get() != ""
                and self.maps_desc_entry.entry.get() != ""
                and self.maps_width_entry.entry.get != ""
                and self.maps_height_entry.entry.get() != ""
            ):
                self.current_map_data.setData("name", self.maps_name_entry.entry.get())
                self.current_map_data.setData(
                    "edge_obj_id", self.maps_edge_obj_id_entry.entry.get()
                )
                self.current_map_data.setData("desc", self.maps_desc_entry.entry.get())
                self.current_map_data.setData(
                    "width", int(self.maps_width_entry.entry.get())
                )
                self.current_map_data.setData(
                    "height", int(self.maps_height_entry.entry.get())
                )
                with open("settings/maps.json", "r") as f:
                    map_json = json.load(f)
                if self.maps_id_entry.entry.get() != self.select_maps_combo.get():
                    if self.select_maps_combo.get() in map_json:
                        map_json.pop(self.select_maps_combo.get())
                    if self.select_maps_combo.get() in self.map_data:
                        self.map_data.pop(self.select_maps_combo.get())
                    self.map_ids.pop(self.select_maps_combo.current())
                    self.map_ids.append(self.maps_id_entry.entry.get())
                    self.select_maps_combo.configure(values=self.map_ids)
                    self.select_maps_combo.current(len(self.map_ids) - 1)

                self.map_data[self.maps_id_entry.entry.get()] = self.current_map_data
                map_json[self.maps_id_entry.entry.get()] = self.current_map_data.data
                f.close()

                with open("settings/maps.json", "w") as f:
                    json.dump(map_json, f, indent=4)
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

    def create_component(self):
        """
        Creates a new component and adds it to the component dictionary.
        """
        self.component_id = askstring(
            "Component ID", "Please enter an ID for the new component."
        )
        while (
            len(self.component_id) == 0 or self.component_id in self.component_data.keys()
        ):
            if len(self.component_id) == 0:
                messagebox.showwarning(
                    "Warning", "Please enter an ID for the new component"
                )
            else:
                messagebox.showwarning(
                    "Warning", "This ID already exists, please enter a new ID."
                )
            self.component_id = askstring(
                "Component ID", "Please enter an ID for the new component."
            )
        if len(self.component_id) != 0:
            self.component_ids.append(self.component_id + ": ")
            self.select_component_combo.configure(values=self.component_ids)
            self.select_component_combo.current(len(self.component_ids) - 1)
            self.new_dict = {"id": self.component_id, "name": "", "ctype": ""}

            if self.components_type_combo.get() == "CnC":
                self.new_dict["ctype"] = "CnC"
                for key in self.cnc_keys:
                    self.new_dict[key] = ""
            elif self.components_type_combo.get() == "FixedGun":
                self.new_dict["ctype"] = "FixedGun"
                for key in self.fixed_gun_keys:
                    self.new_dict[key] = ""
                self.new_dict["reloading"] = False
            elif self.components_type_combo.get() == "Engine":
                self.new_dict["ctype"] = "Engine"
                for key in self.engine_keys:
                    self.new_dict[key] = ""
            elif self.components_type_combo.get() == "Radar":
                self.new_dict["ctype"] = "Radar"
                for key in self.radar_keys:
                    self.new_dict[key] = ""
                self.new_dict["active"] = False
            elif self.components_type_combo.get() == "Radio":
                self.new_dict["ctype"] = "Radio"
                for key in self.radio_keys:
                    self.new_dict[key] = ""
            elif self.components_type_combo.get() == "Arm":
                self.new_dict["ctype"] = "Arm"
                for key in self.arm_keys:
                    self.new_dict[key] = ""

            self.current_component_data = comp.Comp(self.new_dict)

            self.component_data[self.component_id] = self.current_component_data
            self.show_component_entries(self.current_component_data)

    def create_object(self):
        """
        Creates a new object and adds it to the object dictionary.
        """
        self.object_id = askstring("Object ID", "Please enter an ID for the new object.")
        while len(self.object_id) == 0 or self.object_id in self.object_data:
            if len(self.object_id) == 0:
                messagebox.showwarning(
                    "Warning", "Please enter an ID for the new object"
                )
            else:
                messagebox.showwarning(
                    "Warning", "This ID already exists, please enter a new ID."
                )
            self.object_id = askstring(
                "Object ID", "Please enter an ID for the new object."
            )
        if len(self.object_id) != 0:
            self.object_ids.append(self.object_id + ": ")
            self.select_objects_combo.configure(values=self.object_ids)
            self.select_objects_combo.current(len(self.object_ids) - 1)
            self.current_object_data = obj.Object(
                {
                    "id": self.object_id,
                    "name": "",
                    "fill_alive": "",
                    "fill_dead": "",
                    "text": "",
                    "health": "",
                    "density": "",
                    "comp_ids": [],
                    "points_count": "",
                }
            )
            self.object_data[self.object_id] = self.current_object_data
            self.show_object_entry(self.current_object_data)

    def create_map(self):
        """
        Creates a new map and adds it to the map dictionary.
        """
        self.map_name = askstring("Map Name", "Please enter a name for a new map.")
        while len(self.map_name) == 0 or self.map_name in self.map_data.keys():
            if len(self.map_name) == 0:
                messagebox.showwarning("Warning", "Please enter an ID for the new map")
            else:
                messagebox.showwarning(
                    "Warning", "This Name already exists, please enter a new Name."
                )
            self.map_name = askstring("Map Name", "Please enter a name for a new map.")
        if len(self.map_name) != 0:
            self.map_ids.append(self.map_name)
            self.select_maps_combo.configure(values=self.map_ids)
            self.select_maps_combo.current(len(self.map_ids) - 1)
            self.current_map_data = zmap.Map(
                {
                    "name": "",
                    "edge_obj_id": "",
                    "desc": "",
                    "width": "",
                    "height": "",
                    "placed_objects": {},
                    "placed_items": {},
                    "sides": {},
                    "win_states": [],
                }
            )
            self.map_data[self.map_name] = self.current_map_data
            self.show_map_entry(self.current_map_data)

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

    def delete_components(self):
        """
        Deletes the currently selected component from the JSON and component dictionary.
        """
        if self.select_component_combo.get().split(":")[0] in self.component_data:
            self.component_data.pop(self.select_component_combo.get().split(":")[0])

            with open("settings/components.json", "r") as f:
                component_json = json.load(f)
                component_json.pop(self.select_component_combo.get().split(":")[0])
            f.close()
            with open("settings/components.json", "w") as f:
                json.dump(component_json, f, indent=4)
            f.close()
            self.component_ids.pop(self.select_component_combo.current())
            self.select_component_combo.configure(values=self.component_ids)
            self.select_component_combo.current(len(self.component_ids) - 1)
            self.change_components_entry_widgets()

    def delete_object(self):
        """
        Deletes the currently selected object from the JSON and object dictionary.
        """
        if self.select_objects_combo.get().split(":")[0] in self.object_data:
            self.object_data.pop(self.select_objects_combo.get().split(":")[0])

            with open("settings/objects.json", "r") as f:
                object_json = json.load(f)
                object_json.pop(self.select_objects_combo.get().split(":")[0])
            f.close()
            with open("settings/objects.json", "w") as f:
                json.dump(object_json, f, indent=4)
            f.close()
            self.object_ids.pop(self.select_objects_combo.current())
            self.select_objects_combo.configure(values=self.object_ids)
            self.select_objects_combo.current(len(self.object_ids) - 1)
            self.change_objects_entry_widgets()

    def delete_map(self):
        """
        Deletes the currently selected map from the JSON and map dictionary.
        """
        if self.select_maps_combo.get() in self.map_data:
            self.map_data.pop(self.select_maps_combo.get())
            with open("settings/maps.json", "r") as f:
                map_json = json.load(f)
                map_json.pop(self.select_maps_combo.get())
            f.close()
            with open("settings/maps.json", "w") as f:
                json.dump(map_json, f, indent=4)
            f.close()
            self.map_ids.pop(self.select_maps_combo.current())
            self.select_maps_combo.configure(values=self.map_ids)
            self.select_maps_combo.current(len(self.map_ids) - 1)
            self.change_maps_entry_widgets()

    ### SHOW MAP WINDOW ###
    def show_map(self):
        """
        Shows the UI representation of the currently selected map.
        """
        self.ui_map = ui_map_config.UIMapConfig(
            self.current_map_data, self, logger=self.logger
        )

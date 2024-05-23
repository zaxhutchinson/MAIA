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


class UIComponentConfig(tk.Frame):
    def __init__(self, controller, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=BGCOLOR)
       
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
        self.components_column = uiQuietFrame(master=self.main_frame)
        self.button_row = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Component Config")
        self.validate_num = self.main_frame.register(self.validate_number_entry)

        # Place main widgets
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.button_row.pack(side=tk.BOTTOM, fill="x")

        # Make Component Widgets
        self.select_component_combo = uiComboBox(master=self.components_column)
        self.select_component_combo.configure(state="readonly")
        self.components_label = uiLabel(
            master=self.components_column, text="Components"
        )
        
        self.components_id_label = uiLabel(master=self.components_column, text="ID:")
        self.components_id_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_name_label = uiLabel(
            master=self.components_column, text="Name:"
        )
        self.components_name_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_ctype_label = uiLabel(
            master=self.components_column, text="CType:"
        )
        self.components_type_label = uiLabel(master=self.components_column, text="")
        self.components_type_combo = uiComboBox(master=self.components_column)
        self.components_type_attr1_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr1_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr2_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr2_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr3_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr3_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr4_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr4_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr5_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr5_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr6_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr6_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )
        self.components_type_attr7_label = uiLabel(
            master=self.components_column, text=""
        )
        self.components_type_attr7_entry = EntryHelp(
            master=self.components_column, text="To be added."
        )

        # Buttons
        self.components_update_button = uiButton(
            master=self.button_row,
            command=self.update_components_json,
            text="Update",
        )
        self.components_create_button = uiButton(
            master=self.button_row, command=self.create_component, text="Create"
        )
        self.components_delete_button = uiButton(
            master=self.button_row, command=self.delete_components, text="Delete"
        )
        self.home_button = uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
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


        self.components_update_button.pack(side=tk.LEFT)
        self.components_create_button.pack(side=tk.LEFT)
        self.components_delete_button.pack(side=tk.LEFT)
        self.home_button.pack(side=tk.LEFT)

        self.init_entry_widgets()

    def init_entry_widgets(self):
        """
        Gets information from the loader and assigns current values for each setting type.
        """
        

        # COMPONENT
        self.component_data = self.ldr.comp_templates
        self.component_ids = self.ldr.get_comp_ids()
        self.component_names = self.ldr.get_comp_names()
        for i in range(len(self.component_ids)):
            self.component_ids[i] = (
                self.component_ids[i] + ": " + self.component_names[i]
            )
        self.component_types = self.ldr.get_comp_types()
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

        

    def get_previous_component_combo(self, event):
        self.prev_component_combo = self.select_component_combo.current()

    

    def change_components_entry_widgets(self, event=None):
        """
        Gets the correct component data for the currently selected team.
        """
        self.answer = True

        if self.current_component_data.get_data("ctype") == "CnC":
            ctype_attributes = self.cnc_keys
        elif self.current_component_data.get_data("ctype") == "FixedGun":
            ctype_attributes = self.fixed_gun_keys
        elif self.current_component_data.get_data("ctype") == "Engine":
            ctype_attributes = self.engine_keys
        elif self.current_component_data.get_data("ctype") == "Radar":
            ctype_attributes = self.radar_keys
        elif self.current_component_data.get_data("ctype") == "Radio":
            ctype_attributes = self.radio_keys
        elif self.current_component_data.get_data("ctype") == "Arm":
            ctype_attributes = self.arm_keys

        if not (
            (
                (
                    self.components_id_entry.entry.get()
                    == self.current_component_data.get_data("id")
                )
                and (
                    self.components_name_entry.entry.get()
                    == self.current_component_data.get_data("name")
                )
                and (
                    self.components_type_combo.get()
                    == self.current_component_data.get_data("ctype")
                )
                and (
                    self.components_type_attr1_entry.entry.get()
                    == str(self.current_component_data.get_data(ctype_attributes[0]))
                )
                and (
                    (len(ctype_attributes) < 2)
                    or (
                        self.components_type_attr2_entry.entry.get()
                        == str(
                            self.current_component_data.get_data(ctype_attributes[1])
                        )
                    )
                )
                and (
                    (len(ctype_attributes) < 3)
                    or self.current_component_data.get_data(ctype_attributes[2]) is None
                    or (
                        self.components_type_attr3_entry.entry.get()
                        == str(
                            self.current_component_data.get_data(ctype_attributes[2])
                        )
                    )
                )
                and (
                    (len(ctype_attributes) < 4)
                    or (
                        self.components_type_attr4_entry.entry.get()
                        == str(
                            self.current_component_data.get_data(ctype_attributes[3])
                        )
                    )
                )
                and (
                    (len(ctype_attributes) < 5)
                    or (
                        self.components_type_attr5_entry.entry.get()
                        == str(
                            self.current_component_data.get_data(ctype_attributes[4])
                        )
                    )
                )
                and (
                    (len(ctype_attributes) < 6)
                    or (
                        self.components_type_attr6_entry.entry.get()
                        == str(
                            self.current_component_data.get_data(ctype_attributes[5])
                        )
                    )
                )
                and (
                    (len(ctype_attributes) < 7)
                    or (
                        self.components_type_attr7_entry.entry.get()
                        == str(
                            self.current_component_data.get_data(ctype_attributes[6])
                        )
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

    

    def show_component_entries(self, current_comp):
        """
        Updates the values in the component entry widgets.
        """
        self.component_type_attr = current_comp.view_keys
        self.components_id_entry.entry.delete(0, tk.END)
        self.components_id_entry.entry.insert(0, current_comp.get_data("id"))
        self.components_name_entry.entry.delete(0, tk.END)
        self.components_name_entry.entry.insert(
            0,
            current_comp.get_data("name"),
        )
        self.components_type_combo.configure(values=self.component_types)
        self.components_type_combo.set(current_comp.get_data("ctype"))
        self.components_type_label.config(text=current_comp.get_data("ctype"))
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

        if current_comp.get_data("ctype") == "CnC":
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[4])
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
        elif current_comp.get_data("ctype") == "FixedGun":
            self.components_type_attr3_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[4])
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0,
                (
                    current_comp.get_data(self.component_type_attr[6])
                    if current_comp.get_data("reloading") is not False
                    else "False"
                ),
            )
            self.components_type_attr3_entry.entry.configure(
                state="readonly", validate="none"
            )
            self.components_type_attr4_label.config(text=self.component_type_attr[7])
            self.components_type_attr4_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[7])
            )
            self.components_type_attr5_label.config(text=self.component_type_attr[8])
            self.components_type_attr5_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[8])
            )
            self.components_type_attr6_label.config(text=self.component_type_attr[9])
            self.components_type_attr6_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[9])
            )
            self.components_type_attr7_label.config(text=self.component_type_attr[10])
            self.components_type_attr7_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[10])
            )
        elif current_comp.get_data("ctype") == "Engine":
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[4])
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[6])
            )
            self.components_type_attr4_label.config(text=self.component_type_attr[7])
            self.components_type_attr4_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[7])
            )
            self.components_type_attr5_label.config(text=self.component_type_attr[8])
            self.components_type_attr5_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[8])
            )
            self.components_type_attr6_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr6_entry.help_button.configure(state="disabled")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        elif current_comp.get_data("ctype") == "Radar":
            self.components_type_attr1_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0,
                (
                    current_comp.get_data(self.component_type_attr[4])
                    if current_comp.get_data("active") is not False
                    else "False"
                ),
            )
            self.components_type_attr1_entry.entry.configure(
                state="readonly", validate="none"
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[6])
            )
            self.components_type_attr4_label.config(text=self.component_type_attr[7])
            self.components_type_attr4_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[7])
            )
            self.components_type_attr5_label.config(text=self.component_type_attr[8])
            self.components_type_attr5_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[8])
            )
            self.components_type_attr6_label.config(text=self.component_type_attr[9])
            self.components_type_attr6_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[9])
            )
            self.components_type_attr7_entry.entry.configure(state="readonly")
            self.components_type_attr7_entry.help_button.configure(state="disabled")
        elif current_comp.get_data("ctype") == "Radio":
            self.components_type_attr3_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text="max_range")
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.get_data("max_range")
            )
            self.components_type_attr2_label.config(text="cur_range")
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.get_data("cur_range")
            )
            self.components_type_attr3_label.config(text="message")
            self.components_type_attr3_entry.entry.insert(
                0,
                (
                    current_comp.get_data("message")
                    if current_comp.get_data("message") is not None
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
        elif self.current_component_data.get_data("ctype") == "Arm":
            self.components_type_attr3_entry.entry.configure(validate="none")
            self.components_type_attr1_label.config(text=self.component_type_attr[4])
            self.components_type_attr1_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[4])
            )
            self.components_type_attr2_label.config(text=self.component_type_attr[5])
            self.components_type_attr2_entry.entry.insert(
                0, current_comp.get_data(self.component_type_attr[5])
            )
            self.components_type_attr3_label.config(text=self.component_type_attr[6])
            self.components_type_attr3_entry.entry.insert(
                0,
                (
                    current_comp.get_data(self.component_type_attr[6])
                    if current_comp.get_data(self.component_type_attr[6]) is not None
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

    

    def update_components_json(self):
        """
        Updates the components JSON. values
        """
        if (
            self.components_id_entry.entry.get() in self.component_data.keys()
            and self.components_id_entry.entry.get()
            != self.select_component_combo.get().split(":")[0]
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
                if self.current_component_data.get_data("ctype") == "CnC":
                    self.current_component_data.setData(
                        "max_cmds_per_tick",
                        int(self.components_type_attr1_entry.entry.get()),
                    )
                if self.current_component_data.get_data("ctype") == "FixedGun":
                    self.current_component_data.setData(
                        "reload_ticks",
                        int(self.components_type_attr1_entry.entry.get()),
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
                if self.current_component_data.get_data("ctype") == "Engine":
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
                        "max_turnrate",
                        float(self.components_type_attr4_entry.entry.get()),
                    )
                    self.current_component_data.setData(
                        "cur_turnrate",
                        float(self.components_type_attr5_entry.entry.get()),
                    )
                if self.current_component_data.get_data("ctype") == "Radar":
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
                        "offset_angle",
                        int(self.components_type_attr5_entry.entry.get()),
                    )
                    self.current_component_data.setData(
                        "resolution", int(self.components_type_attr6_entry.entry.get())
                    )
                if self.current_component_data.get_data("ctype") == "Radio":
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
                if self.current_component_data.get_data("ctype") == "Arm":
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
                    self.current_component_data.get_data("id")
                    != self.select_component_combo.get().split(":")[0]
                ):
                    if (
                        self.select_component_combo.get().split(":")[0]
                        in component_json
                    ):
                        component_json.pop(
                            self.select_component_combo.get().split(":")[0]
                        )
                    if (
                        self.select_component_combo.get().split(":")[0]
                        in self.component_data
                    ):
                        self.component_data.pop(
                            self.select_component_combo.get().split(":")[0]
                        )
                    self.component_ids.pop(self.select_component_combo.current())
                    self.component_ids.append(
                        self.current_component_data.get_data("id")
                        + ": "
                        + self.current_component_data.get_data("name")
                    )
                    self.select_component_combo.configure(values=self.component_ids)
                    self.select_component_combo.current(len(self.component_ids) - 1)

                component_json[self.current_component_data.get_data("id")] = (
                    self.current_component_data.getSelfView()
                )
                f.close()

                self.component_data[self.current_component_data.get_data("id")] = (
                    self.current_component_data
                )

                if self.select_component_combo.get().split(":")[1] != "" or (
                    self.current_component_data.get_data("name")
                    != component_json[self.current_component_data.get_data("id")][
                        "name"
                    ]
                ):
                    self.component_ids.pop(self.select_component_combo.current())
                    self.component_ids.append(
                        self.current_component_data.get_data("id")
                        + ": "
                        + self.current_component_data.get_data("name")
                    )
                    self.select_component_combo.configure(values=self.component_ids)
                    self.select_component_combo.current(len(self.component_ids) - 1)
                if self.current_component_data.get_data("name") != self.component_data[
                    self.select_component_combo.get().split(":")[0]
                ].get_data("name"):
                    comp_idx = self.select_component_combo.current()
                    self.current_comp_ids[comp_idx] = ": ".join(
                        [
                            self.current_comp_ids[comp_idx].split(":")[0],
                            self.current_component_data.get_data("name"),
                        ]
                    )
                    self.select_component_combo.configure(values=self.component_ids)
                    self.select_component_combo.current(len(self.component_ids) - 1)
                if (
                    "slot_id"
                    in component_json[self.current_component_data.get_data("id")].keys()
                ):
                    component_json[self.current_component_data.get_data("id")].pop(
                        "slot_id"
                    )
                with open("settings/components.json", "w") as f:
                    json.dump(component_json, f, indent=4)
                f.close()

    

    def create_component(self):
        """
        Creates a new component and adds it to the component dictionary.
        """
        self.component_id = askstring(
            "Component ID", "Please enter an ID for the new component."
        )
        while (
            len(self.component_id) == 0
            or self.component_id in self.component_data.keys()
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

    def goto_home(self):
        self.controller.show_frame("home_page")

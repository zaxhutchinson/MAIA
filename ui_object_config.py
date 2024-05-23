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


class UIObjectConfig(tk.Frame):
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
        self.objects_id_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
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
        self.objects_density_label = uiLabel(
            master=self.objects_column, text="Density:"
        )
        self.objects_density_entry = EntryHelp(
            master=self.objects_column, text="To be added."
        )
        self.objects_density_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.objects_comp_ids_label = uiLabel(
            master=self.objects_column, text="Comp IDs:"
        )
        self.objects_comp_ids_combo = ComboBoxHelp(
            master=self.objects_column, text="To be Added."
        )
        self.objects_points_count_label = uiLabel(
            master=self.objects_column, text="Points Count:"
        )
        self.objects_points_count_combo = ComboBoxHelp(
            master=self.objects_column, text="To be Added."
        )

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

        

        self.init_entry_widgets()

    def init_entry_widgets(self):
        """
        Gets information from the loader and assigns current values for each setting type.
        """
        

        # OBJECT
        self.object_data = self.ldr.obj_templates
        self.object_ids = self.ldr.get_obj_ids()
        self.current_object_data = self.object_data[self.object_ids[0]]
        self.object_names = self.ldr.get_obj_names()
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

        

    def get_previous_object_combo(self, event):
        self.prev_object_combo = self.select_objects_combo.current()

    

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
                    == self.current_object_data.get_data("id")
                )
                and (
                    self.objects_name_entry.entry.get()
                    == self.current_object_data.get_data("name")
                )
                and (
                    self.objects_fill_alive_entry.entry.get()
                    == self.current_object_data.get_data("fill_alive")
                )
                and (
                    self.objects_fill_dead_entry.entry.get()
                    == self.current_object_data.get_data("fill_dead")
                )
                and (
                    self.objects_text_entry.entry.get()
                    == self.current_object_data.get_data("text")
                )
                and (
                    self.objects_health_entry.entry.get()
                    == str(self.current_object_data.get_data("health"))
                )
                and (
                    self.objects_density_entry.entry.get()
                    == str(self.current_object_data.get_data("density"))
                )
                and (comp_ids == self.current_object_data.get_data("comp_ids"))
                and (
                    bool(self.objects_points_count_combo.combobox.current())
                    == self.current_object_data.get_data("points_count")
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

    

    def show_object_entry(self, current_obj):
        """
        Updates the values stored in the object entry widgets.
        """
        self.objects_id_entry.entry.delete(0, tk.END)
        self.objects_id_entry.entry.insert(0, current_obj.get_data("id"))
        self.objects_name_entry.entry.delete(0, tk.END)
        self.objects_name_entry.entry.insert(0, current_obj.get_data("name"))
        self.objects_fill_alive_entry.entry.delete(0, tk.END)
        self.objects_fill_alive_entry.entry.insert(
            0, current_obj.get_data("fill_alive")
        )
        self.objects_fill_dead_entry.entry.delete(0, tk.END)
        self.objects_fill_dead_entry.entry.insert(0, current_obj.get_data("fill_dead"))
        self.objects_text_entry.entry.delete(0, tk.END)
        self.objects_text_entry.entry.insert(0, current_obj.get_data("text"))
        self.objects_health_entry.entry.delete(0, tk.END)
        self.objects_health_entry.entry.insert(0, current_obj.get_data("health"))
        self.objects_density_entry.entry.delete(0, tk.END)
        self.objects_density_entry.entry.insert(0, current_obj.get_data("density"))
        self.current_comp_ids = current_obj.get_data("comp_ids")[:]
        self.objects_comp_ids_combo.combobox.set("")
        self.objects_comp_ids_combo.combobox.configure(values=self.current_comp_ids)
        if len(self.current_comp_ids) != 0:
            self.objects_comp_ids_combo.combobox.current(0)
        self.objects_comp_ids_combo.combobox.bind(
            "<<ComboboxSelected>>", self.get_current_comp_id
        )
        self.objects_comp_ids_combo.combobox.bind("<Enter>", self.add_empty_comp_id)
        self.objects_comp_ids_combo.combobox.bind("<Return>", self.add_new_comp_id)
        self.objects_comp_ids_combo.combobox.bind("<KeyRelease>", self.delete_comp_id)
        self.objects_points_count_combo.combobox.configure(values=["False", "True"])
        self.objects_points_count_combo.combobox.config(state="normal")
        if bool(current_obj.get_data("points_count")) is True:
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
                self.objects_comp_ids_combo.combobox.configure(
                    values=self.current_comp_ids
                )

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

    

    def update_objects_json(self):
        """
        Updates the objects JSON values.
        """
        if (
            self.objects_id_entry.entry.get() in self.object_data.keys()
            and self.objects_id_entry.entry.get()
            != self.select_objects_combo.get().split(":")[0]
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
                self.current_object_data.setData(
                    "id", self.objects_id_entry.entry.get()
                )
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
                    "points_count",
                    bool(self.objects_points_count_combo.combobox.current()),
                )

                with open("settings/objects.json", "r") as f:
                    object_json = json.load(f)

                if (
                    self.current_object_data.get_data("id")
                    != self.select_objects_combo.get().split(":")[0]
                ):
                    if self.select_objects_combo.get().split(":")[0] in object_json:
                        object_json.pop(self.select_objects_combo.get().split(":")[0])
                    if self.select_objects_combo.get() in self.object_data:
                        self.object_data.pop(self.select_objects_combo.get())
                    self.object_ids.pop(self.select_objects_combo.current())
                    self.object_ids.append(
                        self.current_object_data.get_data("id")
                        + ": "
                        + self.current_object_data.get_data("name")
                    )
                    self.select_objects_combo.configure(values=self.object_ids)
                    self.select_objects_combo.current(len(self.object_ids) - 1)

                object_json[self.current_object_data.get_data("id")] = (
                    self.current_object_data.getJSONView()
                )
                f.close()

                self.object_data[self.current_object_data.get_data("id")] = (
                    self.current_object_data
                )

                if self.select_objects_combo.get().split(":")[1] != "" or (
                    self.current_object_data.get_data("name")
                    != object_json[self.current_object_data.get_data("id")]["name"]
                ):
                    self.object_ids.pop(self.select_objects_combo.current())
                    self.object_ids.append(
                        self.current_object_data.get_data("id")
                        + ": "
                        + self.current_object_data.get_data("name")
                    )
                    self.select_objects_combo.configure(values=self.object_ids)
                    self.select_objects_combo.current(len(self.object_ids) - 1)

                if self.current_object_data.get_data("name") != self.object_data[
                    self.select_objects_combo.get().split(":")[0]
                ].get_data("name"):
                    obj_idx = self.select_objects_combo.current()
                    self.object_ids[obj_idx] = ": ".join(
                        [
                            self.object_ids[obj_idx].split(":")[0],
                            self.current_object_data.get_data("name"),
                        ]
                    )
                    self.select_objects_combo.configure(values=self.object_ids)
                    self.select_objects_combo.current(len(self.object_ids) - 1)

                with open("settings/objects.json", "w") as f:
                    json.dump(object_json, f, indent=4)
                f.close()

    

    def create_object(self):
        """
        Creates a new object and adds it to the object dictionary.
        """
        self.object_id = askstring(
            "Object ID", "Please enter an ID for the new object."
        )
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

    
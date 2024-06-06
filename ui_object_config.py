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
import zfunctions
from tkinter.messagebox import askyesno
from tkinter.messagebox import showwarning
from tkinter.simpledialog import askstring

import ui_map_config
from ui_widgets import *


class UIObjectConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=BGCOLOR)
        self.logger = logger
        self.ldr = ldr
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
        # Make frames

        self.main_frame = uiQuietFrame(master=self)
        self.obj_selection_frame = uiQuietFrame(master=self.main_frame)
        self.obj_info_frame = uiQuietFrame(master=self.main_frame)
        self.obj_comp_frame = uiQuietFrame(master=self.main_frame)
        self.comp_selection_frame = uiQuietFrame(master=self.main_frame)
        self.button_row = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Object Configuration")
        self.validate_num = self.main_frame.register(self.validate_number_entry)

        # Place frames
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.obj_selection_frame.pack(side=tk.LEFT, fill="y")
        self.obj_info_frame.pack(side=tk.LEFT, fill="y")
        self.obj_info_frame.columnconfigure(0,weight=1)
        self.obj_info_frame.columnconfigure(1,weight=1)
        self.obj_comp_frame.pack(side=tk.LEFT, fill="y")
        self.obj_comp_frame.rowconfigure(1,weight=1)
        # self.obj_info_frame.rowconfigure(11,weight=1)
        self.comp_selection_frame.pack(side=tk.LEFT, fill="y")
        self.comp_selection_frame.rowconfigure(1,weight=1)

        # Make widgets
        self.select_obj_listbox_var = tk.StringVar()
        self.select_obj_listbox = uiListBox(
            master=self.obj_selection_frame,
            listvariable=self.select_obj_listbox_var,
            selectmode='browse'
        )
        self.select_obj_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.select_obj_listbox.bind(
            "<<ListboxSelect>>", self.show_object
        )

        # Make Object Widgets
        self.obj_id_label = uiLabel(master=self.obj_info_frame, text="ID")
        self.obj_id_entry = EntryHelp(master=self.obj_info_frame, text="An object's unique ID.")
        self.obj_name_label = uiLabel(master=self.obj_info_frame, text="Name")
        self.obj_name_entry = EntryHelp(master=self.obj_info_frame, text="An object's name. Names do not have to be unique.")
        self.obj_health_label = uiLabel(master=self.obj_info_frame, text="Health")
        self.obj_health_entry = EntryHelp(master=self.obj_info_frame, text="An integer value giving the maximum/starting health of the object.")
        self.obj_density_label = uiLabel(master=self.obj_info_frame, text="Density")
        self.obj_density_entry = EntryHelp(master=self.obj_info_frame, text="An object's density determines how well radar scans penetrate and pass through the object. A high density object will stop radar scans of lower or equal value, preventing the scan from detecting objects on the other side.")
        self.obj_points_label = uiLabel(master=self.obj_info_frame, text="Points")
        self.obj_points_entry = EntryHelp(master=self.obj_info_frame, text="Point value associated with the destruction of the object.")
        self.obj_char_label = uiLabel(master=self.obj_info_frame, text="Display Char")
        self.obj_char_entry = EntryHelp(master=self.obj_info_frame, text="A single character used to display the object on the map when a sprite is not available.")
        self.obj_char_color_alive_label = uiLabel(master=self.obj_info_frame, text="Alive Color")
        self.obj_char_color_alive_entry = EntryHelp(master=self.obj_info_frame, text="The color used to display the object's character when the object is alive.")
        self.obj_char_color_dead_label = uiLabel(master=self.obj_info_frame, text="Dead Color")
        self.obj_char_color_dead_entry = EntryHelp(master=self.obj_info_frame, text="The color used to display the object's character when the object is dead.")
        self.obj_sprite_alive_name_label = uiLabel(master=self.obj_info_frame, text="Alive Sprite")
        self.obj_sprite_alive_name_entry = EntryHelp(master=self.obj_info_frame, text="The filename of the sprite used to display the object when it is alive.")
        self.obj_sprite_dead_name_label = uiLabel(master=self.obj_info_frame, text="Dead Sprite")
        self.obj_sprite_dead_name_entry = EntryHelp(master=self.obj_info_frame, text="The filename of the sprite used to display the object when it is dead.")

        # Place obj widgets
        self.obj_id_label.grid(row=0, column=0, sticky="ew")
        self.obj_id_entry.frame.grid(row=0, column=1, sticky="ew")
        self.obj_name_label.grid(row=1, column=0, sticky="ew")
        self.obj_name_entry.frame.grid(row=1, column=1, sticky="ew")
        self.obj_health_label.grid(row=2, column=0, sticky="ew")
        self.obj_health_entry.frame.grid(row=2, column=1, sticky="ew")
        self.obj_density_label.grid(row=3, column=0, sticky="ew")
        self.obj_density_entry.frame.grid(row=3, column=1, sticky="ew")
        self.obj_points_label.grid(row=4, column=0, sticky="ew")
        self.obj_points_entry.frame.grid(row=4, column=1, sticky="ew")
        self.obj_char_label.grid(row=5, column=0, sticky="ew")
        self.obj_char_entry.frame.grid(row=5, column=1, sticky="ew")
        self.obj_char_color_alive_label.grid(row=6, column=0, sticky="ew")
        self.obj_char_color_alive_entry.frame.grid(row=6, column=1, sticky="ew")
        self.obj_char_color_dead_label.grid(row=7, column=0, sticky="ew")
        self.obj_char_color_dead_entry.frame.grid(row=7, column=1, sticky="ew")
        self.obj_sprite_alive_name_label.grid(row=8, column=0, sticky="ew")
        self.obj_sprite_alive_name_entry.frame.grid(row=8, column=1, sticky="ew")
        self.obj_sprite_dead_name_label.grid(row=9, column=0, sticky="ew")
        self.obj_sprite_dead_name_entry.frame.grid(row=9, column=1, sticky="ew")
        
        self.obj_comp_remove_label = uiLabel(master=self.obj_comp_frame, text="Object's Components")
        self.obj_comp_remove_listbox_var = tk.StringVar()
        self.obj_comp_remove_listbox = uiListBox(
            master=self.obj_comp_frame,
            listvariable=self.obj_comp_remove_listbox_var,
            selectmode='multiple',
            width=32
        )
        self.obj_comp_remove_button = uiButton(master=self.obj_comp_frame, command=self.remove_comps, text="Remove Component")
        self.obj_comp_remove_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.obj_comp_remove_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.obj_comp_remove_button.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.obj_comp_add_label = uiLabel(master=self.comp_selection_frame, text="All Components")
        self.obj_comp_add_listbox_var = tk.StringVar()
        self.obj_comp_add_listbox = uiListBox(
            master=self.comp_selection_frame,
            listvariable=self.obj_comp_add_listbox_var,
            selectmode='multiple',
            width=32
        )
        self.obj_comp_add_button = uiButton(master=self.comp_selection_frame, command=self.add_comps, text="Add Component(s)")
        self.obj_comp_add_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.obj_comp_add_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.obj_comp_add_button.grid(row=2, column=0, columnspan=2, sticky="ew")


        # Main Buttons
        self.obj_create_button = uiButton(
            master=self.button_row,
            command=self.create_obj,
            text="Add Object"
        )
        self.obj_create_button.pack(side=tk.LEFT)
        self.obj_update_button = uiButton(
            master=self.button_row,
            command=self.update_obj,
            text="Update Object"
        )
        self.obj_update_button.pack(side=tk.LEFT)
        self.obj_delete_button = uiCarefulButton(
            master=self.button_row,
            command=self.delete_obj,
            text="Delete Object"
        )
        self.obj_delete_button.pack(side=tk.LEFT)

        self.home_button = uiButton(
            master=self.button_row,
            command=self.goto_home,
            text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiCarefulButton(
            master=self.button_row,
            command=self.save_to_json,
            text="Save Objs to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

        self.populate_obj_listbox()

    def populate_obj_listbox(self):

        self.clear_all_fields()
        obj_data = self.ldr.get_obj_templates()
        entries = []
        for obj in obj_data.values():
            entry = f"{obj["id"]}:{obj["name"]}"
            entries.append(entry)
        entries = sorted(entries)
        self.select_obj_listbox.delete(0,tk.END)
        self.select_obj_listbox_var.set(entries)



    def clear_all_fields(self):
        "Clears all the object info fields."
        self.obj_id_entry.entry.delete(0, tk.END)
        self.obj_name_entry.entry.delete(0, tk.END)
        self.obj_health_entry.entry.delete(0, tk.END)
        self.obj_density_entry.entry.delete(0, tk.END)
        self.obj_points_entry.entry.delete(0, tk.END)
        self.obj_char_entry.entry.delete(0, tk.END)
        self.obj_char_color_alive_entry.entry.delete(0, tk.END)
        self.obj_char_color_dead_entry.entry.delete(0, tk.END)
        self.obj_sprite_alive_name_entry.entry.delete(0, tk.END)
        self.obj_sprite_dead_name_entry.entry.delete(0, tk.END)
        self.obj_comp_remove_listbox.delete(0, tk.END)
        self.obj_comp_add_listbox.delete(0, tk.END)

    def select_obj_with_id(self, _id):
        for index, entry in enumerate(self.select_obj_listbox.get(0,tk.END)):
            obj_id, obj_name = entry.split(":")
            if _id == obj_id:
                self.select_obj_listbox.selection_clear(0, tk.END)
                self.select_obj_listbox.selection_set(index)
                self.select_obj_listbox.activate(index)
                self.show_object()
                break

    def show_object(self, event=None):
        selected_obj = self.get_currently_selected_obj()
        if selected_obj != None:
            self.clear_all_fields()
            self.obj_id_entry.entry.insert(0, selected_obj["id"])
            self.obj_name_entry.entry.insert(0, selected_obj["name"])
            self.obj_health_entry.entry.insert(0, selected_obj["health"])
            self.obj_density_entry.entry.insert(0, selected_obj["density"])
            self.obj_points_entry.entry.insert(0, selected_obj["points"])
            self.obj_char_entry.entry.insert(0, selected_obj["character"])
            self.obj_char_color_alive_entry.entry.insert(0, selected_obj["color_alive"])
            self.obj_char_color_dead_entry.entry.insert(0, selected_obj["color_dead"])
            self.obj_sprite_alive_name_entry.entry.insert(0, selected_obj["alive_sprite_filename"])
            self.obj_sprite_dead_name_entry.entry.insert(0, selected_obj["dead_sprite_filename"])
            self.show_obj_comps(selected_obj)
            self.show_all_comps()

    def show_obj_comps(self, obj):
        comp_data = self.ldr.get_comp_templates()
        comp_entries = []
        for cid in obj["comp_ids"]:
            comp = comp_data[cid]
            entry = f"{comp["id"]}:{comp["name"]}"
            comp_entries.append(entry)
        comp_entries = sorted(comp_entries)
        self.obj_comp_remove_listbox_var.set(comp_entries)
    
    def show_all_comps(self):
        comp_data = self.ldr.get_comp_templates()
        entries = []
        for comp in comp_data.values():
            entry = f"{comp["id"]}:{comp["name"]}"
            entries.append(entry)
        entries = sorted(entries)
        self.obj_comp_add_listbox_var.set(entries)

    def create_obj(self):
        
        obj_data = self.ldr.get_obj_templates()
        good = False
        while not good:
            obj_id = askstring("Unique Object ID", "Please enter an unique ID for the new object.")
            if len(obj_id) == 0:
                messagebox.showwarning(
                    "Warning", "You must enter a non-empty object ID to continue"
                )
            elif obj_id in obj_data.keys():
                messagebox.showwarning(
                    "Warning", f"Object ID {obj_id} already exists, please enter a new ID."
                )
            else:
                good = True

        new_obj = {
            "id":obj_id,
            "name":"None",
            "color_alive":"green",
            "color_dead":"red",
            "character":"O",
            "health":0,
            "density":0,
            "comp_ids":[],
            "points":0,
            "alive_sprite_filename":"",
            "dead_sprite_filename":""
        }
        obj_data.update({obj_id: new_obj})

        # Repopulate the listbox of objects
        self.populate_obj_listbox()

        # Select the new object so it can be displayed for the user.
        self.select_obj_with_id(obj_id)


    def update_obj(self):
        
        obj_data = self.ldr.get_obj_templates()
        current_obj = self.get_currently_selected_obj()

        new_id = self.obj_id_entry.entry.get()
        new_name = self.obj_name_entry.entry.get()
        new_health = self.obj_health_entry.entry.get()
        new_density = self.obj_density_entry.entry.get()
        new_points = self.obj_points_entry.entry.get()
        new_char = self.obj_char_entry.entry.get()
        new_alive_color = self.obj_char_color_alive_entry.entry.get()
        new_dead_color = self.obj_char_color_dead_entry.entry.get()
        new_alive_sprite = self.obj_sprite_alive_name_entry.entry.get()
        new_dead_sprite = self.obj_sprite_dead_name_entry.entry.get()
        
        if new_id != current_obj["id"]:
            if new_id in obj_data.keys():
                showwarning(
                    title="Warning",
                    message=f"ID {new_id} is in use by another object. Please use another ID.",
                )
            else:
                old_id = current_obj["id"]
                current_obj["id"] = new_id
                del obj_data[old_id]
                obj_data[new_id] = current_obj

        warnings = ""

        if len(new_name) > 0:
            current_obj["name"] = new_name
        else:
            warnings += f"WARNING: Name field cannot be empty.\n"

        if len(new_health) > 0 and zfunctions.is_int(new_health):
            current_obj["health"] = new_health
        else:
            warnings += f"WARNING: Health field must be an integer.\n"

        if len(new_density) > 0 and zfunctions.is_int(new_density):
            current_obj["density"] = new_density
        else:
            warnings += f"WARNING: Density field must be an integer.\n"
    
        if len(new_points) > 0 and zfunctions.is_int(new_points):
            current_obj["points"] = new_points
        else:
            warnings += f"WARNING: Points field must be an integer.\n"

        if len(new_char) == 1:
            current_obj["character"] = new_char
        else:
            warnings += f"WARNING: Character must be a single character.\n"
        
        # TODO: Some color and filename validation. Maybe.
        current_obj["color_alive"] = new_alive_color
        current_obj["color_dead"] = new_dead_color
        current_obj["alive_sprite_filename"] = new_alive_sprite
        current_obj["dead_sprite_filename"] = new_dead_sprite

        if len(warnings) > 0:
            showwarning(
                title="Warning",
                message=warnings
            )

        self.populate_obj_listbox()

        self.select_obj_with_id(new_id)
        self.show_object()

    def delete_obj(self):
        """
        Deleted the selected object from the Loader's object templates dictionary.
        """
        obj_data = self.ldr.get_obj_templates()
        current_obj = self.get_currently_selected_obj()
        if current_obj != None:
            del obj_data[current_obj["id"]]
            self.populate_obj_listbox()

    def add_comps(self):
        obj_data = self.ldr.get_obj_templates()
        current_obj = self.get_currently_selected_obj()
        comps_to_add = self.get_comps_to_add()
        for comp_id in comps_to_add:
            current_obj["comp_ids"].append(comp_id)
        self.show_object()
        # self.obj_comp_add_listbox.selection_clear(0,tk.END)
    def remove_comps(self):
        obj_data = self.ldr.get_obj_templates()
        current_obj = self.get_currently_selected_obj()
        comps_to_remove = self.get_comps_to_remove()
        for comp_id in comps_to_remove:
            current_obj["comp_ids"].remove(comp_id)
        self.show_object()

    def goto_home(self):
        self.controller.show_frame("home_page")
    def save_to_json(self):
        self.ldr.save_obj_templates()


    def get_currently_selected_obj(self):
        obj_index = self.select_obj_listbox.curselection()
        if len(obj_index) == 1:
            obj_entry = self.select_obj_listbox.get(obj_index[0])
            obj_id, obj_name = obj_entry.split(":")
            return self.ldr.get_obj_template(obj_id)
        else:
            return None

    def get_comps_to_add(self):
        comp_indexes = self.obj_comp_add_listbox.curselection()
        comp_ids_to_add = []
        if len(comp_indexes) > 0:
            for index in comp_indexes:
                comp_entry = self.obj_comp_add_listbox.get(index)
                comp_id, comp_name = comp_entry.split(":")
                comp_ids_to_add.append(comp_id)
            return comp_ids_to_add
        else:
            return []


    def get_comps_to_remove(self):
        comp_indexes = self.obj_comp_remove_listbox.curselection()
        comp_ids_to_remove = []
        if len(comp_indexes) > 0:
            for index in comp_indexes:
                comp_entry = self.obj_comp_remove_listbox.get(index)
                comp_id, comp_name = comp_entry.split(":")
                comp_ids_to_remove.append(comp_id)
            return comp_ids_to_remove
        else:
            return []

    def init_entry_widgets(self):
        """
        Gets information from the loader and assigns current values for each setting type.
        """
        

        # OBJECT
        obj_data = self.ldr.get_obj_templates()
        
        # for obj in obj_data:
            

        # self.current_object_data = self.object_data[self.object_ids[0]]
        # self.object_names = self.ldr.get_obj_names()
        # for i in range(len(self.object_ids)):
        #     self.object_ids[i] = self.object_ids[i] + ": " + self.object_names[i]
        # self.current_object_data = self.object_data[self.object_ids[0].split(":")[0]]
        # self.select_objects_combo.configure(values=self.object_ids)
        # self.select_objects_combo.current(0)
        self.select_objects_combo.bind(
            "<<ComboboxSelected>>", self.change_objects_entry_widgets
        )
        self.select_objects_combo.bind("<Enter>", self.get_previous_object_combo)

        # self.show_object_entry(self.current_object_data)

        

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

    
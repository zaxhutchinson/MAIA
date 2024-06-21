import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging
import loader
import json
import gstate
import obj
import zmap
from tkinter.messagebox import askyesno
from tkinter.messagebox import showwarning
from tkinter.simpledialog import askstring

import ui_map_config
from ui_widgets import *

class UINewGoal():
    def __init__(self):

        self.gstate_id_svar = tk.StringVar()
        self.gstate_type_svar = tk.StringVar()

        self.top = tk.Toplevel() # use Toplevel() instead of Tk()
        
        self.label = uiLabel(master=self.top, text='Provide a unique ID and type for the new gstate.')
        self.label.grid(row=0, column=0,columnspan=2)

        self.id_label = uiLabel(master=self.top, text="ID")
        self.id_label.grid(row=1,column=0)
        self.id_entry = uiEntry(master=self.top)
        self.id_entry.grid(row=1,column=1)

        self.type_label = uiLabel(master=self.top, text="Type")
        self.type_label.grid(row=2,column=0)
        # box_value = tk.StringVar()
        self.combo = uiComboBox(master=self.top)
        self.combo.config(values=gstate.GSTATE_TYPES)
        self.combo.grid(row=2, column=1, padx=50,pady=10)
        self.combo.bind("<<ComboBoxSelect>>", lambda: ())

        self.btn = uiButton(master=self.top, text="Select", command=self.select)
        self.btn.grid(row=4,column=0,columnspan=2)
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.wait_window(self.top)  # wait for itself destroyed, so like a modal dialog

    
    def destroy(self):
        self.top.destroy()


    def select(self):
        self.gstate_type = self.combo.get()
        self.gstate_id = self.id_entry.get()
        self.destroy()

    def get_result(self):
        return {
            "id":self.gstate_id,
            "type":self.gstate_type,
            "msg":""
        }

class UIGetObjects():
    def __init__(self, ldr, selectmode="single"):

        self.objs = []

        self.top = tk.Toplevel() # use Toplevel() instead of Tk()
        
        self.label = uiLabel(master=self.top, text='Select one or more objects to add to the goal.')
        self.label.grid(row=0, column=0)
        
        obj_entries = []
        obj_data = ldr.get_obj_templates()
        for obj in obj_data.values():
            obj_entries.append(
                f"{obj['id']}:{obj['name']}"
            )

        self.listbox_var = tk.StringVar()
        self.listbox = uiListBox(
            master=self.top, listvariable=self.listbox_var, selectmode=selectmode
        )
        self.listbox_var.set(obj_entries)
        self.listbox.grid(row=1, column=0, padx=50,pady=10)
        # self.combo.bind("<<ComboBoxSelect>>", lambda: ())

        self.btn = uiButton(master=self.top, text="Select", command=self.select)
        self.btn.grid(row=2,column=0)
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.wait_window(self.top)  # wait for itself destroyed, so like a modal dialog

    
    def destroy(self):
        self.top.destroy()


    def select(self):
        selections = self.listbox.curselection()
        for s in selections:
            obj = self.listbox.get(s)
            obj_id = obj.split(":")[0]
            self.objs.append(obj_id)
        self.destroy()

    def get_result(self):
        return self.objs



class UIGetItems():
    def __init__(self, ldr, selectmode="single"):

        self.items = []

        self.top = tk.Toplevel() # use Toplevel() instead of Tk()
        
        self.label = uiLabel(master=self.top, text='Select one or more items to add to the goal.')
        self.label.grid(row=0, column=0)
        
        item_entries = []
        item_data = ldr.get_item_templates()
        for itm in item_data.values():
            item_entries.append(
                f"{itm['id']}:{itm['name']}"
            )

        self.listbox_var = tk.StringVar()
        self.listbox = uiListBox(
            master=self.top, listvariable=self.listbox_var, selectmode=selectmode
        )
        self.listbox_var.set(item_entries)
        self.listbox.grid(row=1, column=0, padx=50,pady=10)
        # self.combo.bind("<<ComboBoxSelect>>", lambda: ())

        self.btn = uiButton(master=self.top, text="Select", command=self.select)
        self.btn.grid(row=2,column=0)
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.wait_window(self.top)  # wait for itself destroyed, so like a modal dialog

    
    def destroy(self):
        self.top.destroy()


    def select(self):
        selections = self.listbox.curselection()
        for s in selections:
            itm = self.listbox.get(s)
            itm_id = itm.split(":")[0]
            self.items.append(itm_id)
        self.destroy()

    def get_result(self):
        return self.items


class UIGStateConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=BGCOLOR)
       
        self.logger = logger
        self.ldr = ldr

        self.build_ui()

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

    def build_ui(self):
        """
        Initializes all widgets and places them.
        """
        # Make frames
        self.main_frame = uiQuietFrame(master=self)
        self.goal_selection_frame = uiLabelFrame(master=self.main_frame,text="Goal List")
        self.button_row = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Goal Config")
        self.validate_num = self.main_frame.register(self.validate_number_entry)

        # Component Attribute Columns
        self.goal_general_frame = uiLabelFrame(master=self.main_frame, text="General Data")
        self.goal_items_touch_frame = uiLabelFrame(master=self.main_frame, text="ITEMS_TOUCH Data")
        self.goal_obj_items_touch_frame = uiLabelFrame(master=self.main_frame, text="OBJ_ITEMS_TOUCH Data")
        self.goal_n_objs_destroyed_frame = uiLabelFrame(master=self.main_frame, text="N_OBJS_DESTROYED Data")
        self.goal_n_objs_in_locs_frame = uiLabelFrame(master=self.main_frame, text="N_OBJS_IN_LOCS Data")

        self.goal_general_frame.columnconfigure(0,weight=1)

        self.current_goal_attribute_frame = None

        # Place frames
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.goal_selection_frame.pack(side=tk.LEFT, fill="y")
        self.goal_general_frame.pack(
            side=tk.LEFT, fill="y"
        )

        # Goal type selection
        self.select_goal_type_combo = uiComboBox(master=self.goal_selection_frame)
        self.select_goal_type_combo.configure(
            state="readonly",
            values=gstate.GSTATE_TYPES
        )
        self.select_goal_type_combo.pack(side=tk.TOP,fill=tk.BOTH)
        self.select_goal_type_combo.bind(
            "<<ComboboxSelected>>", self.populate_goal_listbox
        )


        # Component Selection widgets
        self.select_goal_listbox_var = tk.StringVar()
        self.select_goal_listbox = uiListBox(
            master=self.goal_selection_frame, 
            listvariable=self.select_goal_listbox_var,
            selectmode='single'
        )
        self.select_goal_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
        self.select_goal_listbox.bind(
            "<<ListboxSelect>>", self.show_goal
        )

        self.build_general_goal_ui()
        self.build_items_touch_ui()
        self.build_obj_items_touch_ui()
        self.build_n_objs_destroyed_ui()
        self.build_n_objs_in_locs_ui()

        # Buttons
        self.new_goal_button = uiButton(
            master=self.button_row, command=self.new_goal, text="Create Goal"
        )
        self.new_goal_button.pack(side=tk.LEFT)

        self.update_goal_button = uiButton(
            master=self.button_row,
            command=self.update_goal,
            text="Update Goal",
        )
        self.update_goal_button.pack(side=tk.LEFT)
        
        self.delete_goal_button = uiCarefulButton(
            master=self.button_row, command=self.delete_goal, text="Delete Goal"
        )
        self.delete_goal_button.pack(side=tk.LEFT)


        self.home_button = uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiCarefulButton(
            master=self.button_row, command=self.save_to_json, text="Save Comps to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

        self.populate_goal_listbox()

    def build_general_goal_ui(self):
        self.goal_id_label = uiLabel(master=self.goal_general_frame, text="ID")
        self.goal_id_entry = EntryHelp(
            master=self.goal_general_frame, text="Unique ID of the goal."
        )
        self.goal_type_label = uiLabel(master=self.goal_general_frame, text="Type")
        self.goal_type_entry = EntryHelp(
            master=self.goal_general_frame, text="The type of the goal. This can only be specified when a new goal is created. If you want to change a goal's type, you will need to delete the goal and recreate it."
        )
        self.goal_type_entry.entry.config(state="disabled")
        self.goal_msg_label = uiLabel(master=self.goal_general_frame, text="Desc")
        self.goal_msg_textbox = uiTextbox(master=self.goal_general_frame)
        self.goal_msg_textbox.configure(width=16, height=5, state=tk.NORMAL)

        self.goal_id_label.grid(row=0, column=0, sticky="ew")
        self.goal_id_entry.frame.grid(row=0, column=1, sticky="ew")
        self.goal_type_label.grid(row=1, column=0, sticky="ew")
        self.goal_type_entry.frame.grid(row=1, column=1, sticky="ew")
        self.goal_msg_label.grid(row=2,column=0,columnspan=2, sticky="ew")
        self.goal_msg_textbox.grid(row=3,column=0,columnspan=2, sticky="ew")

    def build_items_touch_ui(self):
    
        self.IT_items_label = uiLabel(
            master=self.goal_items_touch_frame, text="Items"
        )

        self.IT_items_listbox_var = tk.StringVar()
        self.IT_items_listbox = uiListBox(
            master=self.goal_items_touch_frame, 
            listvariable=self.IT_items_listbox_var,
            selectmode='multiple'
        )

        

        self.IT_add_items_button = uiButton(
            master=self.goal_items_touch_frame,
            command=self.IT_add_items,
            text="Add Item(s)"
        )
        self.IT_remove_items_button = uiButton(
            master=self.goal_items_touch_frame,
            command=self.IT_remove_items,
            text="Remove Item(s)"
        )

        self.IT_items_label.grid(row=0,column=0,columnspan=2, stick="ew")
        self.IT_items_listbox.grid(row=1,column=0,columnspan=2, sticky="nsew")
        self.IT_add_items_button.grid(row=2,column=0,columnspan=2, sticky="ew")
        self.IT_remove_items_button.grid(row=3,column=0,columnspan=2, sticky="ew")

    def build_obj_items_touch_ui(self):
        self.OIT_items_label = uiLabel(
            master=self.goal_obj_items_touch_frame, text="Items"
        )

        self.OIT_items_listbox_var = tk.StringVar()
        self.OIT_items_listbox = uiListBox(
            master=self.goal_obj_items_touch_frame, 
            listvariable=self.OIT_items_listbox_var,
            selectmode='multiple'
        )

        self.OIT_add_items_button = uiButton(
            master=self.goal_obj_items_touch_frame,
            command=self.OIT_add_items,
            text="Add Item(s)"
        )
        self.OIT_remove_items_button = uiButton(
            master=self.goal_obj_items_touch_frame,
            command=self.OIT_remove_items,
            text="Remove Item(s)"
        )

        self.OIT_obj_label = uiLabel(
            master=self.goal_obj_items_touch_frame,
            text="Object"
        )

        self.OIT_obj_entry = EntryHelp(
            master=self.goal_obj_items_touch_frame,
            text="The goal is complete when this object is in the same location as all items in the list above.\n\nNOTE: The value in this field can only be changed via the add/remove object buttons below."
        )
        self.OIT_obj_entry.entry.config(state="disabled")

        self.OIT_add_objs_button = uiButton(
            master=self.goal_obj_items_touch_frame,
            command=self.OIT_add_object,
            text="Add Object(s)"
        )
        self.OIT_remove_objs_button = uiButton(
            master=self.goal_obj_items_touch_frame,
            command=self.OIT_remove_objects,
            text="Remove Object(s)"
        )

        self.OIT_items_label.grid(row=0,column=0,stick="ew")
        self.OIT_items_listbox.grid(row=1,column=0,columnspan=2,sticky="nsew")
        self.OIT_add_items_button.grid(row=2,column=0,columnspan=2,sticky="ew")
        self.OIT_remove_items_button.grid(row=3,column=0,columnspan=2,sticky="ew")
        self.OIT_obj_label.grid(row=4, column=0, sticky="ew")
        self.OIT_obj_entry.frame.grid(row=4, column=1, sticky="ew")
        self.OIT_add_objs_button.grid(row=5, column=0, columnspan=2,sticky="ew")
        self.OIT_remove_objs_button.grid(row=6, column=0, columnspan=2,sticky="ew")
    def build_n_objs_destroyed_ui(self):
        self.NOD_amount_label = uiLabel(
            master=self.goal_n_objs_destroyed_frame, text="Amount (N)"
        )
        self.NOD_amount_entry = EntryHelp(
            master=self.goal_n_objs_destroyed_frame, text="The number of the objects below that must be destroyed to complete this goal. Amount cannot be set to a value larger than the number of objects in the listbox below."
        )


        self.NOD_objs_label = uiLabel(
            master=self.goal_n_objs_destroyed_frame,
            text="Objects"
        )

        self.NOD_objs_listbox_var = tk.StringVar()
        self.NOD_objs_listbox = uiListBox(
            master=self.goal_n_objs_destroyed_frame,
            listvariable=self.NOD_objs_listbox_var,
            selectmode='multiple'
        )
        self.NOD_add_objs_button = uiButton(
            master=self.goal_n_objs_destroyed_frame,
            command=self.NOD_add_objects,
            text="Add Object(s)"
        )
        self.NOD_remove_objs_button = uiButton(
            master=self.goal_n_objs_destroyed_frame,
            command=self.NOD_remove_objects,
            text="Remove Object(s)"
        )

        self.NOD_amount_label.grid(row=0,column=0,stick="ew")
        self.NOD_amount_entry.frame.grid(row=0, column=1, sticky="ew")

        self.NOD_objs_label.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.NOD_objs_listbox.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.NOD_add_objs_button.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.NOD_remove_objs_button.grid(row=4, column=0, columnspan=2, sticky="ew")
    def build_n_objs_in_locs_ui(self):
        self.NOIL_amount_label = uiLabel(
            master=self.goal_n_objs_in_locs_frame,
            text="Amount (N)"
        )
        self.NOIL_amount_entry = EntryHelp(
            master=self.goal_n_objs_in_locs_frame,
            text="The number of objects that must be in one of the goal locations."
        )
        self.NOIL_objs_label = uiLabel(
            master=self.goal_n_objs_in_locs_frame,
            text="Objects"
        )
        self.NOIL_objs_listbox_var = tk.StringVar()
        self.NOIL_objs_listbox = uiListBox(
            master=self.goal_n_objs_in_locs_frame,
            listvariable=self.NOIL_objs_listbox_var,
            selectmode='multiple'
        )
        self.NOIL_add_objs_button = uiButton(
            master = self.goal_n_objs_in_locs_frame,
            command=self.NOIL_add_objects,
            text="Add Object(s)"
        )
        self.NOIL_remove_objs_button = uiButton(
            master=self.goal_n_objs_in_locs_frame,
            command=self.NOIL_remove_objects,
            text="Remove Object(s)"
        )

        self.NOIL_locs_label = uiLabel(
            master=self.goal_n_objs_in_locs_frame,
            text="Locations"
        )
        self.NOIL_locs_listbox_var = tk.StringVar()
        self.NOIL_locs_listbox = uiListBox(
            master=self.goal_n_objs_in_locs_frame,
            listvariable=self.NOIL_locs_listbox_var,
            selectmode='multiple'
        )
        self.NOIL_add_locs_button = uiButton(
            master = self.goal_n_objs_in_locs_frame,
            command=self.NOIL_add_locations,
            text="Add Locations(s)"
        )
        self.NOIL_remove_locs_button = uiButton(
            master=self.goal_n_objs_in_locs_frame,
            command=self.NOIL_remove_locations,
            text="Remove Locations(s)"
        )

        self.NOIL_amount_label.grid(row=0, column=0, sticky="ew")
        self.NOIL_amount_entry.frame.grid(row=0, column=1, sticky="ew")
        self.NOIL_objs_label.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.NOIL_objs_listbox.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.NOIL_add_objs_button.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.NOIL_remove_objs_button.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.NOIL_locs_label.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.NOIL_locs_listbox.grid(row=6, column=0, columnspan=2, sticky="ew")
        self.NOIL_add_locs_button.grid(row=7, column=0, columnspan=2, sticky="ew")
        self.NOIL_remove_locs_button.grid(row=8, column=0, columnspan=2, sticky="ew")

    def populate_goal_listbox(self, event=None):

        self.clear_all_fields()

        goal_type = self.select_goal_type_combo.get()
        self.show_goal_type_attr_frame(goal_type)

        goal_data = self.ldr.get_gstate_templates()
        keys = []

        for goal in goal_data.values():
            if goal["type"] == goal_type:
                keys.append(f"{goal['id']}")


        self.select_goal_listbox.delete(0,tk.END)
        self.select_goal_listbox_var.set(keys)

    def show_goal_type_attr_frame(self, goal_type):
        
        next_attr_frame = self.current_goal_attribute_frame

        match(goal_type):
            case "ITEMS_TOUCH":
                next_attr_frame = self.goal_items_touch_frame
            case "OBJ_ITEMS_TOUCH":
                next_attr_frame = self.goal_obj_items_touch_frame
            case "N_OBJS_DESTROYED":
                next_attr_frame = self.goal_n_objs_destroyed_frame
            case "N_OBJS_IN_LOCS":
                next_attr_frame = self.goal_n_objs_in_locs_frame

        if self.current_goal_attribute_frame != next_attr_frame:
            if self.current_goal_attribute_frame != None:
                self.current_goal_attribute_frame.pack_forget()
            self.current_goal_attribute_frame = next_attr_frame
            self.current_goal_attribute_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        


    def show_goal(self, event=None):
        selected_goal = self.get_currently_selected_goal()
        if selected_goal != None:
            self.clear_all_fields()

            self.goal_id_entry.entry.insert(0, selected_goal["id"])
            self.goal_type_entry.entry.config(state='normal')
            self.goal_type_entry.entry.insert(0, selected_goal["type"])
            self.goal_type_entry.entry.config(state='disabled')
            self.goal_msg_textbox.insert(1.0,selected_goal["msg"])

            match(selected_goal["type"]):
                case "ITEMS_TOUCH":
                    self.show_items_touch(selected_goal)
                case "OBJ_ITEMS_TOUCH":
                    self.show_obj_items_touch(selected_goal)
                case "N_OBJS_DESTROYED":
                    self.show_n_objs_destroyed(selected_goal)
                case "N_OBJS_IN_LOCS":
                    self.show_n_objs_in_locs(selected_goal)

    def show_items_touch(self, goal):
        self.IT_items_listbox_var.set(goal["items"])
    def show_obj_items_touch(self, goal):
        self.OIT_items_listbox_var.set(goal["items"])
        self.OIT_obj_entry.entry.config(state="normal")
        self.OIT_obj_entry.entry.insert(0,goal["object"])
        self.OIT_obj_entry.entry.config(state="disabled")
    def show_n_objs_destroyed(self, goal):
        self.NOD_amount_entry.entry.insert(0, goal["amount"])
        self.NOD_objs_listbox_var.set(goal["objects"])
    def show_n_objs_in_locs(self, goal):
        self.NOIL_amount_entry.entry.insert(0, goal["amount"])
        self.NOIL_objs_listbox_var.set(goal["objects"])
        self.NOIL_locs_listbox_var.set(goal["locations"])
    def clear_all_fields(self):
        # General
        self.goal_id_entry.entry.delete(0, tk.END)
        self.goal_type_entry.entry.config(state='normal')
        self.goal_type_entry.entry.delete(0, tk.END)
        self.goal_type_entry.entry.config(state='disabled')
        self.goal_msg_textbox.delete(1.0,tk.END)
        # ITEMS_TOUCH
        self.IT_items_listbox.delete(0, tk.END)
        # OBJ_ITEMS_TOUCH
        self.OIT_items_listbox.delete(0, tk.END)
        self.OIT_obj_entry.entry.delete(0, tk.END)
        # N_OBJS_DESTROYED
        self.NOD_amount_entry.entry.delete(0, tk.END)
        self.NOD_objs_listbox.delete(0, tk.END)
        # N_OBJS_IN_LOCS
        self.NOIL_amount_entry.entry.delete(0, tk.END)
        self.NOIL_objs_listbox.delete(0, tk.END)
        self.NOIL_locs_listbox.delete(0, tk.END)
    def get_currently_selected_goal(self):
        goal_index = self.select_goal_listbox.curselection()
        if len(goal_index) == 1:
            goal_id = self.select_goal_listbox.get(goal_index[0])
            return self.ldr.get_gstate_template(goal_id)
        else:
            return None

    def select_goal_with_id(self, _id):
        for index, goal_id in enumerate(self.select_goal_listbox.get(0,tk.END)):
            if _id == goal_id:
                self.select_goal_listbox.selection_clear(0, tk.END)
                self.select_goal_listbox.selection_set(index)
                self.select_goal_listbox.activate(index)
                self.show_goal()
                break

    def update_goal(self):
        """
        Updates the components JSON. values
        """
        goal_data = self.ldr.get_gstate_templates()
        selected_goal = self.get_currently_selected_goal()
        if selected_goal != None:

            # Update the ctype specific attributes
            match selected_goal["type"]:
                case "ITEMS_TOUCH":
                    self.update_items_touch(selected_goal)
                case "OBJ_ITEMS_TOUCH":
                    self.update_obj_items_touch(selected_goal)
                case "N_OBJS_DESTROYED":
                    self.update_n_objs_destroyed(selected_goal)
                case "N_OBJS_IN_LOCS":
                    self.update_n_objs_in_locs(selected_goal)
            

            new_id = self.goal_id_entry.entry.get()

            # Update ID: must check if unique
            if new_id != selected_goal["id"]:
                if new_id in [x["id"] for x in goal_data]:
                    tk.messagebox.showwarning(
                        "Invalid goal ID",
                        f"WARNING: The goal id {new_id} already exists. Goal IDs must be unique."
                    )
                elif len(new_id) == 0:
                    tk.messagebox.showwarning(
                        "Invalid goal ID",
                        "Goal IDs cannot be empty."
                    )
                else:
                    old_id = selected_goal["id"]
                    selected_goal["id"] = new_id
                    del goal_data[old_id]
                    goal_data[new_id] = selected_goal

            selected_goal["msg"] = self.goal_msg_textbox.get(1.0,tk.END)

            self.populate_goal_listbox(selected_goal["id"])
            self.select_goal_with_id(selected_goal["id"])

    def update_items_touch(self, selected_goal):
        items = self.IT_items_listbox.get(0, tk.END)
        if len(items) < 2:
            tk.messagebox.showwarning(
                "Too Few Items",
                "This goal requires at least two items."
            )
        else:
            selected_goal["items"] = items
    def update_obj_items_touch(self, selected_goal):
        items = self.OIT_items_listbox.get(0, tk.END)
        obj = self.OIT_obj_entry.entry.get()
        if len(items)==0 :
            tk.messagebox.showwarning(
                "Too Few Items",
                "This goal requires at least one item."
            )
        elif len(obj)==0:
            tk.messagebox.showwarning(
                "Object cannot be empty",
                "This goal requires at least one object."
            )
        else:
            selected_goal["items"]=items
            selected_goal["object"]=obj
    def update_n_objs_destroyed(self, selected_goal):
        amount = self.NOD_amount_entry.entry.get()
        objs = self.NOD_objs_listbox.get(0,tk.END)
        try:
            amount = int(amount)
            if amount <= 0:
                raise Exception
        except:
            tk.messagebox.showwarning(
                "Invalid Amount",
                "Amount must be a positive integer."
            )

        if amount > len(objs):
            tk.messagebox.showwarning(
                "Amount Too Large",
                "The value in the amount field cannot be larger than the number of objects in the listbox."
            )
        elif len(objs) == 0:
            tk.messagebox.showwarning(
                "Too Few Objects",
                "This goal must have at least one object."
            )
        else:
            selected_goal["amount"]=amount
            selected_goal["objects"]=objs

    def update_n_objs_in_locs(self, selected_goal):
        amount = self.NOIL_amount_entry.entry.get()
        objs = self.NOIL_objs_listbox.get(0,tk.END)
        locs = self.NOIL_locs_listbox.get(0,tk.END)

        try:
            amount = int(amount)
            if amount <= 0:
                raise Exception
        except:
            tk.messagebox.showwarning(
                "Invalid Amount",
                "Amount must be a positive integer."
            )
        if amount > len(objs):
            tk.messagebox.showwarning(
                "Invalid Amount",
                "The value in amount cannot be larger than the number of objects."
            )
        elif amount > len(locs):
            tk.messagebox.showwarning(
                "Invalid Amount",
                "The value in amount cannot be larger than the number of locations."
            )
        else:
            selected_goal["objects"]=objs
            selected_goal["locations"]=locs
            selected_goal["amount"]=amount

    def new_goal(self):
        """
        Creates a new goal template and adds it to the goal dictionary.
        """

        goal_data = self.ldr.get_gstate_templates()

        goal_id_svar = tk.StringVar()
        goal_type_svar = tk.StringVar()

        good = False
        while not good:

            dialog = UINewGoal()
            result = dialog.get_result()

            if result["type"] in gstate.GSTATE_TYPES:
                if len(result["id"]) > 0 and result["id"] not in [x["id"] for x in goal_data.values()]:
                    good = True
                else:
                    messagebox.showwarning(
                        "Warning", "A goal must have a non-empty, unique ID."
                    )
            else:
                messagebox.showwarning(
                    "Warning", "A goal must have a valid type."
                )

        goal_attrs = gstate.GOAL_ATTRS_BY_TYPE[result["type"]]

        for attr, val in goal_attrs:
            result[attr] = val

        goal_data.update({result["id"]: result})
        
        self.populate_goal_listbox()
    

    def delete_goal(self):
        """
        Deletes the currently selected component from the JSON and component dictionary.
        """

        goal_data = self.ldr.get_gstate_templates()

        selected_goal = self.get_currently_selected_goal()
        if selected_goal != None:
            del goal_data[selected_goal["id"]]
            self.populate_goal_listbox()

    def IT_add_items(self, event=None):
        dialog = UIGetItems(self.ldr, "multiple")
        results = dialog.get_result()
        if results != None:
            for result in results: 
                self.IT_items_listbox.insert(tk.END,result)
    def IT_remove_items(self, event=None):
        selections = self.IT_items_listbox.curselection()
        for s in reversed(selections):
            self.IT_items_listbox.delete(s)
    def OIT_add_items(self, event=None):
        dialog = UIGetItems(self.ldr, "multiple")
        results = dialog.get_result()
        if results != None:
            for result in results: 
                self.OIT_items_listbox.insert(tk.END,result)
    def OIT_remove_items(self, event=None):
        selections = self.OIT_items_listbox.curselection()
        for s in reversed(selections):
            self.OIT_items_listbox.delete(s)
    def OIT_add_object(self, event=None):
        dialog = UIGetObjects(self.ldr, "single")
        result = dialog.get_result()
        if result != None and len(result)==1:
            self.OIT_obj_entry.entry.config(state="normal")
            self.OIT_obj_entry.entry.insert(0,result[0])
            self.OIT_obj_entry.entry.config(state="disabled")
    def OIT_remove_objects(self, event=None):
        self.OIT_obj_entry.entry.config(state="normal")
        self.OIT_obj_entry.entry.insert(0,"")
        self.OIT_obj_entry.entry.config(state="disabled")
    def NOD_add_objects(self, event=None):
        dialog = UIGetObjects(self.ldr, "multiple")
        results = dialog.get_result()
        if results != None:
            for result in results: 
                self.NOD_objs_listbox.insert(tk.END,result)
    def NOD_remove_objects(self, event=None):
        selections = self.NOD_objs_listbox.curselection()
        for s in reversed(selections):
            self.NOD_objs_listbox.delete(s)
    def NOIL_add_objects(self, event=None):
        dialog = UIGetObjects(self.ldr, "multiple")
        results = dialog.get_result()
        if results != None:
            for result in results: 
                self.NOIL_objs_listbox.insert(tk.END,result)
    def NOIL_remove_objects(self, event=None):
        selections = self.NOIL_objs_listbox.curselection()
        for s in reversed(selections):
            self.NOIL_objs_listbox.delete(s)
    def NOIL_add_locations(self, event=None):
        new_loc = tk.simpledialog.askstring(
            "New Goal Location",
            "Enter a new x,y location in the format: x,y\n\nValues for x and y must be integers. They should be valid, reachable locations for the intended map (not verified by the system)."
        )
        xy = new_loc.split(",")
        if len(xy) == 2 and xy[0].isdigit() and xy[1].isdigit():
            # Cast to int to remove beginning zeros or plus sign.
            #   not that anyone will do this.
            x = int(xy[0])
            y = int(xy[1])
            # prevent negatives
            if x >= 0 and y >= 0:
                self.NOIL_locs_listbox.insert(tk.END, f"{x},{y}")

    def NOIL_remove_locations(self, event=None):
        selections = self.NOIL_locs_listbox.curselection()
        for s in reversed(selections):
            self.NOIL_locs_listbox.delete(s)

    def goto_home(self):
        self.controller.show_frame("home_page")

    def save_to_json(self):
        self.ldr.save_gstate_templates()


    

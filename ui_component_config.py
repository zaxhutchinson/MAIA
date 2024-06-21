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

class UINewComponent():
    def __init__(self):

        self.comp_id_svar = tk.StringVar()
        self.comp_ctype_svar = tk.StringVar()
        self.comp_name_svar = tk.StringVar()

        self.top = tk.Toplevel() # use Toplevel() instead of Tk()
        
        self.label = uiLabel(master=self.top, text='Provide a unique ID, a name and the ctype of the new component.')
        self.label.grid(row=0, column=0,columnspan=2)

        self.id_label = uiLabel(master=self.top, text="ID")
        self.id_label.grid(row=1,column=0)
        self.id_entry = uiEntry(master=self.top)
        self.id_entry.grid(row=1,column=1)

        self.ctype_label = uiLabel(master=self.top, text="CType")
        self.ctype_label.grid(row=2,column=0)
        # box_value = tk.StringVar()
        self.combo = uiComboBox(master=self.top)
        self.combo.config(values=comp.CTYPES_LIST)
        self.combo.grid(row=2, column=1, padx=50,pady=10)
        self.combo.bind("<<ComboBoxSelect>>", lambda: ())
        
        self.name_label = uiLabel(master=self.top, text="Name")
        self.name_label.grid(row=3,column=0)
        self.name_entry = uiEntry(master=self.top)
        self.name_entry.grid(row=3, column=1, padx=50,pady=10)

        self.btn = uiButton(master=self.top, text="Select", command=self.select)
        self.btn.grid(row=4,column=0,columnspan=2)
        self.top.wait_visibility()
        self.top.grab_set()
        self.top.wait_window(self.top)  # wait for itself destroyed, so like a modal dialog

        

    def destroy(self):
        self.top.destroy()


    def select(self):
        self.comp_ctype = self.combo.get()
        self.comp_id = self.id_entry.get()
        self.comp_name = self.name_entry.get()
        self.destroy()

    def get_result(self):
        return {
            "id":self.comp_id,
            "ctype":self.comp_ctype,
            "name":self.comp_name
        }


class UIComponentConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=BGCOLOR)
       
        self.logger = logger
        self.ldr = ldr

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
        # Make frames
        self.main_frame = uiQuietFrame(master=self)
        self.component_selection_frame = uiLabelFrame(master=self.main_frame,text="Component List")
        self.button_row = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Component Config")
        self.validate_num = self.main_frame.register(self.validate_number_entry)

        # Component Attribute Columns
        self.comp_general_frame = uiLabelFrame(master=self.main_frame, text="General Data")
        self.comp_fixed_gun_frame = uiLabelFrame(master=self.main_frame, text="FixedGun Data")
        self.comp_engine_frame = uiLabelFrame(master=self.main_frame, text="Engine Data")
        self.comp_radar_frame = uiLabelFrame(master=self.main_frame, text="Radar Data")
        self.comp_cnc_frame = uiLabelFrame(master=self.main_frame, text="CnC Data")
        self.comp_radio_frame = uiLabelFrame(master=self.main_frame, text="Radio Data")
        self.comp_arm_frame = uiLabelFrame(master=self.main_frame, text="Arm Data")
        self.current_comp_attribute_frame = None

        # Place frames
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.component_selection_frame.pack(side=tk.LEFT, fill="y")
        self.comp_general_frame.pack(
            side=tk.LEFT, fill="y"
        )

        # CType selection
        self.select_component_type_combo = uiComboBox(master=self.component_selection_frame)
        self.select_component_type_combo.configure(
            state="readonly",
            values=comp.CTYPES_LIST
        )
        self.select_component_type_combo.pack(side=tk.TOP,fill=tk.BOTH)
        self.select_component_type_combo.bind(
            "<<ComboboxSelected>>", self.populate_comp_listbox
        )


        # Component Selection widgets
        self.select_comp_listbox_var = tk.StringVar()
        self.select_comp_listbox = uiListBox(
            master=self.component_selection_frame, 
            listvariable=self.select_comp_listbox_var,
            selectmode='browse'
        )
        self.select_comp_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
        self.select_comp_listbox.bind(
            "<<ListboxSelect>>", self.show_component
        )

        self.build_general_comp_ui()
        self.build_fixed_gun_comp_ui()
        self.build_engine_comp_ui()
        self.build_radar_comp_ui()
        self.build_cnc_comp_ui()
        self.build_radio_comp_ui()
        self.build_arm_comp_ui()

        # Buttons
        self.components_create_button = uiButton(
            master=self.button_row, command=self.create_component, text="Add Component"
        )
        self.components_create_button.pack(side=tk.LEFT)

        self.components_update_button = uiButton(
            master=self.button_row,
            command=self.update_component,
            text="Update Component",
        )
        self.components_update_button.pack(side=tk.LEFT)
        
        self.components_delete_button = uiCarefulButton(
            master=self.button_row, command=self.delete_components, text="Delete Component"
        )
        self.components_delete_button.pack(side=tk.LEFT)


        self.home_button = uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiCarefulButton(
            master=self.button_row, command=self.save_to_json, text="Save Comps to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

        self.populate_comp_listbox()

    def build_general_comp_ui(self):
        self.components_id_label = uiLabel(master=self.comp_general_frame, text="ID:")
        self.components_id_entry = EntryHelp(
            master=self.comp_general_frame, text="To be added."
        )
        self.components_name_label = uiLabel(
            master=self.comp_general_frame, text="Name:"
        )
        self.components_name_entry = EntryHelp(
            master=self.comp_general_frame, text="To be added."
        )

        self.components_id_label.grid(row=1, column=0, sticky="ew")
        self.components_id_entry.frame.grid(row=1, column=1, sticky="ew")
        self.components_name_label.grid(row=2, column=0, sticky="ew")
        self.components_name_entry.frame.grid(row=2, column=1, sticky="ew")

    def build_fixed_gun_comp_ui(self):
    
        self.fg_reload_ticks_label = uiLabel(
            master=self.comp_fixed_gun_frame, text="Reload Ticks"
        )
        self.fg_reload_ticks_entry = EntryHelp(
            master=self.comp_fixed_gun_frame, text="The number of turns it takes the gun to reload."
        )
        self.fg_ammo_label = uiLabel(
            master=self.comp_fixed_gun_frame, text="Ammunition"
        )
        self.fg_ammo_entry = EntryHelp(
            master=self.comp_fixed_gun_frame, text="The amount of starting ammunition."
        )
        self.fg_min_damage_label = uiLabel(
            master=self.comp_fixed_gun_frame, text="Min Damage"
        )
        self.fg_min_damage_entry = EntryHelp(
            master=self.comp_fixed_gun_frame, text="The minimum damage the weapon causes."
        )
        self.fg_max_damage_label = uiLabel(
            master=self.comp_fixed_gun_frame, text="Max Damage"
        )
        self.fg_max_damage_entry = EntryHelp(
            master=self.comp_fixed_gun_frame, text="The maximum damage the weapon causes."
        )
        self.fg_wpn_range_label = uiLabel(
            master=self.comp_fixed_gun_frame, text="Range"
        )
        self.fg_wpn_range_entry = EntryHelp(
            master=self.comp_fixed_gun_frame, text="The maximum distance a projectile will travel."
        )

        self.fg_reload_ticks_label.grid(row=1, column=0, sticky="ew")
        self.fg_reload_ticks_entry.frame.grid(row=1, column=1, sticky="ew")
        self.fg_reload_ticks_entry.entry.config(
            validate="key", validatecommand=(self.validate_num, "%P")
        )
        self.fg_ammo_label.grid(row=2, column=0, sticky="ew")
        self.fg_ammo_entry.frame.grid(row=2, column=1, sticky="ew")
        self.fg_min_damage_label.grid(row=3, column=0, sticky="ew")
        self.fg_min_damage_entry.frame.grid(row=3, column=1, sticky="ew")
        self.fg_max_damage_label.grid(row=4, column=0, sticky="ew")
        self.fg_max_damage_entry.frame.grid(row=4, column=1, sticky="ew")
        self.fg_wpn_range_label.grid(row=5, column=0, sticky="ew")
        self.fg_wpn_range_entry.frame.grid(row=5, column=1, sticky="ew")
    def build_engine_comp_ui(self):
        self.engine_min_speed_label = uiLabel(
            master=self.comp_engine_frame, text="Min Speed"
        )
        self.engine_min_speed_entry = EntryHelp(
            master=self.comp_engine_frame, text="The minimum speed of the engine. Negative values allow the object to move in reverse. If an object cannot reverse direction, min speed should be set to 0.0."
        )
        self.engine_max_speed_label = uiLabel(
            master=self.comp_engine_frame, text="Max Speed"
        )
        self.engine_max_speed_entry = EntryHelp(
            master=self.comp_engine_frame, text="The maximum speed of the engine. Speed directly translates into object velocity."
        )
        self.engine_max_turnrate_label = uiLabel(
            master=self.comp_engine_frame, text="Max Turnrate"
        )
        self.engine_max_turnrate_entry = EntryHelp(
            master=self.comp_engine_frame, text="The maximum angle an object can rotate in one tick (in degrees). Turnrate is symmetric."
        )
        self.engine_min_speed_label.grid(row=0, column=0, sticky="ew")
        self.engine_min_speed_entry.frame.grid(row=0, column=1, sticky="ew")
        self.engine_max_speed_label.grid(row=1, column=0, sticky="ew")
        self.engine_max_speed_entry.frame.grid(row=1, column=1, sticky="ew")
        self.engine_max_turnrate_label.grid(row=2, column=0, sticky="ew")
        self.engine_max_turnrate_entry.frame.grid(row=2, column=1, sticky="ew")
    def build_radar_comp_ui(self):
        self.radar_range_label = uiLabel(
            master=self.comp_radar_frame, text="Radar Range"
        )
        self.radar_range_entry = EntryHelp(
            master=self.comp_radar_frame, text="The maximum distance the radar can detect objects."
        )
        self.radar_level_label = uiLabel(
            master=self.comp_radar_frame, text="Radar Level"
        )
        self.radar_level_entry = EntryHelp(
            master=self.comp_radar_frame, text="A higher radar allows the radar beam to pass through objects with a lower density. For example, a radar with a level of 100 can see through objects of density 0 to 99. However, it could not see through an object with a density of 100."
        )
        self.radar_visarc_label = uiLabel(
            master=self.comp_radar_frame, text="Visible Arc"
        )
        self.radar_visarc_entry = EntryHelp(
            master=self.comp_radar_frame, text="A radar's visible arc (and resolution) determine how much of the environment the radar can \"see\". A radar's with a visible arc extends from its offset angle in both directions. Within this arc around the offset, it sends out detection rays. How many rays and how far apart the rays are is determined by the \"resolution\" attribute."
        )
        self.radar_offset_angle_label = uiLabel(
            master=self.comp_radar_frame, text="Offset Angle"
        )
        self.radar_offset_angle_entry = EntryHelp(
            master=self.comp_radar_frame, text="The offset angle (in degrees) gives the direction the radar points relative to the front of the object. For example, an offset angle of 0 means the radar faces the same direction as the object. An offset of 180 would mean the radar sees behind the object."
        )
        self.radar_resolution_label = uiLabel(
            master=self.comp_radar_frame, text="Resolution"
        )
        self.radar_resolution_entry = EntryHelp(
            master=self.comp_radar_frame, text="The resolution (in degrees) determines the interval between radar beams within its visible arc. For example, if a radar has an offset of 0, a visible arc of 20 and a resolution of 5, the radar will send out beams at the following degrees (as offsets from the object's facing): 20, 15, 10, 5, 0, -5, -10, -15, -20."
        )

        self.radar_range_label.grid(row=0, column=0, sticky="ew")
        self.radar_range_entry.frame.grid(row=0, column=1, sticky="ew")
        self.radar_level_label.grid(row=1, column=0, sticky="ew")
        self.radar_level_entry.frame.grid(row=1,column=1,sticky="ew")
        self.radar_visarc_label.grid(row=2, column=0, sticky="ew")
        self.radar_visarc_entry.frame.grid(row=2, column=1, sticky="ew")
        self.radar_offset_angle_label.grid(row=3, column=0, sticky="ew")
        self.radar_offset_angle_entry.frame.grid(row=3, column=1, sticky="ew")
        self.radar_resolution_label.grid(row=4, column=0, sticky="ew")
        self.radar_resolution_entry.frame.grid(row=4, column=1, sticky="ew")
    def build_cnc_comp_ui(self):
        self.cnc_max_commands_per_tick_label = uiLabel(
            master=self.comp_cnc_frame, text="Max Cmds per Tick"
        )
        self.cnc_max_commands_per_tick_entry = EntryHelp(
            master=self.comp_cnc_frame, text="The maximum number of commands, across all components, that can be processed in a given turn."
        )
        self.cnc_max_commands_per_tick_label.grid(row=0, column=0, sticky="ew")
        self.cnc_max_commands_per_tick_entry.frame.grid(row=0, column=1, sticky="ew")
    def build_radio_comp_ui(self):
        self.radio_max_broadcast_range_label = uiLabel(
            master=self.comp_radio_frame, text="Max Broadcast Range"
        )
        self.radio_max_broadcast_range_entry = EntryHelp(
            master=self.comp_radio_frame, text="The max distance from the sending object a message can be received."
        )
        self.radio_max_broadcast_range_label.grid(row=0, column=0, sticky="ew")
        self.radio_max_broadcast_range_entry.frame.grid(row=0, column=1, sticky="ew")
    def build_arm_comp_ui(self):
        self.arm_max_weight_label = uiLabel(
            master=self.comp_arm_frame, text="Max Weight"
        )
        self.arm_max_weight_entry = EntryHelp(
            master=self.comp_arm_frame, text="The maximum weight the arm can lift."
        )
        self.arm_max_bulk_label = uiLabel(
            master=self.comp_arm_frame, text="Max Bulk"
        )
        self.arm_max_bulk_entry = EntryHelp(
            master=self.comp_arm_frame, text="The maximum bulk the arm can manage."
        )
        self.arm_max_weight_label.grid(row=0, column=0, sticky="ew")
        self.arm_max_weight_entry.frame.grid(row=0, column=1, sticky="ew")
        self.arm_max_bulk_label.grid(row=1, column=0, sticky="ew")
        self.arm_max_bulk_entry.frame.grid(row=1, column=1, sticky="ew")

    def populate_comp_listbox(self, event=None):

        self.clear_all_fields()

        _ctype = self.select_component_type_combo.get()
        self.show_ctype_attr_frame(_ctype)

        comp_data = self.ldr.get_comp_templates()
        keys = []

        for comp in comp_data.values():
            if comp["ctype"] == _ctype:
                keys.append(f"{comp["id"]}:{comp["name"]}")


        self.select_comp_listbox.delete(0,tk.END)
        self.select_comp_listbox_var.set(sorted(keys))

    def show_ctype_attr_frame(self, _ctype):
        
        next_attr_frame = self.current_comp_attribute_frame

        match(_ctype):
            case "FixedGun":
                next_attr_frame = self.comp_fixed_gun_frame
            case "Engine":
                next_attr_frame = self.comp_engine_frame
            case "Radar":
                next_attr_frame = self.comp_radar_frame
            case "CnC":
                next_attr_frame = self.comp_cnc_frame
            case "Radio":
                next_attr_frame = self.comp_radio_frame
            case "Arm":
                next_attr_frame = self.comp_arm_frame

        if self.current_comp_attribute_frame != next_attr_frame:
            if self.current_comp_attribute_frame != None:
                self.current_comp_attribute_frame.pack_forget()
            self.current_comp_attribute_frame = next_attr_frame
            self.current_comp_attribute_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        


    def show_component(self, event=None):
        selected_comp = self.get_currently_selected_component()
        if selected_comp != None:
            self.clear_all_fields()

            self.components_id_entry.entry.insert(0, selected_comp["id"])
            self.components_name_entry.entry.insert(0, selected_comp["name"])

            match(selected_comp["ctype"]):
                case "FixedGun":
                    self.show_fixed_gun(selected_comp)
                case "Engine":
                    self.show_engine(selected_comp)
                case "Radar":
                    self.show_radar(selected_comp)
                case "CnC":
                    self.show_cnc(selected_comp)
                case "Radio":
                    self.show_radio(selected_comp)
                case "Arm":
                    self.show_arm(selected_comp)

    def show_fixed_gun(self, comp):
        self.fg_reload_ticks_entry.entry.insert(0, comp["reload_ticks"])
        self.fg_ammo_entry.entry.insert(0, comp["ammunition"])
        self.fg_min_damage_entry.entry.insert(0, comp["min_damage"])
        self.fg_max_damage_entry.entry.insert(0, comp["max_damage"])
        self.fg_wpn_range_entry.entry.insert(0, comp["range"])
    def show_engine(self, comp):
        self.engine_min_speed_entry.entry.insert(0, comp["min_speed"])
        self.engine_max_speed_entry.entry.insert(0, comp["max_speed"])
        self.engine_max_turnrate_entry.entry.insert(0, comp["max_turnrate"])
    def show_radar(self, comp):
        self.radar_range_entry.entry.insert(0, comp["range"])
        self.radar_level_entry.entry.insert(0, comp["level"])
        self.radar_visarc_entry.entry.insert(0, comp["visarc"])
        self.radar_offset_angle_entry.entry.insert(0, comp["offset_angle"])
        self.radar_resolution_entry.entry.insert(0, comp["resolution"])
    def show_cnc(self, comp):
        self.cnc_max_commands_per_tick_entry.entry.insert(0, comp["max_cmds_per_tick"])
    def show_radio(self, comp):
        self.radio_max_broadcast_range_entry.entry.insert(0, comp["max_range"])
    def show_arm(self, comp):
        self.arm_max_weight_entry.entry.insert(0, comp["max_weight"])
        self.arm_max_bulk_entry.entry.insert(0, comp["max_bulk"])

    def clear_all_fields(self):
        # General
        self.components_id_entry.entry.delete(0, tk.END)
        self.components_name_entry.entry.delete(0, tk.END)
        # FixedGun
        self.fg_reload_ticks_entry.entry.delete(0, tk.END)
        self.fg_ammo_entry.entry.delete(0, tk.END)
        self.fg_min_damage_entry.entry.delete(0, tk.END)
        self.fg_max_damage_entry.entry.delete(0, tk.END)
        self.fg_wpn_range_entry.entry.delete(0, tk.END)
        # Engine
        self.engine_min_speed_entry.entry.delete(0, tk.END)
        self.engine_max_speed_entry.entry.delete(0, tk.END)
        self.engine_max_turnrate_entry.entry.delete(0, tk.END)
        # Radar
        self.radar_range_entry.entry.delete(0, tk.END)
        self.radar_level_entry.entry.delete(0, tk.END)
        self.radar_visarc_entry.entry.delete(0, tk.END)
        self.radar_offset_angle_entry.entry.delete(0, tk.END)
        self.radar_resolution_entry.entry.delete(0, tk.END)
        # CnC
        self.cnc_max_commands_per_tick_entry.entry.delete(0, tk.END)
        # Radio
        self.radio_max_broadcast_range_entry.entry.delete(0, tk.END)
        # Arm
        self.arm_max_weight_entry.entry.delete(0, tk.END)
        self.arm_max_bulk_entry.entry.delete(0, tk.END)

    def get_currently_selected_component(self):
        comp_index = self.select_comp_listbox.curselection()
        if len(comp_index) == 1:
            comp_entry = self.select_comp_listbox.get(comp_index[0])
            comp_id, comp_name = comp_entry.split(":")
            return self.ldr.get_comp_template(comp_id)
        else:
            return None

    def select_comp_with_id(self, _id):
        for index, entry in enumerate(self.select_comp_listbox.get(0,tk.END)):
            comp_id, comp_name = entry.split(":")
            if _id == comp_id:
                self.select_comp_listbox.selection_clear(0, tk.END)
                self.select_comp_listbox.selection_set(index)
                self.select_comp_listbox.activate(index)
                self.show_component()
                break

    def update_component(self):
        """
        Updates the components JSON. values
        """
        comp_data = self.ldr.get_comp_templates()
        selected_comp = self.get_currently_selected_component()
        if selected_comp != None:
            
            
            new_id = self.components_id_entry.entry.get()
            new_name = self.components_name_entry.entry.get()

            warnings = ""

            # Update ID: must check if unique
            if new_id != selected_comp["id"]:
                if new_id in self.ldr.get_comp_templates().keys():
                    warnings += f"WARNING: The comp id {new_id} already exists. CompIDs must be unique.\n"
                elif len(new_id) == 0:
                    warnings += f"WARNING: ID cannot be empty.\n"
                else:
                    old_id = selected_comp["id"]
                    selected_comp["id"] = new_id
                    del comp_data[old_id]
                    comp_data[new_id] = selected_comp

            if len(new_name) == 0:
                warnings += f"WARNING: Name cannot be empty.\n"
            else:
                selected_comp["name"] = new_name

            if len(warnings) > 0:
                messagebox.showwarning(
                    "Warning",
                    warnings
                )

            # Update the ctype specific attributes
            match selected_comp["ctype"]:
                case "FixedGun":
                    self.update_fixed_gun(selected_comp)
                case "Engine":
                    self.update_engine(selected_comp)
                case "Radar":
                    self.update_radar(selected_comp)
                case "CnC":
                    self.update_cnc(selected_comp)
                case "Radio":
                    self.update_radio(selected_comp)
                case "Arm":
                    self.update_arm(selected_comp)
            
            self.populate_comp_listbox(selected_comp["id"])
            self.select_comp_with_id(selected_comp["id"])

    def update_fixed_gun(self, selected_comp):
        try:
            selected_comp["reload_ticks"] = int(self.fg_reload_ticks_entry.entry.get())
            selected_comp["ammunition"] = int(self.fg_ammo_entry.entry.get())
            selected_comp["min_damage"] = int(self.fg_min_damage_entry.entry.get())
            selected_comp["max_damage"] = int(self.fg_max_damage_entry.entry.get())
            selected_comp["range"] = int(self.fg_wpn_range_entry.entry.get())
        except ValueError as e:
            messagebox.showwarning(
                "Warning",
                str(e)
            )
    def update_engine(self, selected_comp):
        try:
            selected_comp["min_speed"] = float(self.engine_min_speed_entry.entry.get())
            selected_comp["max_speed"] = float(self.engine_max_speed_entry.entry.get())
            selected_comp["max_turnrate"] = float(self.engine_max_turnrate_entry.entry.get())
        except ValueError as e:
            messagebox.showwarning(
                "Warning",
                str(e)
            )
    def update_radar(self, selected_comp):
        try:
            selected_comp["range"] = int(self.radar_range_entry.entry.get())
            selected_comp["level"] = int(self.radar_level_entry.entry.get())
            selected_comp["visarc"] = int(self.radar_visarc_entry.entry.get())
            selected_comp["offset_angle"] = int(self.radar_offset_angle_entry.entry.get())
            selected_comp["resolution"] = int(self.radar_resolution_entry.entry.get())
        except ValueError as e:
            messagebox.showwarning(
                "Warning",
                str(e)
            )
    def update_cnc(self, selected_comp):
        try:
            selected_comp["max_cmds_per_tick"] = int(self.cnc_max_commands_per_tick_entry.entry.get())
        except ValueError as e:
            messagebox.showwarning(
                "Warning",
                str(e)
            )
    def update_radio(self, selected_comp):
        try:
            selected_comp["max_range"] = int(self.radio_max_broadcast_range_entry.entry.get())
        except ValueError as e:
            messagebox.showwarning(
                "Warning",
                str(e)
            )
    def update_arm(self, selected_comp):
        try:
            selected_comp["max_bulk"] = int(self.arm_max_bulk_entry.entry.get())
            selected_comp["max_weight"] = int(self.arm_max_weight_entry.entry.get())
        except ValueError as e:
            messagebox.showwarning(
                "Warning",
                str(e)
            )



    def create_component(self):
        """
        Creates a new component and adds it to the component dictionary.
        """

        comp_data = self.ldr.get_comp_templates()

        comp_id_svar = tk.StringVar()
        comp_ctype_svar = tk.StringVar()
        comp_name_svar = tk.StringVar()

        good = False
        while not good:

            dialog = UINewComponent()
            result = dialog.get_result()

            if result["ctype"] in comp.CTYPES_LIST:
                if len(result["id"]) > 0 and result["id"] not in comp_data.keys():
                    if len(result["name"]) > 0:
                        good = True
                    else:
                        messagebox.showwarning(
                            "Warning", "A comp must have a name. Does not have to be unique."
                        )
                else:
                    messagebox.showwarning(
                        "Warning", "A comp must have a non-empty, unique ID."
                    )
            else:
                messagebox.showwarning(
                    "Warning", "A comp must have a valid ctype."
                )

        comp_attrs = comp.COMP_ATTRS_BY_CTYPE[result["ctype"]]

        for attr, val in comp_attrs:
            result[attr] = val

        comp_data.update({result["id"]: result})
        
        self.populate_comp_listbox()
    

    def delete_components(self):
        """
        Deletes the currently selected component from the JSON and component dictionary.
        """

        component_data = self.ldr.get_comp_templates()

        selected_comp = self.get_currently_selected_component()
        if selected_comp != None:
            del component_data[selected_comp["id"]]
            self.populate_comp_listbox()


    def goto_home(self):
        self.controller.show_frame("home_page")

    def save_to_json(self):
        self.ldr.save_comp_templates()


    

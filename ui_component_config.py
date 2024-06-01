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

        
        # Make Component Widgets
        # self.select_component_combo = uiComboBox(master=self.comp_general_frame)
        # self.select_component_combo.configure(state="readonly")
        
        
        
        
        # self.components_type_combo = uiComboBox(master=self.comp_general_frame)
        # self.components_type_attr1_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr1_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )
        # self.components_type_attr2_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr2_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )
        # self.components_type_attr3_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr3_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )
        # self.components_type_attr4_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr4_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )
        # self.components_type_attr5_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr5_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )
        # self.components_type_attr6_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr6_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )
        # self.components_type_attr7_label = uiLabel(
        #     master=self.comp_general_frame, text=""
        # )
        # self.components_type_attr7_entry = EntryHelp(
        #     master=self.comp_general_frame, text="To be added."
        # )

        # Buttons
        self.components_create_button = uiButton(
            master=self.button_row, command=self.create_component, text="Add Component"
        )
        self.components_create_button.pack(side=tk.LEFT)

        self.components_update_button = uiButton(
            master=self.button_row,
            command=self.update_components_json,
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

        # Place Component Widgets
        
        # self.select_component_combo.grid(
        #     row=1, column=1, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10
        # )
        

        # self.components_type_attr1_label.grid(row=6, column=1, sticky="nsew")
        # self.components_type_attr1_entry.frame.grid(row=6, column=2, sticky="nsew")
        # self.components_type_attr1_entry.entry.config(
        #     validate="key", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_attr2_label.grid(row=7, column=1, sticky="nsew")
        # self.components_type_attr2_entry.frame.grid(row=7, column=2, sticky="nsew")
        # self.components_type_attr2_entry.entry.config(
        #     validate="key", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_attr3_label.grid(row=8, column=1, sticky="nsew")
        # self.components_type_attr3_entry.frame.grid(row=8, column=2, sticky="nsew")
        # self.components_type_attr3_entry.entry.config(
        #     validate="all", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_attr4_label.grid(row=9, column=1, sticky="nsew")
        # self.components_type_attr4_entry.frame.grid(row=9, column=2, sticky="nsew")
        # self.components_type_attr4_entry.entry.config(
        #     validate="all", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_attr5_label.grid(row=10, column=1, sticky="nsew")
        # self.components_type_attr5_entry.frame.grid(row=10, column=2, sticky="nsew")
        # self.components_type_attr5_entry.entry.config(
        #     validate="all", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_attr6_label.grid(row=11, column=1, sticky="nsew")
        # self.components_type_attr6_entry.frame.grid(row=11, column=2, sticky="nsew")
        # self.components_type_attr6_entry.entry.config(
        #     validate="all", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_attr7_label.grid(row=12, column=1, sticky="nsew")
        # self.components_type_attr7_entry.frame.grid(row=12, column=2, sticky="nsew")
        # self.components_type_attr7_entry.entry.config(
        #     validate="all", validatecommand=(self.validate_num, "%P")
        # )
        # self.components_type_combo.grid(row=13, column=1, columnspan=2, sticky="nsew")

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

        comp_ids = sorted(self.ldr.get_comp_ids_of_ctype(_ctype))
        keys = []
        for _id in comp_ids:
            comp = self.ldr.get_comp_template(_id)
            keys.append(f"{_id}:{comp["name"]}")

        # comp_names = sorted(self.ldr.get_comp_names_of_type(_ctype))
        self.select_comp_listbox.delete(0,tk.END)
        self.select_comp_listbox_var.set(keys)

    def show_ctype_attr_frame(self, _ctype):
        
        next_attr_frame = self.current_comp_attribute_frame


        # self.comp_fixed_gun_frame = uiQuietFrame(master=self.main_frame)
        # self.comp_engine_frame = uiQuietFrame(master=self.main_frame)
        # self.comp_radar_frame = uiQuietFrame(master=self.main_frame)
        # self.comp_cnc_frame = uiQuietFrame(master=self.main_frame)
        # self.comp_radio_frame = uiQuietFrame(master=self.main_frame)
        # self.comp_arm_frame = uiQuietFrame(master=self.main_frame)

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
        

    # def init_entry_widgets(self):
    #     """
    #     Gets information from the loader and assigns current values for each setting type.
    #     """
        

    #     # COMPONENT
    #     self.component_data = self.ldr.comp_templates
    #     self.component_ids = self.ldr.get_comp_ids()
    #     self.component_names = self.ldr.get_comp_names()
    #     for i in range(len(self.component_ids)):
    #         self.component_ids[i] = (
    #             self.component_ids[i] + ": " + self.component_names[i]
    #         )
    #     self.component_types = self.ldr.get_comp_types()
    #     self.current_component_data = self.component_data[
    #         self.component_ids[0].split(":")[0]
    #     ]
    #     self.component_type_attr = self.current_component_data.view_keys

    #     self.select_component_combo.configure(values=self.component_ids)
    #     self.select_component_combo.current(0)
    #     self.select_component_combo.bind(
    #         "<<ComboboxSelected>>", self.change_components_entry_widgets
    #     )
    #     self.select_component_combo.bind("<Enter>", self.get_previous_component_combo)

    #     self.show_component_entries(self.current_component_data)

        

    # def get_previous_component_combo(self, event):
    #     self.prev_component_combo = self.select_component_combo.current()

    

    # def change_components_entry_widgets(self, event=None):
    #     """
    #     Gets the correct component data for the currently selected team.
    #     """
    #     self.answer = True

    #     if self.current_component_data.get_data("ctype") == "CnC":
    #         ctype_attributes = self.cnc_keys
    #     elif self.current_component_data.get_data("ctype") == "FixedGun":
    #         ctype_attributes = self.fixed_gun_keys
    #     elif self.current_component_data.get_data("ctype") == "Engine":
    #         ctype_attributes = self.engine_keys
    #     elif self.current_component_data.get_data("ctype") == "Radar":
    #         ctype_attributes = self.radar_keys
    #     elif self.current_component_data.get_data("ctype") == "Radio":
    #         ctype_attributes = self.radio_keys
    #     elif self.current_component_data.get_data("ctype") == "Arm":
    #         ctype_attributes = self.arm_keys

    #     if not (
    #         (
    #             (
    #                 self.components_id_entry.entry.get()
    #                 == self.current_component_data.get_data("id")
    #             )
    #             and (
    #                 self.components_name_entry.entry.get()
    #                 == self.current_component_data.get_data("name")
    #             )
    #             and (
    #                 self.components_type_combo.get()
    #                 == self.current_component_data.get_data("ctype")
    #             )
    #             and (
    #                 self.components_type_attr1_entry.entry.get()
    #                 == str(self.current_component_data.get_data(ctype_attributes[0]))
    #             )
    #             and (
    #                 (len(ctype_attributes) < 2)
    #                 or (
    #                     self.components_type_attr2_entry.entry.get()
    #                     == str(
    #                         self.current_component_data.get_data(ctype_attributes[1])
    #                     )
    #                 )
    #             )
    #             and (
    #                 (len(ctype_attributes) < 3)
    #                 or self.current_component_data.get_data(ctype_attributes[2]) is None
    #                 or (
    #                     self.components_type_attr3_entry.entry.get()
    #                     == str(
    #                         self.current_component_data.get_data(ctype_attributes[2])
    #                     )
    #                 )
    #             )
    #             and (
    #                 (len(ctype_attributes) < 4)
    #                 or (
    #                     self.components_type_attr4_entry.entry.get()
    #                     == str(
    #                         self.current_component_data.get_data(ctype_attributes[3])
    #                     )
    #                 )
    #             )
    #             and (
    #                 (len(ctype_attributes) < 5)
    #                 or (
    #                     self.components_type_attr5_entry.entry.get()
    #                     == str(
    #                         self.current_component_data.get_data(ctype_attributes[4])
    #                     )
    #                 )
    #             )
    #             and (
    #                 (len(ctype_attributes) < 6)
    #                 or (
    #                     self.components_type_attr6_entry.entry.get()
    #                     == str(
    #                         self.current_component_data.get_data(ctype_attributes[5])
    #                     )
    #                 )
    #             )
    #             and (
    #                 (len(ctype_attributes) < 7)
    #                 or (
    #                     self.components_type_attr7_entry.entry.get()
    #                     == str(
    #                         self.current_component_data.get_data(ctype_attributes[6])
    #                     )
    #                 )
    #             )
    #         )
    #     ):
    #         self.answer = askyesno(
    #             title="confirmation",
    #             message="""Warning: You have modified Component values and have not Updated.
    #              Your changes will not be saved. Are you sure you would like continue?""",
    #         )

    #     if self.answer is True:
    #         current_component_idx = self.select_component_combo.current()
    #         self.component_type_attr = self.component_data[
    #             self.component_ids[current_component_idx].split(":")[0]
    #         ].view_keys
    #         self.current_component_data = self.component_data[
    #             self.component_ids[current_component_idx].split(":")[0]
    #         ]
    #         self.show_component_entries(self.current_component_data)
    #     else:
    #         self.select_component_combo.current(self.prev_component_combo)

    
    # def component_selected(self):
    #     self.show_component()

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


    # def show_component_entries(self, current_comp):
    #     """
    #     Updates the values in the component entry widgets.
    #     """
    #     self.component_type_attr = current_comp.view_keys
    #     self.components_id_entry.entry.delete(0, tk.END)
    #     self.components_id_entry.entry.insert(0, current_comp.get_data("id"))
    #     self.components_name_entry.entry.delete(0, tk.END)
    #     self.components_name_entry.entry.insert(
    #         0,
    #         current_comp.get_data("name"),
    #     )
    #     self.components_type_combo.configure(values=self.component_types)
    #     self.components_type_combo.set(current_comp.get_data("ctype"))
    #     self.components_type_label.config(text=current_comp.get_data("ctype"))
    #     self.components_type_attr1_entry.entry.configure(state="normal")
    #     self.components_type_attr2_entry.entry.configure(state="normal")
    #     self.components_type_attr3_entry.entry.configure(state="normal")
    #     self.components_type_attr4_entry.entry.configure(state="normal")
    #     self.components_type_attr5_entry.entry.configure(state="normal")
    #     self.components_type_attr6_entry.entry.configure(state="normal")
    #     self.components_type_attr7_entry.entry.configure(state="normal")
    #     self.components_type_attr1_entry.help_button.configure(state="normal")
    #     self.components_type_attr2_entry.help_button.configure(state="normal")
    #     self.components_type_attr3_entry.help_button.configure(state="normal")
    #     self.components_type_attr4_entry.help_button.configure(state="normal")
    #     self.components_type_attr5_entry.help_button.configure(state="normal")
    #     self.components_type_attr6_entry.help_button.configure(state="normal")
    #     self.components_type_attr7_entry.help_button.configure(state="normal")
    #     self.components_type_attr1_label.config(text="")
    #     self.components_type_attr2_label.config(text="")
    #     self.components_type_attr3_label.config(text="")
    #     self.components_type_attr4_label.config(text="")
    #     self.components_type_attr5_label.config(text="")
    #     self.components_type_attr6_label.config(text="")
    #     self.components_type_attr7_label.config(text="")
    #     self.components_type_attr1_entry.entry.delete(0, tk.END)
    #     self.components_type_attr1_entry.entry.config(
    #         validate="key", validatecommand=(self.validate_num, "%P")
    #     )
    #     self.components_type_attr2_entry.entry.delete(0, tk.END)
    #     self.components_type_attr3_entry.entry.delete(0, tk.END)
    #     self.components_type_attr3_entry.entry.config(
    #         validate="key", validatecommand=(self.validate_num, "%P")
    #     )
    #     self.components_type_attr4_entry.entry.delete(0, tk.END)
    #     self.components_type_attr5_entry.entry.delete(0, tk.END)
    #     self.components_type_attr6_entry.entry.delete(0, tk.END)
    #     self.components_type_attr7_entry.entry.delete(0, tk.END)

    #     if current_comp.get_data("ctype") == "CnC":
    #         self.components_type_attr1_label.config(text=self.component_type_attr[4])
    #         self.components_type_attr1_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[4])
    #         )
    #         self.components_type_attr2_entry.entry.configure(state="readonly")
    #         self.components_type_attr3_entry.entry.configure(state="readonly")
    #         self.components_type_attr4_entry.entry.configure(state="readonly")
    #         self.components_type_attr5_entry.entry.configure(state="readonly")
    #         self.components_type_attr6_entry.entry.configure(state="readonly")
    #         self.components_type_attr7_entry.entry.configure(state="readonly")
    #         self.components_type_attr2_entry.help_button.configure(state="disabled")
    #         self.components_type_attr3_entry.help_button.configure(state="disabled")
    #         self.components_type_attr4_entry.help_button.configure(state="disabled")
    #         self.components_type_attr5_entry.help_button.configure(state="disabled")
    #         self.components_type_attr6_entry.help_button.configure(state="disabled")
    #         self.components_type_attr7_entry.help_button.configure(state="disabled")
    #     elif current_comp.get_data("ctype") == "FixedGun":
    #         self.components_type_attr3_entry.entry.configure(validate="none")
    #         self.components_type_attr1_label.config(text=self.component_type_attr[4])
    #         self.components_type_attr1_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[4])
    #         )
    #         self.components_type_attr2_label.config(text=self.component_type_attr[5])
    #         self.components_type_attr2_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[5])
    #         )
    #         self.components_type_attr3_label.config(text=self.component_type_attr[6])
    #         self.components_type_attr3_entry.entry.insert(
    #             0,
    #             (
    #                 current_comp.get_data(self.component_type_attr[6])
    #                 if current_comp.get_data("reloading") is not False
    #                 else "False"
    #             ),
    #         )
    #         self.components_type_attr3_entry.entry.configure(
    #             state="readonly", validate="none"
    #         )
    #         self.components_type_attr4_label.config(text=self.component_type_attr[7])
    #         self.components_type_attr4_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[7])
    #         )
    #         self.components_type_attr5_label.config(text=self.component_type_attr[8])
    #         self.components_type_attr5_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[8])
    #         )
    #         self.components_type_attr6_label.config(text=self.component_type_attr[9])
    #         self.components_type_attr6_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[9])
    #         )
    #         self.components_type_attr7_label.config(text=self.component_type_attr[10])
    #         self.components_type_attr7_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[10])
    #         )
    #     elif current_comp.get_data("ctype") == "Engine":
    #         self.components_type_attr1_label.config(text=self.component_type_attr[4])
    #         self.components_type_attr1_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[4])
    #         )
    #         self.components_type_attr2_label.config(text=self.component_type_attr[5])
    #         self.components_type_attr2_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[5])
    #         )
    #         self.components_type_attr3_label.config(text=self.component_type_attr[6])
    #         self.components_type_attr3_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[6])
    #         )
    #         self.components_type_attr4_label.config(text=self.component_type_attr[7])
    #         self.components_type_attr4_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[7])
    #         )
    #         self.components_type_attr5_label.config(text=self.component_type_attr[8])
    #         self.components_type_attr5_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[8])
    #         )
    #         self.components_type_attr6_entry.entry.configure(state="readonly")
    #         self.components_type_attr7_entry.entry.configure(state="readonly")
    #         self.components_type_attr6_entry.help_button.configure(state="disabled")
    #         self.components_type_attr7_entry.help_button.configure(state="disabled")
    #     elif current_comp.get_data("ctype") == "Radar":
    #         self.components_type_attr1_entry.entry.configure(validate="none")
    #         self.components_type_attr1_label.config(text=self.component_type_attr[4])
    #         self.components_type_attr1_entry.entry.insert(
    #             0,
    #             (
    #                 current_comp.get_data(self.component_type_attr[4])
    #                 if current_comp.get_data("active") is not False
    #                 else "False"
    #             ),
    #         )
    #         self.components_type_attr1_entry.entry.configure(
    #             state="readonly", validate="none"
    #         )
    #         self.components_type_attr2_label.config(text=self.component_type_attr[5])
    #         self.components_type_attr2_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[5])
    #         )
    #         self.components_type_attr3_label.config(text=self.component_type_attr[6])
    #         self.components_type_attr3_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[6])
    #         )
    #         self.components_type_attr4_label.config(text=self.component_type_attr[7])
    #         self.components_type_attr4_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[7])
    #         )
    #         self.components_type_attr5_label.config(text=self.component_type_attr[8])
    #         self.components_type_attr5_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[8])
    #         )
    #         self.components_type_attr6_label.config(text=self.component_type_attr[9])
    #         self.components_type_attr6_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[9])
    #         )
    #         self.components_type_attr7_entry.entry.configure(state="readonly")
    #         self.components_type_attr7_entry.help_button.configure(state="disabled")
    #     elif current_comp.get_data("ctype") == "Radio":
    #         self.components_type_attr3_entry.entry.configure(validate="none")
    #         self.components_type_attr1_label.config(text="max_range")
    #         self.components_type_attr1_entry.entry.insert(
    #             0, current_comp.get_data("max_range")
    #         )
    #         self.components_type_attr2_label.config(text="cur_range")
    #         self.components_type_attr2_entry.entry.insert(
    #             0, current_comp.get_data("cur_range")
    #         )
    #         self.components_type_attr3_label.config(text="message")
    #         self.components_type_attr3_entry.entry.insert(
    #             0,
    #             (
    #                 current_comp.get_data("message")
    #                 if current_comp.get_data("message") is not None
    #                 else "null"
    #             ),
    #         )
    #         self.components_type_attr3_entry.entry.configure(state="readonly")
    #         self.components_type_attr4_entry.entry.configure(state="readonly")
    #         self.components_type_attr5_entry.entry.configure(state="readonly")
    #         self.components_type_attr6_entry.entry.configure(state="readonly")
    #         self.components_type_attr7_entry.entry.configure(state="readonly")
    #         self.components_type_attr4_entry.help_button.configure(state="disabled")
    #         self.components_type_attr5_entry.help_button.configure(state="disabled")
    #         self.components_type_attr6_entry.help_button.configure(state="disabled")
    #         self.components_type_attr7_entry.help_button.configure(state="disabled")
    #     elif self.current_component_data.get_data("ctype") == "Arm":
    #         self.components_type_attr3_entry.entry.configure(validate="none")
    #         self.components_type_attr1_label.config(text=self.component_type_attr[4])
    #         self.components_type_attr1_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[4])
    #         )
    #         self.components_type_attr2_label.config(text=self.component_type_attr[5])
    #         self.components_type_attr2_entry.entry.insert(
    #             0, current_comp.get_data(self.component_type_attr[5])
    #         )
    #         self.components_type_attr3_label.config(text=self.component_type_attr[6])
    #         self.components_type_attr3_entry.entry.insert(
    #             0,
    #             (
    #                 current_comp.get_data(self.component_type_attr[6])
    #                 if current_comp.get_data(self.component_type_attr[6]) is not None
    #                 else "null"
    #             ),
    #         )
    #         self.components_type_attr3_entry.entry.configure(state="readonly")
    #         self.components_type_attr4_entry.entry.configure(state="readonly")
    #         self.components_type_attr5_entry.entry.configure(state="readonly")
    #         self.components_type_attr6_entry.entry.configure(state="readonly")
    #         self.components_type_attr7_entry.entry.configure(state="readonly")
    #         self.components_type_attr4_entry.help_button.configure(state="disabled")
    #         self.components_type_attr5_entry.help_button.configure(state="disabled")
    #         self.components_type_attr6_entry.help_button.configure(state="disabled")
    #         self.components_type_attr7_entry.help_button.configure(state="disabled")
    #     self.comp_general_frame.update_idletasks()

    

    def update_components_json(self):
        """
        Updates the components JSON. values
        """
        selected_comp = self.get_currently_selected_component()
        if selected_comp != None:
            
            # Update name
            selected_comp["name"] = self.components_name_entry.entry.get()
            
            # Update ID: must check if unique
            comp_id = self.components_id_entry.entry.get()
            if comp_id != selected_comp["id"]:
                if comp_id not in self.ldr.get_comp_templates().keys():
                    selected_comp["id"] = comp_id
                else:
                    showwarning(
                        title="Warning",
                        message=f"The comp id {comp_id} already exists. CompIDs must be unique."
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
            

    def update_fixed_gun(self, selected_comp):
        try:
            selected_comp["reload_ticks"] = int(self.fg_reload_ticks_entry.entry.get())
            selected_comp["ammunition"] = int(self.fg_ammo_entry.entry.get())
            selected_comp["min_damage"] = int(self.fg_min_damage_entry.entry.get())
            selected_comp["max_damage"] = int(self.fg_max_damage_entry.entry.get())
            selected_comp["range"] = int(self.fg_wpn_range_entry.entry.get())
        except ValueError as e:
            print(e)
    def update_engine(self, selected_comp):
        try:
            selected_comp["min_speed"] = float(self.engine_min_speed_entry.entry.get())
            selected_comp["max_speed"] = float(self.engine_max_speed_entry.entry.get())
            selected_comp["max_turnrate"] = float(self.engine_max_turnrate_entry.entry.get())
        except ValueError as e:
            print(e)
    def update_radar(self, selected_comp):
        try:
            selected_comp["range"] = int(self.radar_range_entry.entry.get())
            selected_comp["level"] = int(self.radar_level_entry.entry.get())
            selected_comp["visarc"] = int(self.radar_visarc_entry.entry.get())
            selected_comp["offset_angle"] = int(self.radar_offset_angle_entry.entry.get())
            selected_comp["resolution"] = int(self.radar_resolution_entry.entry.get())
        except ValueError as e:
            print(e)
    def update_cnc(self, selected_comp):
        try:
            selected_comp["max_cmds_per_tick"] = int(self.cnc_max_commands_per_tick_entry.entry.get())
        except ValueError as e:
            print(e)
    def update_radio(self, selected_comp):
        try:
            selected_comp["max_range"] = int(self.radio_max_broadcast_range_entry.entry.get())
        except ValueError as e:
            print(e)
    def update_arm(self, selected_comp):
        try:
            selected_comp["max_bulk"] = int(self.arm_max_bulk_entry.entry.get())
            selected_comp["max_weight"] = int(self.arm_max_weight_entry.entry.get())
        except ValueError as e:
            print(e)


    

        # if (
        #     self.components_id_entry.entry.get() in self.component_data.keys()
        #     and self.components_id_entry.entry.get()
        #     != self.select_component_combo.get().split(":")[0]
        # ):
        #     showwarning(
        #         title="Warning",
        #         message="The ID you are trying to use is already in use by another component. Please use another ID.",
        #     )
        # else:
        #     if (
        #         self.components_id_entry.entry.get() != ""
        #         and self.components_name_entry.entry.get() != ""
        #         and self.components_type_attr1_entry.entry.get() != ""
        #     ):
        #         self.current_component_data.setData(
        #             "id", self.components_id_entry.entry.get()
        #         )
        #         self.current_component_data.setData(
        #             "name", self.components_name_entry.entry.get()
        #         )
        #         self.current_component_data.setData(
        #             "ctype", self.components_type_combo.get()
        #         )
        #         if self.current_component_data.get_data("ctype") == "CnC":
        #             self.current_component_data.setData(
        #                 "max_cmds_per_tick",
        #                 int(self.components_type_attr1_entry.entry.get()),
        #             )
        #         if self.current_component_data.get_data("ctype") == "FixedGun":
        #             self.current_component_data.setData(
        #                 "reload_ticks",
        #                 int(self.components_type_attr1_entry.entry.get()),
        #             )
        #             self.current_component_data.setData(
        #                 "reload_ticks_remaining",
        #                 int(self.components_type_attr2_entry.entry.get()),
        #             )
        #             self.current_component_data.setData(
        #                 "reloading",
        #                 (
        #                     self.components_type_attr3_entry.entry.get()
        #                     if self.components_type_attr3_entry.entry.get() != "False"
        #                     else False
        #                 ),
        #             )
        #             self.current_component_data.setData(
        #                 "ammunition", int(self.components_type_attr4_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "min_damage", int(self.components_type_attr5_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "max_damage", int(self.components_type_attr6_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "range", int(self.components_type_attr7_entry.entry.get())
        #             )
        #         if self.current_component_data.get_data("ctype") == "Engine":
        #             self.current_component_data.setData(
        #                 "min_speed", float(self.components_type_attr1_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "max_speed", float(self.components_type_attr2_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "cur_speed", float(self.components_type_attr3_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "max_turnrate",
        #                 float(self.components_type_attr4_entry.entry.get()),
        #             )
        #             self.current_component_data.setData(
        #                 "cur_turnrate",
        #                 float(self.components_type_attr5_entry.entry.get()),
        #             )
        #         if self.current_component_data.get_data("ctype") == "Radar":
        #             self.current_component_data.setData(
        #                 "active",
        #                 (
        #                     self.components_type_attr1_entry.entry.get()
        #                     if self.components_type_attr1_entry.entry.get() != "False"
        #                     else False
        #                 ),
        #             )
        #             self.current_component_data.setData(
        #                 "range", int(self.components_type_attr2_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "level", int(self.components_type_attr3_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "visarc", int(self.components_type_attr4_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "offset_angle",
        #                 int(self.components_type_attr5_entry.entry.get()),
        #             )
        #             self.current_component_data.setData(
        #                 "resolution", int(self.components_type_attr6_entry.entry.get())
        #             )
        #         if self.current_component_data.get_data("ctype") == "Radio":
        #             self.current_component_data.setData(
        #                 "max_range", int(self.components_type_attr1_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "cur_range", int(self.components_type_attr2_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "message",
        #                 (
        #                     self.components_type_attr3_entry.entry.get()
        #                     if self.components_type_attr3_entry.entry.get() != ""
        #                     else None
        #                 ),
        #             )
        #         if self.current_component_data.get_data("ctype") == "Arm":
        #             self.current_component_data.setData(
        #                 "max_weight", int(self.components_type_attr1_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "max_bulk", int(self.components_type_attr2_entry.entry.get())
        #             )
        #             self.current_component_data.setData(
        #                 "item",
        #                 (
        #                     self.components_type_attr3_entry.entry.get()
        #                     if self.components_type_attr3_entry.entry.get() != "null"
        #                     else None
        #                 ),
        #             )

        #         with open("settings/components.json", "r") as f:
        #             component_json = json.load(f)

        #         if (
        #             self.current_component_data.get_data("id")
        #             != self.select_component_combo.get().split(":")[0]
        #         ):
        #             if (
        #                 self.select_component_combo.get().split(":")[0]
        #                 in component_json
        #             ):
        #                 component_json.pop(
        #                     self.select_component_combo.get().split(":")[0]
        #                 )
        #             if (
        #                 self.select_component_combo.get().split(":")[0]
        #                 in self.component_data
        #             ):
        #                 self.component_data.pop(
        #                     self.select_component_combo.get().split(":")[0]
        #                 )
        #             self.component_ids.pop(self.select_component_combo.current())
        #             self.component_ids.append(
        #                 self.current_component_data.get_data("id")
        #                 + ": "
        #                 + self.current_component_data.get_data("name")
        #             )
        #             self.select_component_combo.configure(values=self.component_ids)
        #             self.select_component_combo.current(len(self.component_ids) - 1)

        #         component_json[self.current_component_data.get_data("id")] = (
        #             self.current_component_data.getSelfView()
        #         )
        #         f.close()

        #         self.component_data[self.current_component_data.get_data("id")] = (
        #             self.current_component_data
        #         )

        #         if self.select_component_combo.get().split(":")[1] != "" or (
        #             self.current_component_data.get_data("name")
        #             != component_json[self.current_component_data.get_data("id")][
        #                 "name"
        #             ]
        #         ):
        #             self.component_ids.pop(self.select_component_combo.current())
        #             self.component_ids.append(
        #                 self.current_component_data.get_data("id")
        #                 + ": "
        #                 + self.current_component_data.get_data("name")
        #             )
        #             self.select_component_combo.configure(values=self.component_ids)
        #             self.select_component_combo.current(len(self.component_ids) - 1)
        #         if self.current_component_data.get_data("name") != self.component_data[
        #             self.select_component_combo.get().split(":")[0]
        #         ].get_data("name"):
        #             comp_idx = self.select_component_combo.current()
        #             self.current_comp_ids[comp_idx] = ": ".join(
        #                 [
        #                     self.current_comp_ids[comp_idx].split(":")[0],
        #                     self.current_component_data.get_data("name"),
        #                 ]
        #             )
        #             self.select_component_combo.configure(values=self.component_ids)
        #             self.select_component_combo.current(len(self.component_ids) - 1)
        #         if (
        #             "slot_id"
        #             in component_json[self.current_component_data.get_data("id")].keys()
        #         ):
        #             component_json[self.current_component_data.get_data("id")].pop(
        #                 "slot_id"
        #             )
        #         with open("settings/components.json", "w") as f:
        #             json.dump(component_json, f, indent=4)
        #         f.close()

    

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

        # comp_entry = f"{result["id"]}:{result["name"]}"
        
        self.populate_comp_listbox()

        # self.component_id = askstring(
        #     "Component ID", "Please enter an ID for the new component."
        # )
        # while (
        #     len(self.component_id) == 0
        #     or self.component_id in self.component_data.keys()
        # ):
        #     if len(self.component_id) == 0:
        #         messagebox.showwarning(
        #             "Warning", "Please enter an ID for the new component"
        #         )
        #     else:
        #         messagebox.showwarning(
        #             "Warning", "This ID already exists, please enter a new ID."
        #         )
        #     self.component_id = askstring(
        #         "Component ID", "Please enter an ID for the new component."
        #     )
        # if len(self.component_id) != 0:
        #     self.component_ids.append(self.component_id + ": ")
        #     self.select_component_combo.configure(values=self.component_ids)
        #     self.select_component_combo.current(len(self.component_ids) - 1)
        #     self.new_dict = {"id": self.component_id, "name": "", "ctype": ""}

        #     if self.components_type_combo.get() == "CnC":
        #         self.new_dict["ctype"] = "CnC"
        #         for key in self.cnc_keys:
        #             self.new_dict[key] = ""
        #     elif self.components_type_combo.get() == "FixedGun":
        #         self.new_dict["ctype"] = "FixedGun"
        #         for key in self.fixed_gun_keys:
        #             self.new_dict[key] = ""
        #         self.new_dict["reloading"] = False
        #     elif self.components_type_combo.get() == "Engine":
        #         self.new_dict["ctype"] = "Engine"
        #         for key in self.engine_keys:
        #             self.new_dict[key] = ""
        #     elif self.components_type_combo.get() == "Radar":
        #         self.new_dict["ctype"] = "Radar"
        #         for key in self.radar_keys:
        #             self.new_dict[key] = ""
        #         self.new_dict["active"] = False
        #     elif self.components_type_combo.get() == "Radio":
        #         self.new_dict["ctype"] = "Radio"
        #         for key in self.radio_keys:
        #             self.new_dict[key] = ""
        #     elif self.components_type_combo.get() == "Arm":
        #         self.new_dict["ctype"] = "Arm"
        #         for key in self.arm_keys:
        #             self.new_dict[key] = ""

        #     self.current_component_data = comp.Comp(self.new_dict)

        #     self.component_data[self.component_id] = self.current_component_data
        #     self.show_component_entries(self.current_component_data)

    

    def delete_components(self):
        """
        Deletes the currently selected component from the JSON and component dictionary.
        """

        component_data = self.ldr.get_comp_templates()

        selected_comp = self.get_currently_selected_component()
        if selected_comp != None:
            del component_data[selected_comp["id"]]
            self.populate_comp_listbox()

        # if self.select_component_combo.get().split(":")[0] in self.component_data:
        #     self.component_data.pop(self.select_component_combo.get().split(":")[0])

        #     with open("settings/components.json", "r") as f:
        #         component_json = json.load(f)
        #         component_json.pop(self.select_component_combo.get().split(":")[0])
        #     f.close()
        #     with open("settings/components.json", "w") as f:
        #         json.dump(component_json, f, indent=4)
        #     f.close()
        #     self.component_ids.pop(self.select_component_combo.current())
        #     self.select_component_combo.configure(values=self.component_ids)
        #     self.select_component_combo.current(len(self.component_ids) - 1)
        #     self.change_components_entry_widgets()

    def goto_home(self):
        self.controller.show_frame("home_page")

    def save_to_json(self):
        self.ldr.save_comp_templates()


    
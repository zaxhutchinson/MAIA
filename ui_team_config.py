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
        self.team_data = self.ldr.copy_all_team_templates()

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
        # Make main frames

        self.main_frame = uiQuietFrame(master=self)
        self.team_selection_column = uiLabelFrame(master=self.main_frame,text="Teams")
        self.teams_column = uiLabelFrame(master=self.main_frame, text="Team Info")
        self.agents_column = uiLabelFrame(master=self.main_frame, text="Agent Info")
        self.button_row = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Team Config")
        self.validate_num = self.main_frame.register(self.validate_number_entry)

        


        # Place frames
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.team_selection_column.pack(side=tk.LEFT, fill="y")
        self.teams_column.pack(side=tk.LEFT,fill="y")
        self.agents_column.pack(side=tk.LEFT,fill="y")
        

        # Team Selection Widgets
        self.select_team_listbox_var = tk.StringVar()
        self.select_team_listbox = uiListBox(master=self.team_selection_column, listvariable=self.select_team_listbox_var, selectmode='browse')
        self.select_team_listbox.pack(side=tk.LEFT,fill=tk.BOTH)

        # Team Info Widgets
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
        self.agent_list_label = uiLabel(master=self.teams_column, text="Agents")
        self.agent_listbox_var = tk.StringVar()
        self.agent_listbox = uiListBox(master=self.teams_column, listvariable=self.agent_listbox_var, selectmode='browse')
        self.add_agent_button = uiButton(master=self.teams_column, command=self.add_agent, text="Add Agent")
        self.del_agent_button = uiCarefulButton(master=self.teams_column, command=self.del_agent, text="Delete Agent")
        self.update_agent_button = uiButton(master=self.teams_column, command=self.update_agent, text="Update Agent")

        self.select_team_listbox.bind(
            "<<ListboxSelect>>", self.cmd_new_team_selection
        )
        self.agent_listbox.bind(
            "<<ListboxSelect>>", self.cmd_show_agent
        )

        self.team_size_label.grid(row=0, column=0, sticky="ew")
        self.team_size_entry.frame.grid(row=0, column=1, sticky="ew")
        self.team_name_label.grid(row=1, column=0, sticky="ew")
        self.team_name_entry.frame.grid(row=1, column=1, sticky="ew")
        self.agent_list_label.grid(row=2,column=0,columnspan=2,sticky="ew")
        self.agent_listbox.grid(row=3,column=0,columnspan=2,sticky="ew")
        self.add_agent_button.grid(row=4,column=0,columnspan=2,sticky="ew")
        self.update_agent_button.grid(row=5,column=0,columnspan=2,sticky="ew")
        self.del_agent_button.grid(row=6,column=0,columnspan=2,sticky="ew")

        # Agent Info Widgets
        self.callsign_label = uiLabel(master=self.agents_column, text="Callsign:")
        self.callsign_entry = EntryHelp(master=self.agents_column, text="To be added.")
        self.squad_label = uiLabel(master=self.agents_column, text="Squad:")
        self.squad_entry = EntryHelp(master=self.agents_column, text="To be added.")
        self.agent_object_label = uiLabel(master=self.agents_column, text="Object:")
        self.agent_object_entry = EntryHelp(
            master=self.agents_column, text="To be added."
        )
        self.ai_file_label = uiLabel(master=self.agents_column, text="AI File:")
        self.ai_file_entry = EntryHelp(master=self.agents_column, text="To be added.")
        
        self.callsign_label.grid(row=1, column=1, sticky="ew")
        self.callsign_entry.frame.grid(row=1, column=2, sticky="ew")
        self.squad_label.grid(row=2, column=1, sticky="ew")
        self.squad_entry.frame.grid(row=2, column=2, sticky="ew")
        self.agent_object_label.grid(row=3, column=1, sticky="ew")
        self.agent_object_entry.frame.grid(row=3, column=2, sticky="ew")
        self.ai_file_label.grid(row=4, column=1, sticky="ew")
        self.ai_file_entry.frame.grid(row=4, column=2, sticky="ew")
        
        
        # Team Buttons
        
        self.teams_create_button = uiButton(
            master=self.button_row, command=self.create_team, text="Add Team"
        )
        self.teams_create_button.pack(side=tk.LEFT)
        self.teams_update_button = uiButton(
            master=self.button_row, command=self.update_team, text="Update Team"
        )
        self.teams_update_button.pack(side=tk.LEFT)
        self.teams_delete_button = uiCarefulButton(
            master=self.button_row, command=self.delete_team, text="Delete Team"
        )
        self.teams_delete_button.pack(side=tk.LEFT)



        # High-level Buttons
        self.home_button = uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiCarefulButton(
            master=self.button_row, command=self.save_to_json, text="Save Teams to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)
        

        self.populate_team_listbox()

    def populate_team_listbox(self):
        """
        Gets information from the loader and assigns current values for each setting type.
        """
        team_names = sorted(self.get_team_names())
        self.select_team_listbox.delete(0,tk.END)
        self.select_team_listbox_var.set(team_names)
        #self.current_team_data = self.team_data[team_names[0]]
        
        

        

        # self.select_team_listbox.configure(values=self.team_names)

        
        # self.select_team_listbox.bind("<Enter>", self.get_previous_team_combo)
        # self.show_team_entry(self.current_team_data)

    

        



    def get_previous_team_combo(self, event):
        pass
        # self.prev_team_combo = self.select_team_listbox.current()

    def cmd_new_team_selection(self, event=None):
        """
        Gets the correct team data for the currently selected team.
        """
        self.show_team_entry()
        
        

        # DISABLED CHECKING IF TEAM HAS BEEN ALTERED. NOT SURE IF WE
        #   NEED THIS. Current approach is to update the local copy
        #   of the team_data. And only save back to json on an actual
        #   "save".


        # # the answer variable defaults to true
        # self.answer = True
        # self.get_focused_entry()
        # # if any of the team entry values differ from their starting values,
        # # the user is warned that they could be overwritten
        # if not (
        #     (
        #         (self.team_name_entry.entry.get() == self.current_team_data["name"])
        #         and (
        #             self.team_size_entry.entry.get()
        #             == str(self.current_team_data["size"])
        #         )
        #         and (
        #             self.callsign_entry.entry.get()
        #             == self.current_team_data["agent_defs"][0]["callsign"]
        #         )
        #         and (
        #             self.squad_entry.entry.get()
        #             == self.current_team_data["agent_defs"][0]["squad"]
        #         )
        #         and (
        #             self.agent_object_entry.entry.get()
        #             == self.current_team_data["agent_defs"][0]["object"]
        #         )
        #         and (
        #             self.ai_file_entry.entry.get()
        #             == self.current_team_data["agent_defs"][0]["AI_file"]
        #         )
        #     )
        # ):
        #     self.answer = askyesno(
        #         title="confirmation",
        #         message="""Warning: You have modified Team values and have not Updated.
        #           Your changes will not be saved. Are you sure you would like continue?""",
        #     )

        # # the current team is successfully changed if the user made no changes,
        # # or if the user confirms they are fine with their changes being overwritten
        # if self.answer:
        #     # currentTeamIdx = self.selectTeamCombo.current()
        #     self.current_team_data = self.team_data[self.select_team_listbox.get()]
        #     self.show_team_entry(self.current_team_data)
        # else:
        #     self.select_team_listbox.current(self.prev_team_combo)

    

    def show_team_entry(self):
        """
        Updates the values stored in the team entry widgets.
        """
        current_team = self.get_currently_selected_team()
        if current_team != None:

            self.team_name_entry.entry.delete(0, tk.END)
            self.team_name_entry.entry.insert(0, current_team["name"])
            self.team_size_entry.entry.delete(0, tk.END)
            self.team_size_entry.entry.insert(0, current_team["size"])
            
            self.agent_listbox.delete(0,tk.END)
            self.clear_agent_info()

            agent_defs = current_team["agent_defs"]
            agent_callsigns = []
            for agent in agent_defs:
                agent_callsigns.append(agent["callsign"])    
            self.agent_listbox_var.set(agent_callsigns)
    
    def cmd_show_agent(self, event=None):
        self.show_agent_entry()

    def clear_agent_info(self):
        
        self.callsign_entry.entry.delete(0, tk.END)
        self.squad_entry.entry.delete(0, tk.END)
        self.agent_object_entry.entry.delete(0, tk.END)
        self.ai_file_entry.entry.delete(0, tk.END)

    def show_agent_entry(self):
        # agent_selection = self.agent_listbox.curselection()[0]
        team_name = self.team_name_entry.entry.get()
        current_team = self.get_currently_selected_team()
        if current_team != None:
            self.clear_agent_info()
            index = self.agent_listbox.curselection()
            if len(index) == 1:
                index = index[0]
                self.callsign_entry.entry.insert(
                    0, current_team["agent_defs"][index]["callsign"]
                )
                self.squad_entry.entry.insert(0, current_team["agent_defs"][index]["squad"])
                self.agent_object_entry.entry.insert(0, current_team["agent_defs"][index]["object"])
                self.ai_file_entry.entry.insert(0, current_team["agent_defs"][index]["AI_file"])

    ### CREATE NEW ###
    def create_team(self):
        """
        Creates a new team and adds it to the team dictionary.
        """
        
        good_name = False
        while not good_name:
            team_id = askstring("Team ID", "Please enter an ID for the new team.")
            if len(team_id) == 0:
                messagebox.showwarning(
                    "Warning", "You must enter a team ID to continue"
                )
            elif team_id in self.team_data.keys():
                messagebox.showwarning(
                    "Warning", "This ID already exists, please enter a new ID."
                )
            else:
                good_name = True
            

            
        self.select_team_listbox.insert(tk.END, team_id)
        
        new_team_data = {
            "size": "0",
            "name": team_id,
            "agent_defs": [],
        }
        self.team_data.update({team_id: self.current_team_data})
        
        index = self.select_team_listbox.size()-1
        self.select_team_listbox.selection_clear(0,tk.END)
        self.select_team_listbox.selection_set(index)
        self.select_team_listbox.activate(index)
        self.cmd_new_team_selection()

    ### UPDATE JSON FILES###
    def update_team(self):
        """
        Updates the teams JSON values.
        """
        current_team = self.get_currently_selected_team()
        if current_team != None:
            new_name = self.team_name_entry.entry.get()
            if new_name != current_team["name"]:
                if new_name in self.team_data.keys():
                    showwarning(
                        title="Warning",
                        message=f"{new_name} is in use by another team. Please use another name.",
                    )
                old_name = current_team["name"]
                current_team["name"] = new_name
                del self.team_data[old_name]
                self.team_data[new_name]=current_team

                self.populate_team_listbox()


        # if (
        #     self.team_name_entry.entry.get() in self.team_data.keys()
        #     and self.team_name_entry.entry.get() != self.select_team_listbox.get()
        # ):
            
        # else:
        #     if (
        #         self.team_size_entry.entry.get() != ""
        #         and self.callsign_entry.entry.get() != ""
        #         and self.team_name_entry.entry.get() != ""
        #         and self.squad_entry.entry.get() != ""
        #         and self.agent_object_entry.entry.get() != ""
        #         and self.ai_file_entry.entry.get() != ""
        #     ):
        #         self.current_team_data["size"] = int(self.team_size_entry.entry.get())
        #         self.current_team_data["agent_defs"][0][
        #             "callsign"
        #         ] = self.callsign_entry.entry.get()
        #         self.current_team_data["name"] = self.team_name_entry.entry.get()
        #         self.current_team_data["agent_defs"][0][
        #             "squad"
        #         ] = self.squad_entry.entry.get()
        #         self.current_team_data["agent_defs"][0][
        #             "object"
        #         ] = self.agent_object_entry.entry.get()
        #         self.current_team_data["agent_defs"][0][
        #             "AI_file"
        #         ] = self.ai_file_entry.entry.get()

        #         self.team_data.update(
        #             {self.current_team_data["name"]: self.current_team_data}
        #         )

        #         self.teams_json = json.dumps(self.team_data, indent=4)

        #         with open("settings/teams.json", "r") as f:
        #             team_json = json.load(f)

        #         if self.current_team_data["name"] != self.select_team_listbox.get():
        #             if self.select_team_listbox.get() in team_json:
        #                 team_json.pop(self.select_team_listbox.get())
        #             if self.select_team_listbox.get() in self.team_data:
        #                 self.team_data.pop(self.select_team_listbox.get())
        #             self.team_names.pop(self.select_team_listbox.current())
        #             self.team_names.append(self.current_team_data["name"])
        #             self.select_team_listbox.config(values=self.team_names)
        #             self.select_team_listbox.current(len(self.team_names) - 1)

        #         team_json[self.current_team_data["name"]] = self.current_team_data

        #         self.team_data[self.current_team_data["name"]] = self.current_team_data

        #         f.close()

        #         with open("settings/teams.json", "w") as f:
        #             json.dump(team_json, f, indent=4)
        #         f.close()

    
    ### DELETE ###

    def delete_team(self):
        """
        Deletes the currently selected team from the JSON and team dictionary.
        """
        current_team = self.get_currently_selected_team()
        if current_team != None:
            del self.team_data[current_team["name"]]
            self.populate_team_listbox()
    

    def add_agent(self, event=None):
        current_team = self.get_currently_selected_team()
        if current_team != None:
            cur_size_of_team = len(current_team["agent_defs"])
            cur_size_of_team = int(cur_size_of_team)
            new_agent = {}
            new_agent["callsign"]= f"New Agent {cur_size_of_team}"
            new_agent["squad"]="Missing"
            new_agent["object"]="Missing"
            new_agent["AI_file"]="Missing"
            current_team["agent_defs"].append(new_agent)
            self.agent_listbox.insert(tk.END,new_agent["callsign"])
            self.agent_listbox.selection_clear(0,tk.END)
            self.agent_listbox.selection_set(self.agent_listbox.size()-1)
            self.agent_listbox.activate(self.agent_listbox.size()-1)
            self.show_agent_entry()

    def del_agent(self, event=None):
        current_team = self.get_currently_selected_team()
        if current_team != None:
            agent_index = self.agent_listbox.curselection()
            if len(agent_index)==1:
                self.agent_listbox.delete(agent_index[0])
                del current_team["agent_defs"][agent_index[0]]
                self.agent_listbox.selection_clear(0,tk.END)
                self.show_agent_entry()

    def update_agent(self, event=None):
        current_team = self.get_currently_selected_team()
        if current_team != None:
            agent_index = self.agent_listbox.curselection()
            agent = current_team["agent_defs"][agent_index[0]]
            if len(agent_index)==1:
                callsign = self.callsign_entry.entry.get()
                squad = self.squad_entry.entry.get()
                object_name = self.agent_object_entry.entry.get()
                ai_file = self.ai_file_entry.entry.get()
                if len(callsign)==0 or len(squad)==0 or len(object_name)==0 or len(ai_file)==0:
                    messagebox.showwarning(
                        "Warning", "Cannot have blank agent fields."
                    )
                else:
                    agent["callsign"]=callsign
                    agent["squad"]=squad
                    agent["object"]=object_name
                    agent["AI_file"]=ai_file
                    self.agent_listbox.delete(agent_index[0])
                    self.agent_listbox.insert(agent_index[0],callsign)

    def get_currently_selected_team(self):
        team_index = self.select_team_listbox.curselection()
        if len(team_index) == 1:
            team_name = self.select_team_listbox.get(team_index[0])
            return self.team_data[team_name]
        else:
            return None

    def get_team_names(self):
        team_names = []
        for t in self.team_data.values():
            team_names.append(t["name"])
        return team_names


    def save_to_json(self):
        with open("settings/teams.json", "w") as f:
            json.dump(self.team_data, f, indent=4, sort_keys=True)
        f.close()

    def goto_home(self):
        self.controller.show_frame("home_page")

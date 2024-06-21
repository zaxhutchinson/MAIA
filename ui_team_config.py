import tkinter as tk
import ui_widgets as uiw


class UITeamConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=uiw.BGCOLOR)
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
        # Make main frames

        self.main_frame = uiw.uiQuietFrame(master=self)
        self.team_selection_column = uiw.uiLabelFrame(
            master=self.main_frame, text="Teams"
        )
        self.teams_column = uiw.uiLabelFrame(
            master=self.main_frame, text="Team Info"
        )
        self.agents_column = uiw.uiLabelFrame(
            master=self.main_frame, text="Agent Info"
        )
        self.button_row = uiw.uiQuietFrame(master=self.main_frame)
        self.title_label = uiw.uiLabel(
            master=self.main_frame, text="Team Config"
        )
        self.validate_num = self.main_frame.register(
            self.validate_number_entry
        )

        # Place frames
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.team_selection_column.pack(side=tk.LEFT, fill="y")
        self.teams_column.pack(side=tk.LEFT, fill="y")
        self.agents_column.pack(side=tk.LEFT, fill="y")

        # Team Selection Widgets
        self.select_team_listbox_var = tk.StringVar()
        self.select_team_listbox = uiw.uiListBox(
            master=self.team_selection_column,
            listvariable=self.select_team_listbox_var,
            selectmode="browse",
        )
        self.select_team_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Team Info Widgets
        self.team_size_label = uiw.uiLabel(
            master=self.teams_column, text="Size:"
        )
        self.team_size_entry = uiw.EntryHelp(
            master=self.teams_column,
            text=(
                "The team size field represents how many agents you want "
                + "in the selected team."
                " This field takes numeric values only."
            ),
        )
        self.team_size_entry.entry.config(
            validate="all", validatecommand=(self.validate_num, "%P")
        )
        self.team_name_label = uiw.uiLabel(
            master=self.teams_column, text="Name:"
        )
        self.team_name_entry = uiw.EntryHelp(
            master=self.teams_column, text="To be added."
        )
        self.agent_list_label = uiw.uiLabel(
            master=self.teams_column, text="Agents"
        )
        self.agent_listbox_var = tk.StringVar()
        self.agent_listbox = uiw.uiListBox(
            master=self.teams_column,
            listvariable=self.agent_listbox_var,
            selectmode="browse",
        )
        self.add_agent_button = uiw.uiButton(
            master=self.teams_column, command=self.add_agent, text="Add Agent"
        )
        self.del_agent_button = uiw.uiCarefulButton(
            master=self.teams_column,
            command=self.del_agent,
            text="Delete Agent"
        )
        self.update_agent_button = uiw.uiButton(
            master=self.teams_column,
            command=self.update_agent,
            text="Update Agent"
        )

        self.select_team_listbox.bind(
            "<<ListboxSelect>>", self.cmd_new_team_selection
        )
        self.agent_listbox.bind("<<ListboxSelect>>", self.cmd_show_agent)

        self.team_size_label.grid(row=0, column=0, sticky="ew")
        self.team_size_entry.frame.grid(row=0, column=1, sticky="ew")
        self.team_name_label.grid(row=1, column=0, sticky="ew")
        self.team_name_entry.frame.grid(row=1, column=1, sticky="ew")
        self.agent_list_label.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.agent_listbox.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.add_agent_button.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.update_agent_button.grid(
            row=5, column=0, columnspan=2, sticky="ew"
        )
        self.del_agent_button.grid(row=6, column=0, columnspan=2, sticky="ew")

        # Agent Info Widgets
        self.callsign_label = uiw.uiLabel(
            master=self.agents_column, text="Callsign:"
        )
        self.callsign_entry = uiw.EntryHelp(
            master=self.agents_column, text="To be added."
        )
        self.squad_label = uiw.uiLabel(
            master=self.agents_column, text="Squad:"
        )
        self.squad_entry = uiw.EntryHelp(
            master=self.agents_column, text="To be added."
        )
        self.agent_object_label = uiw.uiLabel(
            master=self.agents_column, text="Object:"
        )
        self.agent_object_entry = uiw.EntryHelp(
            master=self.agents_column, text="To be added."
        )
        self.ai_file_label = uiw.uiLabel(
            master=self.agents_column, text="AI File:"
        )
        self.ai_file_entry = uiw.EntryHelp(
            master=self.agents_column, text="To be added."
        )

        self.callsign_label.grid(row=1, column=1, sticky="ew")
        self.callsign_entry.frame.grid(row=1, column=2, sticky="ew")
        self.squad_label.grid(row=2, column=1, sticky="ew")
        self.squad_entry.frame.grid(row=2, column=2, sticky="ew")
        self.agent_object_label.grid(row=3, column=1, sticky="ew")
        self.agent_object_entry.frame.grid(row=3, column=2, sticky="ew")
        self.ai_file_label.grid(row=4, column=1, sticky="ew")
        self.ai_file_entry.frame.grid(row=4, column=2, sticky="ew")

        # Team Buttons

        self.teams_create_button = uiw.uiButton(
            master=self.button_row, command=self.create_team, text="Add Team"
        )
        self.teams_create_button.pack(side=tk.LEFT)
        self.teams_update_button = uiw.uiButton(
            master=self.button_row,
            command=self.update_team,
            text="Update Team"
        )
        self.teams_update_button.pack(side=tk.LEFT)
        self.teams_delete_button = uiw.uiCarefulButton(
            master=self.button_row,
            command=self.delete_team,
            text="Delete Team"
        )
        self.teams_delete_button.pack(side=tk.LEFT)

        # High-level Buttons
        self.home_button = uiw.uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiw.uiCarefulButton(
            master=self.button_row,
            command=self.save_to_json,
            text="Save Teams to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

        self.populate_team_listbox()

    def populate_team_listbox(self):
        """
        Gets information from the loader and assigns current values
        for each setting type.
        """
        team_names = sorted(self.ldr.get_team_names())
        self.select_team_listbox.delete(0, tk.END)
        self.select_team_listbox_var.set(team_names)

    def get_previous_team_combo(self, event):
        pass
        # self.prev_team_combo = self.select_team_listbox.current()

    def cmd_new_team_selection(self, event=None):
        """
        Gets the correct team data for the currently selected team.
        """
        self.show_team_entry()

    def show_team_entry(self):
        """
        Updates the values stored in the team entry widgets.
        """
        current_team = self.get_currently_selected_team()
        if current_team is not None:

            self.team_name_entry.entry.delete(0, tk.END)
            self.team_name_entry.entry.insert(0, current_team["name"])
            self.team_size_entry.entry.delete(0, tk.END)
            self.team_size_entry.entry.insert(0, current_team["size"])

            self.agent_listbox.delete(0, tk.END)
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
        current_team = self.get_currently_selected_team()
        if current_team is not None:
            self.clear_agent_info()
            index = self.agent_listbox.curselection()
            if len(index) == 1:
                index = index[0]
                self.callsign_entry.entry.insert(
                    0, current_team["agent_defs"][index]["callsign"]
                )
                self.squad_entry.entry.insert(
                    0, current_team["agent_defs"][index]["squad"]
                )
                self.agent_object_entry.entry.insert(
                    0, current_team["agent_defs"][index]["object"]
                )
                self.ai_file_entry.entry.insert(
                    0, current_team["agent_defs"][index]["AI_file"]
                )

    # CREATE NEW
    def create_team(self):
        """
        Creates a new team and adds it to the team dictionary.
        """

        team_data = self.ldr.get_team_templates()

        good_name = False
        while not good_name:
            team_id = tk.simpledialog.askstring(
                "New Team ID", "Please enter an ID for the new team."
            )
            if len(team_id) == 0:
                tk.messagebox.showwarning(
                    "Warning", "You must enter a team ID to continue"
                )
            elif team_id in team_data.keys():
                tk.messagebox.showwarning(
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
        team_data.update({team_id: new_team_data})

        index = self.select_team_listbox.size() - 1
        self.select_team_listbox.selection_clear(0, tk.END)
        self.select_team_listbox.selection_set(index)
        self.select_team_listbox.activate(index)
        self.cmd_new_team_selection()

    # UPDATE JSON FILES
    def update_team(self):
        """
        Updates the teams JSON values.
        """
        team_data = self.ldr.get_team_templates()
        current_team = self.get_currently_selected_team()
        if current_team is not None:
            new_name = self.team_name_entry.entry.get()
            if new_name != current_team["name"]:
                if new_name in team_data.keys():
                    tk.simpledialog.showwarning(
                        title="Warning",
                        message=f"{new_name} is in use by another team. "
                        + "Please use another name.",
                    )
                else:
                    old_name = current_team["name"]
                    current_team["name"] = new_name
                    del team_data[old_name]

            team_data[new_name] = current_team
            self.populate_team_listbox()

    # DELETE

    def delete_team(self):
        """
        Deletes the currently selected team from the JSON and team dictionary.
        """
        team_data = self.ldr.get_team_templates()
        current_team = self.get_currently_selected_team()
        if current_team is not None:
            del team_data[current_team["name"]]
            self.populate_team_listbox()

    def add_agent(self, event=None):
        current_team = self.get_currently_selected_team()
        if current_team is not None:
            cur_size_of_team = len(current_team["agent_defs"])
            cur_size_of_team = int(cur_size_of_team)
            new_agent = {}
            new_agent["callsign"] = f"New Agent {cur_size_of_team}"
            new_agent["squad"] = "Missing"
            new_agent["object"] = "Missing"
            new_agent["AI_file"] = "Missing"
            current_team["agent_defs"].append(new_agent)
            self.agent_listbox.insert(tk.END, new_agent["callsign"])
            self.agent_listbox.selection_clear(0, tk.END)
            self.agent_listbox.selection_set(self.agent_listbox.size() - 1)
            self.agent_listbox.activate(self.agent_listbox.size() - 1)
            self.show_agent_entry()

    def del_agent(self, event=None):
        current_team = self.get_currently_selected_team()
        if current_team is not None:
            agent_index = self.agent_listbox.curselection()
            if len(agent_index) == 1:
                self.agent_listbox.delete(agent_index[0])
                del current_team["agent_defs"][agent_index[0]]
                self.agent_listbox.selection_clear(0, tk.END)
                self.show_agent_entry()

    def update_agent(self, event=None):
        current_team = self.get_currently_selected_team()
        if current_team is not None:
            agent_index = self.agent_listbox.curselection()
            agent = current_team["agent_defs"][agent_index[0]]
            if len(agent_index) == 1:
                callsign = self.callsign_entry.entry.get()
                squad = self.squad_entry.entry.get()
                object_name = self.agent_object_entry.entry.get()
                ai_file = self.ai_file_entry.entry.get()
                if (
                    len(callsign) == 0
                    or len(squad) == 0
                    or len(object_name) == 0
                    or len(ai_file) == 0
                ):
                    tk.messagebox.showwarning(
                        "Warning", "Cannot have blank agent fields."
                    )
                else:
                    agent["callsign"] = callsign
                    agent["squad"] = squad
                    agent["object"] = object_name
                    agent["AI_file"] = ai_file
                    self.agent_listbox.delete(agent_index[0])
                    self.agent_listbox.insert(agent_index[0], callsign)

    def get_currently_selected_team(self):
        team_index = self.select_team_listbox.curselection()
        if len(team_index) == 1:
            team_name = self.select_team_listbox.get(team_index[0])
            return self.ldr.get_team_template(team_name)
        else:
            return None

    def save_to_json(self):
        self.ldr.save_team_templates()

    def goto_home(self):
        self.controller.show_frame("home_page")

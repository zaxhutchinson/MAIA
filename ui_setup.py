import tkinter as tk
import queue
import sim
import loader
import ui_sim
import msgs
import zexceptions
import ui_widgets as uiw


class UISetup(tk.Frame):
    def __init__(self, master, controller, logger, ldr):
        """Sets window and frame information and calls function to build UI"""
        tk.Frame.__init__(self, master)
        self.master = master
        self.logger = logger
        self.controller = controller

        # Create the msgr objs
        self.msg_queue = queue.Queue()
        self.imsgr = msgs.IMsgr(self.msg_queue)
        self.omsgr = msgs.OMsgr(self.msg_queue)

        self.ldr = ldr
        self.sim = None #sim.Sim(ldr, self.imsgr)

        # Store selections make via the UI. Only build Sim when
        # 'start match' is clicked.
        self.selected_map = None
        self.team_side_assignments = {}

        self.combat_log = []

        self.build_ui()

        self.UIMap = None

    def reset(self):
        self.sim = None
        self.team_side_assignments.clear()
        self.combat_log.clear()
        self.UIMap = None

    def update_team_names(self):
        """Updates team names"""

        self.teams_list.delete(0, tk.END)
        team_data = self.ldr.get_team_templates()
        for team_id, team in team_data.items():
            entry = f"{team_id}: {team['name']}"
            self.teams_list.insert(tk.END, entry)

    def update_sides_list(self):
        self.sides_list.delete(0, tk.END)
        if self.selected_map is not None:
            for side_id, side in self.selected_map["sides"].items():
                entry = f"{side_id}: {side['name']}"
                self.sides_list.insert(tk.END, entry)

    def update_map_names(self):
        """Updates map names"""
        self.maps_list.delete(0, tk.END)
        map_data = self.ldr.get_map_templates()
        for m in map_data.values():
            entry = f"{m['id']}: {m['name']}"
            self.maps_list.insert(tk.END, entry)

    def update_team_side_assignments_list(self):
        if self.selected_map is not None:
            self.team_assignments_list.delete(0, tk.END)
            team_data = self.ldr.get_team_templates()
            side_data = self.selected_map["sides"]
            for side_id, team_id in self.team_side_assignments.items():
                team_name = team_data[team_id]["name"]
                side_name = side_data[side_id]["name"]
                entry = f"{side_id}:{side_name}->{team_id}:{team_name}"
                self.team_assignments_list.insert(tk.END, entry)

    def select_map(self, event):
        """Selects map for sim

        Located here so that it can be bound to selecting map in build_ui
        """
        cur_selection = self.maps_list.curselection()
        if len(cur_selection) > 0:
            # Reset any selections or previous matches.
            if self.sim is not None:
                self.sim = None
                self.selected_map = None
                self.team_side_assignments = {}

            # Locate the map, copy and give to sim
            map_entry = self.maps_list.get(cur_selection[0])
            map_id, map_name = map_entry.split(":")
            # self.selected_map_id = map_id
            self.selected_map = self.ldr.get_map_template(map_id)

            # Construct the map info string
            map_info = f"NAME:   {self.selected_map['name']}\n"
            map_info += f"DESC:   {self.selected_map['desc']}\n"
            map_info += f"WIDTH:  {self.selected_map['width']}\n"
            map_info += f"HEIGHT: {self.selected_map['height']}\n"

            # Add string to the info text box
            self.map_info_text.delete("1.0", tk.END)
            self.map_info_text.insert(tk.END, map_info)

            self.update_team_names()
            self.update_sides_list()

            self.team_assignments_list.delete(0, tk.END)

    def build_ui(self):
        """Generates the setup UI

        Places map select, places team/side assignments,
        places adv config button, places start button
        """
        # PAGE TITLE
        self.title_label = uiw.uiLabel(master=self, text="CONFIGURATION")
        self.title_label.pack(side=tk.TOP, fill=tk.X)

        #######################################################################
        # SIM UI
        #######################################################################

        self.button_frame = uiw.uiQuietFrame(master=self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.home_button = uiw.uiButton(
            master=self.button_frame,
            command=self.goto_home,
            text="Home"
        )
        self.home_button.pack(side=tk.LEFT)

        self.start_button = uiw.uiButton(
            master=self.button_frame,
            command=self.build_and_run_sim,
            text="Start Match",
        )  # Start Game Button
        self.start_button.pack(
            side=tk.LEFT
        )

        #######################################################################
        # MAP UI
        #######################################################################
        self.maps_frame = uiw.uiQuietFrame(master=self)  # map section
        self.maps_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.maps_label = uiw.uiLabel(master=self.maps_frame, text="MAPS")
        self.maps_label.pack(side=tk.TOP, fill=tk.X)

        self.maps_list = uiw.uiListBox(
            self.maps_frame
        )  # this is the box that says Map 1 maps_list
        self.maps_list.config(width=32)
        self.maps_list.pack(side=tk.TOP, fill=tk.BOTH)

        self.maps_list.bind(
            "<<ListboxSelect>>", self.select_map
        )  # this calls select_map(self, whateverMapIsSelectedInTheBox)

        self.map_info_label = uiw.uiLabel(
            master=self.maps_frame, text="Map Information"
        )
        self.map_info_label.pack(side=tk.TOP, fill=tk.X)

        # info on selected frame
        self.map_info_text = uiw.uiScrollText(self.maps_frame)
        self.map_info_text.config(width=32)
        self.map_info_text.pack(side=tk.TOP, fill=tk.Y)

        # this function call gets Map 1 (later other maps) into the box
        self.update_map_names()

        #######################################################################
        # TEAM UI
        ######################################################################
        self.team_frame = uiw.uiQuietFrame(
            master=self
        )  # team frame is everything team UI #top line creates frame
        self.team_frame.config(padx=0, pady=0)
        self.team_frame.pack(
            side=tk.TOP, fill=tk.X
        )  # bottom line is frame settings

        self.team_pool_frame = uiw.uiQuietFrame(
            master=self.team_frame
        )  # Left half of team frame
        self.team_pool_frame.config(padx=0, pady=0)
        self.team_pool_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.team_pool_left_frame = uiw.uiQuietFrame(
            master=self.team_pool_frame
        )  # part of pool frame, pool section
        self.team_pool_left_frame.columnconfigure(0, weight=1)
        self.team_pool_left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.team_pool_label = uiw.uiLabel(
            master=self.team_pool_left_frame, text="Team Pool"
        )  # label that says "Team Pool" section of pool left frame
        self.team_pool_label.grid(row=0, column=0, sticky="ew")

        self.teams_list = uiw.uiListBox(self.team_pool_left_frame)
        # self.teams_list.config(width=32)
        self.teams_list.grid(row=1, column=0, sticky="nsew")

        self.add_team_button = uiw.uiButton(
            master=self.team_pool_left_frame,
            text="Assign Team to Side",
            command=self.assign_team_to_side
        )
        self.add_team_button.grid(row=4, column=0, sticky="ew")

        # self.team_pool_right_frame = uiw.uiQuietFrame(
        #     master=self.team_pool_frame
        # )  # pool right frame is the sides section, also part of Pool Frame
        # self.team_pool_right_frame.columnconfigure(0, weight=1)
        # self.team_pool_right_frame.pack(
        #     side=tk.LEFT, fill=tk.X, expand=True
        # )

        self.sides_label = uiw.uiLabel(
            master=self.team_pool_left_frame, text="Sides"
        )
        self.sides_label.grid(row=2, column=0, sticky="ew")

        self.sides_list = uiw.uiListBox(self.team_pool_left_frame)
        # self.sides_list.config(width=32)
        self.sides_list.grid(row=3, column=0, sticky="nsew")

        self.remove_team_button = uiw.uiButton(
            master=self.team_pool_left_frame,
            text="Remove Team from Side",
            command=self.remove_team_side_assignment,
        )
        self.remove_team_button.grid(row=5, column=0, sticky="ew")

        # Assigned is other half of team frame, "Play pool" is teams
        # that are playing
        self.play_pool_frame = uiw.uiQuietFrame(
            master=self.team_frame
        )
        self.play_pool_frame.rowconfigure(0, weight=1)
        self.play_pool_frame.columnconfigure(0, weight=1)
        self.play_pool_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.play_pool_label = uiw.uiLabel(
            master=self.play_pool_frame, text="Assigned Teams"
        )
        self.play_pool_label.grid(row=0, column=0, sticky="ew")

        self.team_assignments_list = uiw.uiListBox(self.play_pool_frame)
        self.team_assignments_list.grid(
            row=1, column=0, sticky="nesw"
        )

        self.update_team_names()

        self.pack(fill=tk.BOTH)

    def assign_team_to_side(self):
        """Adds team/side assignment to sim"""
        team_index = self.teams_list.curselection()
        side_index = self.sides_list.curselection()
        if len(team_index) > 0 and len(side_index) > 0:

            selected_side_entry = self.sides_list.get(side_index)
            selected_team_entry = self.teams_list.get(team_index)

            side_id, side_name = selected_side_entry.split(":")
            team_id, team_name = selected_team_entry.split(":")

            print(side_id, team_id)

            self.team_side_assignments[side_id] = team_id

            # self.sim.add_team_name(side_selection, team_name)
            self.update_team_side_assignments_list()
        else:
            self.logger.error(
                "App::add_team() - No side or team selected."
            )


    def remove_team_side_assignment(self):
        """Removes team/side assignment from sim"""
        team_index = self.team_assignments_list.curselection()
        if len(team_index) > 0:
            entry = self.sides_list.get(team_index)
            side_id = entry.split(":")[0]
            del self.team_side_assignments[side_id]
            self.update_team_side_assignments_list()

    def goto_home(self):
        self.controller.show_frame("home_page")

    def check_build_params(self):
        if self.selected_map is not None:
            num_sides = len(self.selected_map["sides"])
            if num_sides == len(self.team_side_assignments):
                return True
            else:
                return False
        else:
            return False

    def build_and_run_sim(self):
        """Builds and runs sim"""

        if self.check_build_params():
            try:
                self.sim = sim.Sim(
                    self.ldr,
                    self.logger,
                    self.selected_map,
                    self.team_side_assignments,
                    imsgr=self.imsgr
                )
                self.sim.build_sim()
            except zexceptions.BuildException as e:
                tk.messagebox.showinfo(title="Build Exception", message=e)
            else:
                # I DON'T REALLY LIKE THIS CALL BACK TO THE CONTROLLER
                # TO GET THE UI SIM OBJECT.
                self.controller.get_frame("match").build(self.sim)
                self.controller.show_frame("match")

                # tk.messagebox.showinfo(title="Success",message=
                # "Sim build was successful.")    --this line makes a pop up
                # map_width = self.sim.get_map().get_width()
                # map_height = self.sim.get_map().get_height()
                # self.UIMap = ui_sim.UISim(
                #     map_width,
                #     map_height,
                #     self.sim,
                #     self.omsgr,
                #     self.controller,
                #     self,
                #     self.logger,
                # )

            # Reset sim data for another run.
            self.reset()

    def run_advanced_settings(self):
        """Opens advanced config settings"""
        pass
        # self.UIMap = ui_advanced_config.UISettings(self, self.logger)

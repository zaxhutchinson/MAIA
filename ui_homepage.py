import tkinter as tk
import queue
from PIL import ImageTk, Image
import loader
import msgs
import ui_widgets as uiw
import consts


class UIHomepage(tk.Frame):
    def __init__(self, controller, master=None, logger=None):
        """Sets window and frame information and calls function to build UI"""
        tk.Frame.__init__(self, master)
        self.master = master
        self.logger = logger
        self.controller = controller

        # Create the msgr objs
        self.msg_queue = queue.Queue()
        self.imsgr = msgs.IMsgr(self.msg_queue)
        self.omsgr = msgs.OMsgr(self.msg_queue)

        self.ldr = loader.Loader(self.logger)
        # self.sim = sim.Sim(self.imsgr)

        self.build_ui()
        self.UIMap = None

    def build_ui(self):
        """Generates the homepage UI

        Places label, places start game button,
        places adv config button, places about button
        """
        # self.mainFrame = uiQuietFrame(master=self)

        self.maia_image = ImageTk.PhotoImage(Image.open("images/maia.png"))
        self.maia_image_label = uiw.uiLabel(
            master=self, image=self.maia_image
        )  # text="Maine AI Arena")
        self.maia_image_label.pack(side=tk.TOP, fill="x")
        self.maia_text_label = uiw.uiLabel(
            master=self, text="Maine AI Arena", font=("Arial", 24)
        )
        self.maia_text_label.pack(side=tk.TOP, fill="x")

        self.maia_version_label = uiw.uiLabel(
            master=self,
            text=f"Version {consts.VERSION_MAJOR}.{consts.VERSION_MINOR}",
            font=("Arial", 10)
        )
        self.maia_version_label.pack(side=tk.TOP, fill="x")

        self.general_frame = tk.LabelFrame(
            self, text="General", labelanchor="n", font=("Arial", 15)
        )
        self.config_frame = tk.LabelFrame(
            self, text="Config", labelanchor="n", font=("Arial", 15)
        )
        self.match_frame = tk.LabelFrame(
            self, text="Match", labelanchor="n", font=("Arial", 15)
        )
        self.general_frame.pack(side=tk.TOP)
        self.config_frame.pack(side=tk.TOP)
        self.match_frame.pack(side=tk.TOP)

        self.about_button = uiw.uiButton(
            master=self.general_frame,
            text="About MAIA",
            command=self.show_about,
        )
        self.about_button.config(width=20, height=3)
        self.about_button.grid(row=0, column=0, sticky="ew")

        self.config_teams_button = uiw.uiButton(
            master=self.config_frame,
            command=self.show_teams_config,
            text="Team Config",
        )
        self.config_teams_button.config(width=20, height=3)
        self.config_teams_button.grid(row=0, column=0, sticky="ew")

        self.config_component_button = uiw.uiButton(
            master=self.config_frame,
            command=self.show_component_config,
            text="Component Config",
        )
        self.config_component_button.config(width=20, height=3)
        self.config_component_button.grid(row=0, column=1, sticky="ew")

        self.config_object_button = uiw.uiButton(
            master=self.config_frame,
            command=self.show_object_config,
            text="Object Config",
        )
        self.config_object_button.config(width=20, height=3)
        self.config_object_button.grid(row=1, column=0, sticky="ew")

        self.config_item_button = uiw.uiButton(
            master=self.config_frame,
            command=self.show_item_config,
            text="Item Config",
        )
        self.config_item_button.config(width=20, height=3)
        self.config_item_button.grid(row=1, column=1, sticky="ew")

        self.config_map_button = uiw.uiButton(
            master=self.config_frame,
            command=self.show_map_config,
            text="Map Config",
        )
        self.config_map_button.config(width=20, height=3)
        self.config_map_button.grid(row=2, column=0, sticky="ew")

        # self.config_gstate_button = uiw.uiButton(
        #     master=self.config_frame,
        #     command=lambda: self.controller.show_frame("config_gstate"),
        #     text="Goal Config",
        # )
        # self.config_gstate_button.config(width=20, height=3)
        # self.config_gstate_button.grid(row=2, column=1, sticky="we")

        self.start_game_button = uiw.uiButton(
            master=self.match_frame,
            text="Match Setup",
            command=self.show_match,
        )
        self.start_game_button.config(width=20, height=3)
        self.start_game_button.pack(side=tk.TOP)

    def show_map_config(self):
        self.controller.get_frame("config_map").event_generate("<<ShowFrame>>")
        self.controller.show_frame("config_map")

    def show_item_config(self):
        self.controller.show_frame("config_item")

    def show_object_config(self):
        self.controller.show_frame("config_object")

    def show_component_config(self):
        self.controller.show_frame("config_component")

    def show_teams_config(self):
        self.controller.show_frame("config_team")

    def show_about(self):
        self.controller.show_frame("about_page")

    def show_match(self):
        self.controller.show_frame("setup_page")

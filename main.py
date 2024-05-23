import tkinter as tk
import sys
import logging

import ui_setup
import vec2
import math
import zmap
import ui_homepage
import ui_about
import ui_team_config
import ui_object_config
import ui_map_config
import ui_component_config


# Initialize the log files
# LogInit()
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        """Initializes MAIA window

        Instances of home page, about page, and set up page frames are stored in array to be raised as needed
        """
        tk.Tk.__init__(self, *args, **kwargs)

        logger = logging.getLogger("main")
        handler = logging.FileHandler("log/main.log", mode="w")
        formatter = logging.Formatter("%(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.title("MAIA")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        # self.minsize(width=1400, height=700)
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["home_page"] = ui_homepage.UIHomepage(
            master=self.container, controller=self, logger=logger
        )
        self.frames["setup_page"] = ui_setup.UISetup(
            master=self.container, controller=self, logger=logger
        )
        self.frames["about_page"] = ui_about.ui_about(
            master=self.container, controller=self, logger=logger
        )
        self.frames["config_team"] = ui_team_config.UITeamConfig(
            master=self.container, controller=self, logger=logger
        )
        self.frames["config_object"] = ui_object_config.UIObjectConfig(
            master=self.container, controller=self, logger=logger
        )
        self.frames["config_map"] = ui_map_config.UIMapConfig(
            master=self.container, controller=self, logger=logger
        )
        self.frames["config_component"] = ui_component_config.UIComponentConfig(
            master=self.container, controller=self, logger=logger
        )

        # the setup page must be placed first to prevent errors
        self.frames["setup_page"].grid(row=0, column=0, sticky="nsew")
        self.frames["home_page"].grid(row=0, column=0, sticky="nsew")
        self.frames["about_page"].grid(row=0, column=0, sticky="nsew")
        self.frames["config_team"].grid(row=0, column=0, sticky="nsew")
        self.frames["config_object"].grid(row=0, column=0, sticky="nsew")
        self.frames["config_map"].grid(row=0, column=0, sticky="nsew")
        self.frames["config_component"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("home_page")

    def show_frame(self, page_name):
        """Raises frame"""
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    root = App()
    root.mainloop()

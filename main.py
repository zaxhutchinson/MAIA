import tkinter as tk
import sys
import logging

import ui_setup
import vec2
import math
import zmap
import ui_homepage
import ui_about


# Initialize the log files
# LogInit()
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        logger = logging.getLogger("main")
        handler = logging.FileHandler("log/main.log", mode="w")
        formatter = logging.Formatter("%(name)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.title("MAIA")
        self.geometry("1300x600")
        self.minsize(width=1300, height=600)
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["HomePage"] = ui_homepage.UIHomepage(
            master=self.container, controller=self, logger=logger
        )
        self.frames["SetupPage"] = ui_setup.UISetup(
            master=self.container, controller=self, logger=logger
        )
        self.frames["AboutPage"] = ui_about.ui_about(
            master=self.container, controller=self, logger=logger
        )

        # the setup page must be placed first to prevent errors
        self.frames["SetupPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["HomePage"].grid(row=0, column=0, sticky="nsew")
        self.frames["AboutPage"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    root = App()
    root.mainloop()

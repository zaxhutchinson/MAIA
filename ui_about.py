import tkinter as tk
import ui_widgets as uiw


class ui_about(tk.Frame):
    def __init__(self, controller, master=None, logger=None):
        """Sets window and frame information and calls function to build UI"""
        tk.Frame.__init__(self, master)
        self.master = master
        self.logger = logger
        self.controller = controller

        self.build_ui()

        self.UIMap = None

    def build_ui(self):
        """Generates the about page UI

        Sets description text, places description,
        places label, places home button
        """
        desc_text = "MAIA is a platform designed for AI competitions that "
        + "provides a modular 2D simulation environment for which students "
        + "write AI to control competing agents.\n The goal is to give coders "
        + "all the tools necessary so that they can focus primarily on "
        + "analysis of information and decision-making.\n\n MAIA was "
        + "developed by Dr. Zachary Hutchinson during his graduate studies "
        + "at the University of Maine, Orono.\n Version 0.22, the most "
        + "current version of MAIA, was released in October of 2020.\n "
        + "Further documentation, including overviews of the AI scripts, "
        + "can be found in the docs directory."
        desc_text = desc_text.replace("            ", "")

        self.maia_label = uiw.uiLabel(master=self, text="Maine AI Arena")
        self.maia_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.description = uiw.uiTextbox(master=self, width=60)
        self.description.insert(1.0, desc_text)
        self.description.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.description.config(state="disabled")

        self.home_button = uiw.uiButton(
            master=self,
            text="Home",
            command=lambda: self.controller.show_frame("home_page"),
        )
        self.home_button.config(width=400)
        self.home_button.pack(side=tk.TOP, fill="y", expand=True)

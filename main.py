import tkinter as tk
import sys
import logging

import ui_setup
import vec2
import math
import zmap
import ui_homepage
import ui_setup
import aboutPage




    # Initialize the log files
    #LogInit()
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        logger = logging.getLogger('main')
        handler = logging.FileHandler('log/main.log',mode='w')
        formatter = logging.Formatter('%(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH,expand=True,side=tk.TOP)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        # diff in instantiation; can the imputs be reduced?
        self.frames["HomePage"] = ui_homepage.UIHomepage(master=self.container,controller=self,logger=logger)
        self.frames["SetupPage"] = ui_setup.UISetup(master=self.container,controller=self,logger=logger)
        self.frames["AboutPage"] = aboutPage.aboutPage(master=self.container,controller=self,logger=logger)
        
        self.frames["HomePage"].grid(row=0,column=0,sticky="nsew")
        self.frames["SetupPage"].grid(row=0,column=0,sticky="nsew")
        self.frames["AboutPage"].grid(row=0,column=0,sticky="nsew")

        self.show_frame("HomePage")
        
        # self.homepage.pack(side="top", fill="both", expand=True)
        # self.setup.pack_forget()
        # self.about.pack_forget()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    root = App()
    root.mainloop()

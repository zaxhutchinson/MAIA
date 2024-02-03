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
    

        self.container = tk.Frame(self)
        self.container.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        logger = logging.getLogger('main')
        handler = logging.FileHandler('log/main.log',mode='w')
        formatter = logging.Formatter('%(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Start App
        self.homepage = ui_homepage.UIHomepage(master=self, logger=logger,parent=self.container)
        self.setup = ui_setup.UISetup(master=self, logger=logger,parent=self.container)
        self.about = aboutPage.aboutPage(master=self, logger=logger,parent=self.container)
        
        self.homepage.pack(side="top", fill="both", expand=True)
        self.setup.pack_forget()
        self.about.pack_forget()

if __name__ == "__main__":
    root = App()
    root.mainloop()

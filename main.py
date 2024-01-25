import tkinter as tk
import sys
import logging

import ui_setup
import vec2
import math
import zmap
import ui_homepage



if __name__ == "__main__":
    # Initialize the log files
    #LogInit()

    logger = logging.getLogger('main')
    handler = logging.FileHandler('log/main.log',mode='w')
    formatter = logging.Formatter('%(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    

    # Start App
    root = tk.Tk()
    maia_app = ui_homepage.UIHomepage(master=root, logger=logger)
    maia_app.Run()

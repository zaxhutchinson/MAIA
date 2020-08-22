import tkinter as tk
import sys

import ui_setup
import vec2
import math
import zmap
from log import *



if __name__ == "__main__":
    # Initialize the log files
    LogInit()
    

    # Start App
    root = tk.Tk()
    maia_app = ui_setup.UISetup(master=root)
    maia_app.Run()

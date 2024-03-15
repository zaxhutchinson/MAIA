import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging
import loader
import json
import comp
import obj
import zmap
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring

from ui_widgets import *


class UIMapConfig(tk.Toplevel):
    def __init__(self, map_width, map_height, master=None, logger=None):
        super().__init__(master)
        self.master = master

        self.map_width = map_width
        self.map_height = map_height

        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.build_ui()

    def build_ui(self):
        self.cell_size = 32
        self.map_obj_char_size = 24
        self.map_item_char_size = 10
        self.char_offset = (self.cell_size - self.map_obj_char_size) / 2
        self.map_obj_font = tk.font.Font(
            family="TkFixedFont", size=self.map_obj_char_size
        )
        self.map_item_font = tk.font.Font(
            family="TkFixedFont", size=self.map_item_char_size
        )

        self.xbar = tk.Scrollbar(self.container, orient=tk.HORIZONTAL)
        self.ybar = tk.Scrollbar(self.container, orient=tk.VERTICAL)
        self.canvas = uiCanvas(
            master=self.container,
            width=800,
            height=800,
            xscrollcommand=self.xbar.set,
            yscrollcommand=self.ybar.set,
            scrollregion=(
                0,
                0,
                (self.map_width + 2) * self.cell_size,
                (self.map_height + 2) * self.cell_size,
            ),
            cell_size=self.cell_size,
            obj_char_size=self.map_obj_char_size,
            item_char_size=self.map_item_char_size,
            char_offset=self.char_offset,
            obj_font=self.map_obj_font,
            item_font=self.map_item_font,
        )
        self.ybar.configure(command=self.canvas.yview)
        self.xbar.configure(command=self.canvas.xview)
        self.ybar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.yview_moveto(0.0)
        self.canvas.xview_moveto(0.0)

        # Draw the background tiles
        self.canvas_background_tile_ids = []
        self.canvas_background_RCnum_ids = []
        self.drawTiles()

        # self.obj_drawIDs = {}
        # self.initObjects()

        # self.item_drawIDs = {}
        # self.initItems()

    def drawTiles(self):

        w = self.map_width + 2
        h = self.map_height + 2

        for x in range(w):
            for y in range(h):

                if x != 0 and x != w - 1 and y != 0 and y != h - 1:

                    tile_id = self.canvas.drawTile(x=x, y=y, fill="snow4")

                    self.canvas_background_tile_ids.append(tile_id)

                if (x == 0 and (y != 0 and y != h - 1)) or (
                    x == w - 1 and (y != 0 and y != h - 1)
                ):
                    RCnum_id = self.canvas.drawRCNumber(
                        x=x, y=y, fill="gray35", text=str(y - 1)
                    )
                    self.canvas_background_RCnum_ids.append(RCnum_id)
                elif (y == 0 and (x != 0 and x != w - 1)) or (
                    y == h - 1 and (x != 0 and x != w - 1)
                ):
                    RCnum_id = self.canvas.drawRCNumber(
                        x=x, y=y, fill="gray35", text=str(x - 1)
                    )
                    self.canvas_background_RCnum_ids.append(RCnum_id)

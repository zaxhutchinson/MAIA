import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext

import uuid
import random

import queue
import cProfile
import logging
import loader
import json
import comp
import obj
import zmap

from ui_widgets import *


class UIMapConfig(tk.Toplevel):
    def __init__(self, _map, master=None, logger=None):
        super().__init__(master)
        self.master = master
        self.logger = logger
        self.ldr = loader.Loader(self.logger)

        self.map = _map
        self.map_width = self.map.getData("width")
        self.map_height = self.map.getData("height")

        self.objs = {}
        self.items = {}
        self.sides = {}

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

        self.add_objects()
        self.add_ai_objects()
        self.add_items()

        # Draw the background tiles
        self.canvas_background_tile_ids = []
        self.canvas_background_RCnum_ids = []
        self.draw_tiles()

        self.obj_drawIDs = {}
        self.initObjects()

        self.item_drawIDs = {}
        self.initItems()

    def add_objects(self):
        # Create the map border
        edge_obj_id = self.map.getData("edge_obj_id")
        edge_coords = self.map.getListOfEdgeCoordinates()
        for ec in edge_coords:
            # Copy the obj
            newobj = self.ldr.copyObjTemplate(edge_obj_id)
            # Create obj place data
            data = {}
            data["x"] = ec[0]
            data["y"] = ec[1]
            data["uuid"] = uuid.uuid4()
            # Place, add to objDict and add to map
            newobj.place(data)
            self.objs[data["uuid"]] = newobj

        # Add all placed objects
        pl_objs = self.map.getData("placed_objects")
        for oid, lst in pl_objs.items():
            for o in lst:
                # If an object entry in placed_objs does not
                # have a position, it is ignored.
                if "x" in o and "y" in o:
                    newobj = self.ldr.copyObjTemplate(oid)
                    data = o
                    data["uuid"] = uuid.uuid4()
                    newobj.place(data)
                    self.objs[data["uuid"]] = newobj

    def add_ai_objects(self):
        # Add possible team and ai-controlled obj locations
        sides = self.map.getData("sides")
        print(sides)
        for iid, lst in sides.items():
            starting_locations = list(lst["starting_locations"])
            print(starting_locations)

            for loc in starting_locations:
                newobj = self.ldr.copyObjTemplate("player")
                data = {}

                data["x"] = loc[0]
                data["y"] = loc[1]
                data["uuid"] = uuid.uuid4()

                # Place and store and add to map
                newobj.place(data)
                self.objs[data["uuid"]] = newobj

    def add_items(self):
        # Add all placed items
        pl_items = self.map.getData("placed_items")
        for iid, lst in pl_items.items():
            for i in lst:
                # If an item entry does not have a position, ignore.
                if "x" in i and "y" in i:
                    newitem = self.ldr.copyItemTemplate(iid)
                    data = i
                    data["uuid"] = uuid.uuid4()
                    newitem.place(data)
                    self.items[data["uuid"]] = newitem

    def draw_tiles(self):

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

    def addObjectDrawID(self, _uuid, _drawID):
        self.obj_drawIDs[_uuid] = _drawID

    def getObjectDrawID(self, _uuid):
        try:
            return self.obj_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UIMapConfig: KeyError " + str(_uuid) + " in getObjectDrawID()."
            )
            return None

    def initObjects(self):
        draw_data = []

        for curr_obj in self.objs.values():
            draw_data.append(curr_obj.getDrawData())

        for dd in draw_data:
            obj_id = self.canvas.drawObj(dd=dd)
            self.addObjectDrawID(dd["uuid"], obj_id)

    def addItemDrawID(self, _uuid, _drawID):
        self.item_drawIDs[_uuid] = _drawID

    def getItemDrawID(self, _uuid):
        try:
            return self.item_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UIMapConfig: KeyError " + str(_uuid) + " in getObjectDrawID()."
            )
            return None

    def initItems(self):
        draw_data = []

        for curr_items in self.items.values():
            draw_data.append(curr_items.getDrawData())

        for dd in draw_data:
            item_id = self.canvas.drawObj(dd=dd)
            self.addItemDrawID(dd["uuid"], item_id)

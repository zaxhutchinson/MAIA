import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext

import uuid
import loader

from ui_widgets import *


class UIMapConfig(tk.Toplevel):
    def __init__(self, _map, master=None, logger=None):
        """Sets window and frame information and calls function to build UI"""
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
        """Generates UI of map

        Set map info, generate canvas, draw tiles,
        draw placed objects, draw placed items, draw
        ai-controlled objects
        """
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

        self.x_bar = tk.Scrollbar(self.container, orient=tk.HORIZONTAL)
        self.y_bar = tk.Scrollbar(self.container, orient=tk.VERTICAL)
        self.canvas = uiCanvas(
            master=self.container,
            width=800,
            height=800,
            xscrollcommand=self.x_bar.set,
            yscrollcommand=self.y_bar.set,
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
        self.y_bar.configure(command=self.canvas.yview)
        self.x_bar.configure(command=self.canvas.xview)
        self.y_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_bar.pack(side=tk.BOTTOM, fill=tk.X)
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
        """Add edges and placed object to obj list"""
        # Create the map border
        edge_obj_id = self.map.getData("edge_obj_id")
        edge_coords = self.map.getListOfEdgeCoordinates()
        for ec in edge_coords:
            # Copy the obj
            new_obj = self.ldr.copyObjTemplate(edge_obj_id)
            # Create obj place data
            data = {}
            data["x"] = ec[0]
            data["y"] = ec[1]
            data["uuid"] = uuid.uuid4()
            # Place, add to objDict and add to map
            new_obj.place(data)
            self.objs[data["uuid"]] = new_obj

        # Add all placed objects
        pl_objs = self.map.getData("placed_objects")
        for oid, lst in pl_objs.items():
            for o in lst:
                # If an object entry in placed_objs does not
                # have a position, it is ignored.
                if "x" in o and "y" in o:
                    new_obj = self.ldr.copyObjTemplate(oid)
                    data = o
                    data["uuid"] = uuid.uuid4()
                    new_obj.place(data)
                    self.objs[data["uuid"]] = new_obj

    def add_ai_objects(self):
        """Add ai-controlled object to obj list"""
        # Add possible team and ai-controlled obj locations
        sides = self.map.getData("sides")
        for iid, lst in sides.items():
            starting_locations = list(lst["starting_locations"])

            for loc in starting_locations:
                new_obj = self.ldr.copyObjTemplate("start_loc")
                new_obj.setData("fill_alive", lst["color"])
                data = {}

                data["x"] = loc[0]
                data["y"] = loc[1]
                data["uuid"] = uuid.uuid4()

                # Place and store and add to map
                new_obj.place(data)
                self.objs[data["uuid"]] = new_obj

    def add_items(self):
        """Add placed items to item list"""
        # Add all placed items
        pl_items = self.map.getData("placed_items")
        for iid, lst in pl_items.items():
            for i in lst:
                # If an item entry does not have a position, ignore.
                if "x" in i and "y" in i:
                    new_item = self.ldr.copyItemTemplate(iid)
                    data = i
                    data["uuid"] = uuid.uuid4()
                    new_item.place(data)
                    self.items[data["uuid"]] = new_item

    def draw_tiles(self):
        """Draw tiles on canvas"""
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
        """Add object draw id to obj draw id list"""
        self.obj_drawIDs[_uuid] = _drawID

    def getObjectDrawID(self, _uuid):
        """Get object draw id"""
        try:
            return self.obj_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UIMapConfig: KeyError " + str(_uuid) + " in getObjectDrawID()."
            )
            return None

    def initObjects(self):
        """Draw initial object state

        Get and add draw date for every object to draw data list
        Draw each object on canvas
        """
        draw_data = []

        for curr_obj in self.objs.values():
            draw_data.append(curr_obj.getDrawData())

        for dd in draw_data:
            obj_id = self.canvas.drawObj(dd=dd)
            self.addObjectDrawID(dd["uuid"], obj_id)

    def addItemDrawID(self, _uuid, _drawID):
        """Add item draw id to item draw id list"""
        self.item_drawIDs[_uuid] = _drawID

    def getItemDrawID(self, _uuid):
        """Get item draw id"""
        try:
            return self.item_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UIMapConfig: KeyError " + str(_uuid) + " in getObjectDrawID()."
            )
            return None

    def initItems(self):
        """Draw initial item state

        Get and add draw date for every item to draw data list
        Draw each item on canvas
        """
        draw_data = []

        for curr_items in self.items.values():
            draw_data.append(curr_items.getDrawData())

        for dd in draw_data:
            item_id = self.canvas.drawObj(dd=dd)
            self.addItemDrawID(dd["uuid"], item_id)

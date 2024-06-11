import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext

import uuid
import loader

from ui_widgets import *


class UIMapConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        """Sets window and frame information and calls function to build ui"""
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.logger = logger
        self.ldr = ldr

        # Possible general config parameters.
        self.cell_size = 32             # in pixels
        self.border_size = 32           # in pixels, the area around the map where row/column labels are drawn.
        self.map_obj_char_size = 24     # font size
        self.map_item_char_size = 10    # font size

        self.canvas = None
        self.x_bar = None
        self.y_bar = None

        self.objs = {}
        self.items = {}
        self.sides = {}

        self.build_ui()
        self.populate_map_listbox()
        self.populate_obj_listbox()
        self.populate_item_listbox()

    def build_ui(self):
        """Generates UI of map

        Sets map info, generates canvas, draws tiles,
        draws placed objects, draws placed items, draws
        ai-controlled objects
        """
        self.main_frame = uiQuietFrame(master=self)
        self.map_selection_frame = uiLabelFrame(master=self.main_frame, text="Maps")
        self.map_container_frame = uiQuietFrame(master=self.main_frame)
        self.map_frame = uiQuietFrame(master=self.map_container_frame)
        self.map_info_frame = uiLabelFrame(master=self.map_container_frame, text="Map Info")
        self.paint_frame = uiQuietFrame(master=self.main_frame)
        self.add_remove_frame = uiQuietFrame(master=self.paint_frame)
        self.obj_selection_frame = uiLabelFrame(master=self.paint_frame, text="Objects")
        self.item_selection_frame = uiLabelFrame(master=self.paint_frame, text="Items")
        self.button_row = uiQuietFrame(master=self.main_frame)
        self.title_label = uiLabel(master=self.main_frame, text="Map Configuration")

        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.map_selection_frame.pack(side=tk.LEFT, fill="y")
        self.map_container_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.map_info_frame.pack(side=tk.LEFT, fill="y")
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.paint_frame.pack(side=tk.RIGHT, fill="y")
        self.add_remove_frame.pack(side=tk.TOP, fill="x")
        self.add_remove_frame.rowconfigure(0,weight=1)
        self.add_remove_frame.columnconfigure(0,weight=1)
        self.obj_selection_frame.pack(side=tk.TOP, fill="y", expand=True)
        self.obj_selection_frame.rowconfigure(0, weight=1)
        self.item_selection_frame.pack(side=tk.TOP, fill="y", expand=True)
        self.item_selection_frame.rowconfigure(0, weight=1)
        


        # MAP SELECTION
        self.map_select_listbox_var = tk.StringVar()
        self.map_select_listbox = uiListBox(
            master=self.map_selection_frame,
            listvariable=self.map_select_listbox_var,
            selectmode='single'
        )
        self.map_select_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.map_select_listbox.bind(
            "<<ListboxSelect>>", self.show_map
        )

        # MAP



        # MAP INFO
        self.map_info_frame.columnconfigure(1,weight=1)

        self.map_id_label = uiLabel(master=self.map_info_frame, text="ID")
        self.map_id_entry = EntryHelp(master=self.map_info_frame, text="The unique ID of the map.")
        self.map_name_label = uiLabel(master=self.map_info_frame, text="Name")
        self.map_name_entry = EntryHelp(master=self.map_info_frame, text="The name of the map (does not have to be unique).")
        self.map_desc_label = uiLabel(master=self.map_info_frame, text="Description")
        self.map_desc_text = uiTextbox(master=self.map_info_frame)
        self.map_desc_text.configure(width=16, height=5, state=tk.NORMAL)
        self.map_width_label = uiLabel(master=self.map_info_frame, text="Width")
        self.map_width_entry = EntryHelp(master=self.map_info_frame, text="The playable width of the map in number of cells. NOTE: The actual width will be two greater to compensate for the edges.")
        self.map_height_label = uiLabel(master=self.map_info_frame, text="Height")
        self.map_height_entry = EntryHelp(master=self.map_info_frame, text="The playable height of the map in number of cells. NOTE: The actual width will be two greater to compensate for the edges.")
        self.map_edge_id_label = uiLabel(master=self.map_info_frame, text="Edge Obj ID")
        self.map_edge_id_entry = EntryHelp(master=self.map_info_frame, text="The ID of the object at the outer edge of the map. This should be an indestructible object. Copies of this object will be added automatically to fence in the playable area.")

        self.map_id_label.grid(row=0, column=0, sticky="ew")
        self.map_id_entry.frame.grid(row=0, column=1, sticky="ew")
        self.map_name_label.grid(row=1, column=0, sticky="ew")
        self.map_name_entry.frame.grid(row=1, column=1, sticky="ew")
        self.map_width_label.grid(row=2, column=0, sticky="ew")
        self.map_width_entry.frame.grid(row=2, column=1, sticky="ew")
        self.map_height_label.grid(row=3, column=0, sticky="ew")
        self.map_height_entry.frame.grid(row=3, column=1, sticky="ew")
        self.map_desc_label.grid(row=4, column=0, columnspan=2,sticky="w")
        self.map_desc_text.grid(row=5, column=0, columnspan=2,sticky="nesw")
        self.map_edge_id_label.grid(row=6, column=0, sticky="ew")
        self.map_edge_id_entry.frame.grid(row=6, column=1, sticky="ew")

        # OBJ/ITEM SELECTION
        self.add_remove_var = 0
        self.add_button = uiButton(
            master=self.add_remove_frame,
            command=self.toggle_add,
            text="Add Item/Object",
            bg="red"
        )
        self.add_button.config(bg="red")
        self.add_button.grid(row=1,column=0,sticky="ew")
        self.remove_button = uiButton(
            master=self.add_remove_frame,
            command=self.toggle_remove,
            text="Remove Item/Object",
        )
        self.remove_button.config(bg="red")
        self.remove_button.grid(row=2, column=0, sticky="ew")

        self.draw_label = uiLabel(master=self.add_remove_frame, text="Toggle Add or Remove")
        self.draw_label.grid(row=0,column=0,sticky="ew")
        self.draw_label.columnconfigure(0,weight=1)
        self.obj_select_listbox_var = tk.StringVar()
        self.obj_select_listbox = uiListBox(
            master=self.obj_selection_frame,
            listvariable=self.obj_select_listbox_var,
            selectmode='single'
        )
        self.obj_select_listbox.bind("<<ListboxSelect>>", self.object_clicked)
        self.obj_select_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.item_select_listbox_var = tk.StringVar()
        self.item_select_listbox = uiListBox(
            master=self.item_selection_frame,
            listvariable=self.item_select_listbox_var,
            selectmode='single'
        )
        self.item_select_listbox.bind("<<ListboxSelect>>", self.item_clicked)
        self.item_select_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # BUTTON ROW
        self.map_create_button = uiButton(
            master=self.button_row,
            command=self.create_map,
            text="New Map"
        )
        self.map_create_button.pack(side=tk.LEFT)
        self.map_update_button = uiButton(
            master=self.button_row,
            command=self.update_map,
            text="Update Map"
        )
        self.map_update_button.pack(side=tk.LEFT)
        self.map_delete_button = uiCarefulButton(
            master=self.button_row,
            command=self.delete_map,
            text="Delete Map"
        )
        self.map_delete_button.pack(side=tk.LEFT)
        self.home_button = uiButton(
            master=self.button_row,
            command=self.goto_home,
            text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiCarefulButton(
            master=self.button_row,
            command=self.save_to_json,
            text="Save Map to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

    def toggle_add(self):
        if self.add_remove_var == -1:
            self.remove_button.config(bg="red")
            self.add_remove_var = 1
            self.add_button.config(bg="green")
        elif self.add_remove_var == 1:
            self.add_remove_var = 0
            self.add_button.config(bg="red")
        elif self.add_remove_var == 0:
            self.add_remove_var = 1
            self.add_button.config(bg="green")

    def toggle_remove(self):
        if self.add_remove_var == 1:
            self.add_button.config(bg="red")
            self.add_remove_var = -1
            self.remove_button.config(bg="green")
        elif self.add_remove_var == -1:
            self.add_remove_var = 0
            self.remove_button.config(bg="red")
        elif self.add_remove_var == 0:
            self.add_remove_var = -1
            self.remove_button.config(bg="green")

    def populate_map_listbox(self):
        
        self.map_select_listbox.delete(0, tk.END)
        map_data = self.ldr.get_map_templates()
        entries = []
        for m in map_data.values():
            entry = f"{m["id"]}:{m["name"]}"
            entries.append(entry)
        self.map_select_listbox_var.set(entries)

    def populate_obj_listbox(self):
        
        self.obj_select_listbox.delete(0, tk.END)
        obj_data = self.ldr.get_obj_templates()
        entries = []
        for o in obj_data.values():
            entry = f"{o["id"]}:{o["name"]}"
            entries.append(entry)
        self.obj_select_listbox_var.set(entries)

    def populate_item_listbox(self):
        
        self.item_select_listbox.delete(0, tk.END)
        item_data = self.ldr.get_item_templates()
        entries = []
        for i in item_data.values():
            entry = f"{i["id"]}:{i["name"]}"
            entries.append(entry)
        self.item_select_listbox_var.set(entries)


    def object_clicked(self, event=None):
        self.item_select_listbox.selection_clear(0, tk.END)

    def item_clicked(self, event=None):
        self.obj_select_listbox.selection_clear(0, tk.END)
    

    def create_map(self):
        pass
    def update_map(self):
        pass
    def delete_map(self):
        pass
    def goto_home(self):
        pass
    def save_to_json(self):
        pass


    def get_currently_selected_map(self):
        map_index = self.map_select_listbox.curselection()
        if len(map_index) == 1:
            map_entry = self.map_select_listbox.get(map_index[0])
            map_id, map_name = map_entry.split(":")
            return self.ldr.get_map_template(map_id)
        else:
            return None

    def get_currently_selected_obj(self):
        obj_index = self.obj_select_listbox.curselection()
        if len(obj_index) == 1:
            obj_entry = self.obj_select_listbox.get(obj_index[0])
            obj_id, obj_name = obj_entry.split(":")
            return self.ldr.get_obj_template(obj_id)
        else:
            return None

    def get_currently_selected_item(self):
        item_index = self.item_select_listbox.curselection()
        if len(item_index) == 1:
            item_entry = self.item_select_listbox.get(item_index[0])
            item_id, item_name = item_entry.split(":")
            return self.ldr.get_item_template(item_id)
        else:
            return None

    def clear_map_info(self):
        self.map_id_entry.entry.delete(0, tk.END)
        self.map_name_entry.entry.delete(0, tk.END)
        self.map_desc_text.delete(1.0, tk.END)
        self.map_width_entry.entry.delete(0, tk.END)
        self.map_height_entry.entry.delete(0, tk.END)
        self.map_edge_id_entry.entry.delete(0, tk.END)

    def show_map_info(self, cur_map):
        self.clear_map_info()

        self.map_id_entry.entry.insert(0, cur_map["id"])
        self.map_name_entry.entry.insert(0, cur_map["name"])
        self.map_desc_text.insert(1.0, cur_map["desc"])
        self.map_width_entry.entry.insert(0, cur_map["width"])
        self.map_height_entry.entry.insert(0, cur_map["height"])
        self.map_edge_id_entry.entry.insert(0, cur_map["edge_obj_id"])

    def show_map(self, event=None):

        if self.canvas != None:
            self.canvas.destroy()
            self.x_bar.destroy()
            self.y_bar.destroy()
            self.canvas = None
            self.x_bar = None
            self.y_bar = None
            self.cur_map = None

        self.cur_map = self.get_currently_selected_map()
        if self.cur_map != None:

            self.show_map_info(self.cur_map)

            # Get map attributes
            map_width = self.cur_map["width"]
            map_height = self.cur_map["height"]

            
            self.char_offset = (self.cell_size - self.map_obj_char_size) / 2
            self.map_obj_font = tk.font.Font(
                family="TkFixedFont", size=self.map_obj_char_size
            )
            self.map_item_font = tk.font.Font(
                family="TkFixedFont", size=self.map_item_char_size
            )

            self.x_bar = tk.Scrollbar(self.map_frame, orient=tk.HORIZONTAL)
            self.y_bar = tk.Scrollbar(self.map_frame, orient=tk.VERTICAL)
            self.canvas = uiCanvas(
                master=self.map_frame,
                width=800,
                height=800,
                xscrollcommand=self.x_bar.set,
                yscrollcommand=self.y_bar.set,
                scrollregion=(
                    0,
                    0,
                    (map_width + 2) * self.cell_size,
                    (map_height + 2) * self.cell_size,
                ),
                cell_size=self.cell_size,
                border_size=self.border_size,
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
            self.canvas.bind('<Button-1>', self.map_mouse_click)

            self.draw_tiles(map_width, map_height)
            self.draw_rc_labels(map_width, map_height)
            self.draw_objects(self.cur_map)
            self.draw_edge_objs(self.cur_map)
            self.draw_starting_locations(self.cur_map)

            # self.add_objects(cur_map)
            # self.add_ai_objects()
            # self.add_items()

            # # Draw the background tiles
            # self.canvas_background_tile_ids = []
            # self.canvas_background_RCnum_ids = []
            

            # self.obj_drawIDs = {}
            # self.init_objects()

            # self.item_drawIDs = {}
            # self.init_items()

    def map_mouse_click(self, event):
        x,y = self.canvas.mousexy_to_cellxy(event.x, event.y)
        if x >= 0 and y >= 0 and x < self.cur_map["width"] and y < self.cur_map["height"]:
            

            ##############################################################
            # Search the map for obj/item
            thing_type = None
            thing_index = None
            
            # First check objects
            for i in range(len(self.cur_map["objects"])):
                obj = self.cur_map["objects"][i]
                if obj["x"]==x and obj["y"]==y:
                    thing_index = i
                    thing_type = "object"
                    break

            # If what was clicked wasn't an object, check items.
            if thing_index == None:
                for i in range(len(self.cur_map["items"])):
                    itm = self.cur_map["items"][i]
                    if itm["x"]==x and itm["y"]==y:
                        thing_index = i
                        thing_type = "item"
                        break
            #############################################################
            
            # If we found something, we can remove it or print info (TODO)
            if thing_index != None:
                if self.add_remove_var < 0:
                    if thing_type == "object":
                        del self.cur_map["objects"][thing_index]
                        self.canvas.remove_obj_at(x,y)
                    elif thing_type == "item":
                        del self.cur_map["items"][thing_index]
                
                elif self.add_remove_var == 0: # info
                    if thing_type == "object":
                        pass
                    elif thing_type == "item":
                        pass
            # else it's empty and we can add something.
            else:
                if self.add_remove_var > 0:
                    itm = self.get_currently_selected_item()
                    obj = self.get_currently_selected_obj()
                    if obj != None:
                        obj_entry = {
                            "id":obj["id"],
                            "x":x,
                            "y":y
                        }
                        self.cur_map["objects"].append(obj_entry)
                        self.canvas.draw_sprite(
                            x=x, y=y, sprite_filename=obj["alive_sprite_filename"]
                        )
                    elif itm != None:
                        pass

    def draw_tiles(self, width, height):
        """Draws tiles on canvas"""

        for x in range(width):
            for y in range(height):

                tile_id = self.canvas.draw_tile(x=x, y=y, fill="#DDDDDD")

                # self.canvas_background_tile_ids.append(tile_id)

    def draw_rc_labels(self, width, height):
        """Draws tiles on canvas"""

        self.canvas.draw_row_labels(
            width=width, height=height,
            fill="#000000"
        )
        self.canvas.draw_column_labels(
            width=width, height=height,
            fill="#000000"
        )

    def draw_objects(self, cur_map):
        """Adds edges and placed object to obj list"""
        # Get map attributes
        map_width = cur_map["width"]
        map_height = cur_map["height"]

        for obj_entry in cur_map["objects"]:

            obj = self.ldr.get_obj_template(obj_entry["id"])

            sprite_filename = obj["alive_sprite_filename"]

            self.canvas.draw_sprite(
                x=obj_entry["x"], y=obj_entry["y"],
                sprite_filename=sprite_filename
            )

    def draw_edge_objs(self, cur_map):
        """
        Draws the edge objects
        """
        edge_obj_id = cur_map["edge_obj_id"]
        edge_obj = self.ldr.get_obj_template(edge_obj_id)
        map_width = cur_map["width"]
        map_height = cur_map["height"]
        sprite_filename = edge_obj["alive_sprite_filename"]

        # Draw top and bottom edges
        for x in range(map_width):
            self.canvas.draw_sprite(
                x=x, y=0, sprite_filename=sprite_filename
            )
            self.canvas.draw_sprite(
                x=x, y=map_height-1, sprite_filename=sprite_filename
            )

        # Draw left and right (minus the corner hexes)
        for y in range(1,map_height-1):
            self.canvas.draw_sprite(
                x=0, y=y, sprite_filename=sprite_filename
            )
            self.canvas.draw_sprite(
                x=map_width-1, y=y, sprite_filename=sprite_filename
            )

    def draw_starting_locations(self, cur_map):
        """Adds ai-controlled object to obj list"""
        # Add possible team and ai-controlled obj locations
        sides = cur_map["sides"]

        for side in sides:
            color = side["color"]
            starting_locations = side["starting_locations"]

            for i in range(len(starting_locations)):
                loc = starting_locations[i]
                x = loc["x"]
                y = loc["y"]
                self.canvas.draw_starting_location(
                    x, y, i, color
                )
                # self.canvas.draw_circle(
                #     x, y, color, self.cell_size-5
                # )
                # self.canvas.draw_character(
                #     x, y, str(i), "black"
                # )

        # sides = self.map.get_data("sides")
        # for iid, lst in sides.items():
        #     starting_locations = list(lst["starting_locations"])

        #     for loc in starting_locations:
        #         new_obj = self.ldr.copy_obj_template("start_loc")
        #         new_obj.set_data("fill_alive", lst["color"])
        #         data = {}

        #         data["x"] = loc[0]
        #         data["y"] = loc[1]
        #         data["uuid"] = uuid.uuid4()

        #         # Place and store and add to map
        #         new_obj.place(data)
        #         self.objs[data["uuid"]] = new_obj

    def add_items(self):
        """Adds placed items to item list"""
        # Add all placed items
        pl_items = self.map.get_data("placed_items")
        for iid, lst in pl_items.items():
            for i in lst:
                # If an item entry does not have a position, ignore.
                if "x" in i and "y" in i:
                    new_item = self.ldr.copy_item_template(iid)
                    data = i
                    data["uuid"] = uuid.uuid4()
                    new_item.place(data)
                    self.items[data["uuid"]] = new_item



    def add_object_draw_id(self, _uuid, _drawID):
        """Adds object draw id to obj draw id list"""
        self.obj_drawIDs[_uuid] = _drawID

    def get_object_draw_id(self, _uuid):
        """Gets object draw id"""
        try:
            return self.obj_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UIMapConfig: KeyError " + str(_uuid) + " in getObjectDrawID()."
            )
            return None

    def init_objects(self):
        """Draws initial object state

        Gets and adds draw data for every object to draw data list
        Draws each object on canvas
        """
        draw_data = []

        for curr_obj in self.objs.values():
            draw_data.append(curr_obj.get_draw_data())

        for dd in draw_data:
            obj_id = self.canvas.draw_sprite(dd=dd)
            self.add_object_draw_id(dd["uuid"], obj_id)

    def add_item_draw_id(self, _uuid, _drawID):
        """Adds item draw id to item draw id list"""
        self.item_drawIDs[_uuid] = _drawID

    def get_item_draw_id(self, _uuid):
        """Gets item draw id"""
        try:
            return self.item_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UIMapConfig: KeyError " + str(_uuid) + " in getObjectDrawID()."
            )
            return None

    def init_items(self):
        """Draws initial item state

        Gets and adds draw data for every item to draw data list
        Draws each item on canvas
        """
        draw_data = []

        for curr_items in self.items.values():
            draw_data.append(curr_items.get_draw_data())

        for dd in draw_data:
            item_id = self.canvas.draw_sprite(dd=dd)
            self.add_item_draw_id(dd["uuid"], item_id)

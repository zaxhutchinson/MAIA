##############################################################################
# UI SIM
#
# The main UI element for a simulation in progress.
##############################################################################
import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile
import logging
import ui_scoreboard

from ui_widgets import *


class UISim(tk.Toplevel):
    def __init__(
        self, map_width, map_height, sim, omsgr, controller, master=None, logger=None
    ):
        """Sets window and frame information and generates the sim UI

        Sets map info, generates canvas, draws tiles,
        draws placed objects, draws placed items, draws
        ai-controlled objects
        Places sim log, places turns-to-run entry elements,
        places end game button
        """
        super().__init__(master)
        self.master = master
        self.configure(bg=BGCOLOR)
        self.title("MAIA - Sim UI")
        self.logger = logger
        self.controller = controller

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

        # Store data
        self.sim = sim
        self.omsgr = omsgr
        self.map_width = map_width
        self.map_height = map_height

        self.UIMap = None

        # Create the left and right frames
        self.map_frame = uiQuietFrame(master=self)
        self.map_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.log_frame = uiQuietFrame(master=self)
        self.log_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        # Create the map canvas
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

        # Create the log notebook and tabs

        self.log_notebook = uiNotebook(master=self.log_frame)
        self.log_notebook.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        self.main_log_frame = uiQuietFrame(master=self.log_notebook)
        self.log_notebook.add(self.main_log_frame, text="Main")
        self.main_log_scroll = uiScrollText(master=self.main_log_frame)
        self.main_log_scroll.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.main_log_scroll.configure(state="disabled")

        # Add the buttons
        self.data_frame_1 = uiQuietFrame(master=self.log_frame)
        self.data_frame_1.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.turns_label = uiLabel(master=self.data_frame_1, text="Turns To Run")
        self.turns_label.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.turns_entry = uiEntry(master=self.data_frame_1)
        self.turns_entry.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # self.data_frame_2 = uiQuietFrame(master=self.log_frame)
        # self.data_frame_2.pack(fill=tk.BOTH,expand=True,side=tk.TOP)

        self.btn_frame_1 = uiQuietFrame(master=self.log_frame)
        self.btn_frame_1.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.turns_button = uiButton(
            master=self.btn_frame_1, text="Run X Turns", command=self.run_x_turns
        )
        self.turns_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.display_points_button = uiButton(
            master=self.btn_frame_1, text="Display Points", command=self.display_points
        )
        self.display_points_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.top_right_frame = uiQuietFrame(master=self.log_frame)
        self.top_right_frame.pack(fill=tk.NONE, expand=False, side=tk.TOP, anchor="ne")

        self.end_game_button = uiButton(
            master=self.top_right_frame,
            text="End Game",
            command=self.display_scoreboard,
            width=10,
        )
        self.end_game_button.pack(padx=5, pady=5)

        self.log_frame.after(100, self.update_log)

        # Draw the background tiles
        self.canvas_background_tile_ids = []
        self.canvas_background_rc_num_ids = []
        self.draw_tiles()

        self.obj_draw_ids = {}
        self.init_objects()

        self.item_drawIDs = {}
        self.init_items()

        # TEST JUNK
        # self.canvas.create_text(50, 50, text="Hello world")
        # self.canvas.create_rectangle(50,50,450,450,fill="green")

    def display_message(self, msg):
        """Display message in sim log"""
        m = msg.get_text()
        self.main_log_scroll.configure(state="normal")
        self.main_log_scroll.insert(tk.END, m + "\n")
        self.main_log_scroll.configure(state="disabled")
        self.main_log_scroll.yview(tk.END)

    def draw_tiles(self):
        """Draw tiles on canvas"""
        w = self.map_width + 2
        h = self.map_height + 2

        for x in range(w):
            for y in range(h):

                if x != 0 and x != w - 1 and y != 0 and y != h - 1:

                    tile_id = self.canvas.draw_tile(x=x, y=y, fill="snow4")

                    self.canvas_background_tile_ids.append(tile_id)

                if (x == 0 and (y != 0 and y != h - 1)) or (
                    x == w - 1 and (y != 0 and y != h - 1)
                ):
                    rc_num_id = self.canvas.drawRCNumber(
                        x=x, y=y, fill="gray35", text=str(y - 1)
                    )
                    self.canvas_background_rc_num_ids.append(rc_num_id)
                elif (y == 0 and (x != 0 and x != w - 1)) or (
                    y == h - 1 and (x != 0 and x != w - 1)
                ):
                    rc_num_id = self.canvas.drawRCNumber(
                        x=x, y=y, fill="gray35", text=str(x - 1)
                    )
                    self.canvas_background_rc_num_ids.append(rc_num_id)

    #####################################################
    # OBJECT DRAWING
    def add_object_draw_id(self, _uuid, _drawID):
        """Adds object draw id to obj draw id list"""
        self.obj_draw_ids[_uuid] = _drawID

    def get_object_draw_id(self, _uuid):
        """Gets object draw id"""
        try:
            return self.obj_draw_ids[_uuid]
        except KeyError:
            self.logger.error(
                "UISim: KeyError " + str(_uuid) + " in get_object_draw_id()."
            )
            return None

    def remove_object_draw_id(self, _uuid):
        """Removes object draw id to obj draw id list"""
        obj_id = self.get_object_draw_id(_uuid)
        if obj_id is not None:
            self.canvas.remove_obj(obj_id)
            del self.obj_draw_ids[_uuid]

    def init_objects(self):
        """Draws initial object state

        Gets and add draw date for every object to draw data list
        Draws each object on canvas
        """
        # self.canvas.delete(tk.ALL)
        draw_data = self.sim.get_obj_draw_data()
        for dd in draw_data:
            obj_id = self.canvas.draw_obj(dd=dd)
            self.add_object_draw_id(dd["uuid"], obj_id)

    def update_objects(self):
        """Updates objects"""
        draw_data = self.sim.get_obj_draw_data()
        for dd in draw_data:
            if dd["redraw"]:
                obj_id = self.get_object_draw_id(dd["uuid"])
                obj_id = self.canvas.redraw_obj(dd=dd, obj_id=obj_id)
                self.add_object_draw_id(dd["uuid"], obj_id)
            else:
                obj_id = self.get_object_draw_id(dd["uuid"])
                self.canvas.update_drawn_obj(dd=dd, obj_id=obj_id)

    ######################################################
    # ITEM DRAWING
    def add_item_draw_id(self, _uuid, _drawID):
        """Adds item draw id to item draw id list"""
        self.item_drawIDs[_uuid] = _drawID

    def get_item_draw_id(self, _uuid):
        """Gets item draw id"""
        try:
            return self.item_drawIDs[_uuid]
        except KeyError:
            self.logger.error(
                "UISim: KeyError " + str(_uuid) + " in get_item_draw_id()."
            )
            return None

    def remove_item_draw_id(self, _uuid):
        """Removes object draw id from item draw id list"""
        del self.item_drawIDs[_uuid]

    def init_items(self):
        """Draws initial item state

        Gets and adds draw data for every item to draw data list
        Draws each item on canvas
        """
        draw_data = self.sim.get_item_draw_data()
        for dd in draw_data:
            item_id = self.canvas.drawItem(dd=dd)
            self.add_item_draw_id(dd["uuid"], item_id)

    def update_items(self):
        """Updates items"""
        draw_data = self.sim.get_item_draw_data()
        for dd in draw_data:
            item_id = self.get_item_draw_id(dd["uuid"])
            self.canvas.update_drawn_item(dd=dd, itemID=item_id)

    def update_log(self):
        """Updates log"""
        while True:
            try:
                m = self.omsgr.get_msg()
            except queue.Empty:
                break
            else:
                self.display_message(m)
        self.log_frame.after(100, self.update_log)

    def run_x_turns(self):
        """Run sim for a set number of turns"""
        turns_to_run = self.turns_to_run_entry.get()
        if turns_to_run.isdigit():
            turns_to_run = int(turns_to_run)
            if self.sim.run_sim(turns_to_run):
                self.display_scoreboard()

        self.update_objects()
        self.update_items()

    def display_points(self):
        """Displays points"""
        self.sim.get_points_data()

    def display_scoreboard(self):
        """Displays scoreboard"""
        teams_scores = self.sim.get_final_scores()
        for widget in self.log_frame.winfo_children():
            widget.pack_forget()

        scoreboard_frame = uiQuietFrame(master=self.log_frame)
        scoreboard_frame.pack(fill=tk.BOTH, expand=True)

        scoreboard_frame = ui_scoreboard.ScoreboardFrame(
            teams_scores, self.controller, self, self.sim, master=self.log_frame
        )
        scoreboard_frame.pack(fill=tk.BOTH, expand=True)

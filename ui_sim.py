##############################################################################
# UI SIM
#
# The main UI element for a simulation in progress.
##############################################################################
import tkinter as tk
import queue

import msgs
import ui_scoreboard

import ui_widgets as uiw

# The default delay between turns. This value is used by
# both the continuous and the turn-by-turn modes. If the delay
# box is empty or contains a non-integer, this value is used instead.
DEFAULT_TURN_DELAY_IN_MS = 500


class UISim(tk.Frame):
    def __init__(self, master, controller, logger, ldr):
        """Sets window and frame information and generates the sim UI

        Sets map info, generates canvas, draws tiles,
        draws placed objects, draws placed items, draws
        ai-controlled objects
        Places sim log, places turns-to-run entry elements,
        places end game button
        """
        super().__init__(master)
        self.master = master
        self.logger = logger
        self.controller = controller
        self.ldr = ldr
        self.border_size = 32
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
        self.sim = None
        self.map = None
        # self.omsgr = None
        self.map_width = None
        self.map_height = None
        self.UIMap = None
        self.continuous_run = False
        self.obj_draw_ids = {}
        self.item_drawIDs = {}

    def build(self, _sim):
        self.sim = _sim
        self.map = self.sim.get_map()
        self.map_width = self.map.get_width()
        self.map_height = self.map.get_height()
        self.build_ui()

    def build_ui(self):

        # Create the left and right frames
        self.map_frame = uiw.uiQuietFrame(master=self)
        self.map_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.log_frame = uiw.uiQuietFrame(master=self)
        self.log_frame.pack(fill=tk.BOTH, side=tk.RIGHT)
        self.log_frame.rowconfigure(1, weight=1)
        self.log_frame.columnconfigure(0, weight=1)

        # Create the map canvas
        self.x_bar = tk.Scrollbar(self.map_frame, orient=tk.HORIZONTAL)
        self.y_bar = tk.Scrollbar(self.map_frame, orient=tk.VERTICAL)

        self.canvas = uiw.uiCanvas(
            master=self.map_frame,
            width=100,
            height=100,
            xscrollcommand=self.x_bar.set,
            yscrollcommand=self.y_bar.set,
            scrollregion=(
                0,
                0,
                (self.map_width + 2) * self.cell_size,
                (self.map_height + 2) * self.cell_size,
            ),
            border_size=self.border_size,
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

        # self.log_notebook = uiw.uiNotebook(master=self.log_frame)
        # self.log_notebook.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # self.main_log_frame = uiw.uiQuietFrame(master=self.log_frame)
        # self.log_notebook.add(self.main_log_frame, text="Main")
        self.log_label = uiw.uiLabel(
            master=self.log_frame,
            text="Match Log"
        )
        self.log_label.grid(row=0, column=0, sticky="ew")

        self.main_log_scroll = uiw.uiScrollText(master=self.log_frame)
        self.main_log_scroll.grid(row=1, column=0, sticky="nsew")
        self.main_log_scroll.configure(state="disabled")
        self.main_log_scroll.configure(width=50)

        self.btn_frame_1 = uiw.uiQuietFrame(master=self.log_frame)
        self.btn_frame_1.grid(row=2, column=0, sticky="ew")
        self.btn_frame_1.rowconfigure(0, weight=1)
        self.btn_frame_1.columnconfigure(0, weight=1)

        self.btn_run = uiw.uiButton(
            master=self.btn_frame_1,
            text="Run",
            command=self.run_continuous_proxy
        )
        self.btn_run.grid(row=0, column=0, sticky="ew")
        self.btn_pause = uiw.uiButton(
            master=self.btn_frame_1,
            text="Pause",
            command=self.pause_continuous
        )
        self.btn_pause.grid(row=0, column=1, sticky="ew")
        self.delay_label = uiw.uiLabel(
            master=self.btn_frame_1, text="Delay (ms)"
        )
        self.delay_label.grid(row=0, column=2, sticky="ew")
        self.delay_entry = uiw.uiEntry(master=self.btn_frame_1)
        self.delay_entry.grid(row=0, column=3, sticky="ew")

        self.btn_frame_2 = uiw.uiQuietFrame(master=self.log_frame)
        self.btn_frame_2.grid(row=3, column=0, sticky="ew")
        self.btn_frame_2.rowconfigure(0, weight=1)
        self.btn_frame_2.columnconfigure(0, weight=1)

        self.turns_button = uiw.uiButton(
            master=self.btn_frame_2,
            text="Run X Turns",
            command=self.run_x_turns
        )
        self.turns_button.grid(row=0, column=0, sticky="ew")
        self.turns_label = uiw.uiLabel(
            master=self.btn_frame_2, text="Turns To Run"
        )
        self.turns_label.grid(row=0, column=1, sticky="ew")
        self.turns_entry = uiw.uiEntry(master=self.btn_frame_2)
        self.turns_entry.grid(row=0, column=2, sticky="ew")

        self.btn_frame_3 = uiw.uiQuietFrame(master=self.log_frame)
        self.btn_frame_3.grid(row=4, column=0, sticky="ew")
        self.btn_frame_3.rowconfigure(0, weight=1)
        self.btn_frame_3.columnconfigure(0, weight=1)

        self.display_points_button = uiw.uiButton(
            master=self.btn_frame_3,
            text="Display Points",
            command=self.display_points
        )
        self.display_points_button.grid(row=0, column=0, sticky="ew")
        self.end_game_button = uiw.uiButton(
            master=self.btn_frame_3,
            text="End Game",
            command=self.display_scoreboard
        )
        self.end_game_button.grid(row=0, column=1, sticky="ew")

        self.log_frame.after(100, self.update_log)

        # Draw the background tiles
        self.draw_tiles()
        self.draw_rc_labels()
        self.draw_map()

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
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.canvas.draw_tile(x=x, y=y, fill="#DDDDDD")

    def draw_rc_labels(self):
        self.canvas.draw_row_labels(
            width=self.map_width, height=self.map_height, fill="#000000"
        )
        self.canvas.draw_column_labels(
            width=self.map_width, height=self.map_height, fill="#000000"
        )

    def draw_map(self):
        self.draw_objects()
        self.draw_items()

    def draw_objects(self):
        for o in self.sim.get_objects().values():
            self.draw_object(o)

    def draw_object(self, _obj):
        dd = _obj.get_draw_data()
        if dd["redraw"]:
            self.remove_object_draw_id(dd["uuid"])
            obj_id = self.canvas.draw_sprite(**dd)
            self.add_object_draw_id(dd["uuid"], obj_id)

    def draw_items(self):
        for i in self.sim.get_items().values():
            self.draw_item(i)

    def draw_item(self, itm):
        dd = itm.get_draw_data()
        if dd["redraw"]:
            self.remove_item_draw_id(dd["uuid"])
            item_id = self.canvas.draw_sprite(**dd)
            self.add_item_draw_id(dd["uuid"], item_id)

    #####################################################
    # OBJECT DRAWING
    def add_object_draw_id(self, _uuid, _drawID):
        """Adds object draw id to obj draw id list"""
        self.obj_draw_ids[_uuid] = _drawID

    def get_object_draw_id(self, _uuid):
        """Gets object draw id"""
        if _uuid in self.obj_draw_ids:
            return self.obj_draw_ids[_uuid]
        else:
            return None

    def remove_object_draw_id(self, _uuid):
        """Removes object draw id to obj draw id list"""
        obj_id = self.get_object_draw_id(_uuid)
        if obj_id is not None:
            self.canvas.remove_obj(obj_id)
            del self.obj_draw_ids[_uuid]
    #
    # def init_objects(self):
    #     """Draws initial object state
    #
    #     Gets and add draw date for every object to draw data list
    #     Draws each object on canvas
    #     """
    #     # self.canvas.delete(tk.ALL)
    #     draw_data = self.sim.get_obj_draw_data()
    #     for dd in draw_data:
    #         obj_id = self.canvas.draw_sprite(
    #             x=dd["x"],
    #             y=dd["y"],
    #             sprite_filename=dd["sprite_filename"],
    #             sprite_type="object"
    #         )
    #         self.add_object_draw_id(dd["uuid"], obj_id)
    #
    # def update_objects(self):
    #     """Updates objects"""
    #     draw_data = self.sim.get_obj_draw_data()
    #     for dd in draw_data:
    #         if dd["redraw"]:
    #             obj_id = self.get_object_draw_id(dd["uuid"])
    #             obj_id = self.canvas.redraw_obj(dd=dd, obj_id=obj_id)
    #             self.add_object_draw_id(dd["uuid"], obj_id)
    #         else:
    #             obj_id = self.get_object_draw_id(dd["uuid"])
    #             self.canvas.update_drawn_obj(dd=dd, obj_id=obj_id)
    #
    # def update_object(self, object_draw_data):
    #     if object_draw_data["redraw"]:
    #         obj_id = self.get_object_draw_id(object_draw_data["uuid"])
    #         obj_id = self.canvas.redraw_obj(dd=object_draw_data, obj_id=obj_id)
    #         self.add_object_draw_id(object_draw_data["uuid"], obj_id)
    #     else:
    #         obj_id = self.get_object_draw_id(object_draw_data["uuid"])
    #         self.canvas.update_drawn_obj(dd=object_draw_data, obj_id=obj_id)

    ######################################################
    # ITEM DRAWING
    def add_item_draw_id(self, _uuid, _drawID):
        """Adds item draw id to item draw id list"""
        self.item_drawIDs[_uuid] = _drawID

    def get_item_draw_id(self, _uuid):
        """Gets item draw id"""
        if _uuid in self.item_drawIDs:
            return self.item_drawIDs[_uuid]
        else:
            return None

    def remove_item_draw_id(self, _uuid):
        """Removes object draw id from item draw id list"""
        del self.item_drawIDs[_uuid]
    #
    # def init_items(self):
    #     """Draws initial item state
    #
    #     Gets and adds draw data for every item to draw data list
    #     Draws each item on canvas
    #     """
    #     draw_data = self.sim.get_item_draw_data()
    #     for dd in draw_data:
    #         item_id = self.canvas.drawItem(dd=dd)
    #         self.add_item_draw_id(dd["uuid"], item_id)
    #
    # def update_items(self):
    #     """Updates items"""
    #     draw_data = self.sim.get_item_draw_data()
    #     for dd in draw_data:
    #         item_id = self.get_item_draw_id(dd["uuid"])
    #         self.canvas.update_drawn_item(dd=dd, itemID=item_id)

    def update_log(self):
        """Updates log"""
        pass
        # while True:
        #     try:
        #         pass
        #         # m = self.omsgr.get_msg()
        #     except queue.Empty:
        #         break
        #     else:
        #         pass
        #         # self.display_message(m)
        # self.log_frame.after(100, self.update_log)

    def run_x_turns(self):
        """Run sim for a set number of turns"""
        turns_to_run = self.turns_entry.get()
        if turns_to_run.isdigit():

            turns_to_run = int(turns_to_run)
            game_ended = False

            while turns_to_run > 0:

                self.display_message(msgs.Msg(self.sim.get_turn(), "Turn", ""))

                game_ended = self.sim.run_sim(self, 1)
                turns_to_run -= 1
                if game_ended:
                    self.display_scoreboard()
                    break

            self.draw_objects()
            self.draw_items()

    def run_continuous_proxy(self):
        """A proxy function for continuous mode"""
        self.continuous_run = True

        delay = self.delay_entry.get()
        if delay.isdigit():
            delay = int(delay)
        else:
            delay = DEFAULT_TURN_DELAY_IN_MS

        self.run_continuous(delay)

    def run_continuous(self, delay):
        """Responsible for continuous mode

        This function is rescheduled using tk's after method
        to create a continuous mode.
        """
        self.display_message(msgs.Msg(self.sim.get_turn(), "Turn", ""))

        # Will abort running another turn if the user has clicked
        #   pause between turns.
        if not self.continuous_run:
            return

        game_ended = self.sim.run_sim(self, 1, delay)
        self.draw_objects()
        self.draw_items()

        if game_ended:
            self.display_scoreboard()
        else:
            if self.continuous_run:
                self.btn_run.after(delay, self.run_continuous, delay)

    def pause_continuous(self):
        """Pauses continuous mode"""
        self.continuous_run = False

    def display_points(self):
        """Displays points"""
        self.sim.get_points_data()

    def display_scoreboard(self):
        """Displays scoreboard"""
        teams_scores = self.sim.get_final_scores()
        for widget in self.log_frame.winfo_children():
            widget.pack_forget()

        scoreboard_frame = uiw.uiQuietFrame(master=self.log_frame)
        scoreboard_frame.pack(fill=tk.BOTH, expand=True)

        scoreboard_frame = ui_scoreboard.ScoreboardFrame(
            teams_scores,
            self.controller,
            self,
            self.sim,
            master=self.log_frame
        )
        scoreboard_frame.pack(fill=tk.BOTH, expand=True)

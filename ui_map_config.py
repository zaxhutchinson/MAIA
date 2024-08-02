import tkinter as tk
import tkinter.font
import enum
import zfunctions
import trigger
import ui_widgets as uiw


class AddRemove(enum.Enum):
    Info = 0
    AddObject = 1
    DelObject = 2
    AddItem = 3
    DelItem = 4
    AddStart = 5
    DelStart = 6


class UITrigger:
    def __init__(self, items, items_on_map, cur_trigger=None):

        self.cur_trigger = cur_trigger

        self.name_var = ""
        self.type_var = ""
        self.points_var = 0
        self.item_ids = []

        self.top = tk.Toplevel()  # use Toplevel() instead of Tk()
        self.top.minsize(300,400)

        self.frame = uiw.uiQuietFrame(
            master=self.top
        )
        self.frame.configure(
            padx=10, pady=10
        )
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.name_label = uiw.uiLabel(master=self.frame, text="Name")
        self.name_entry = uiw.EntryHelp(
            master=self.frame,
            text="Custom name for the trigger."
        )
        self.type_label = uiw.uiLabel(master=self.frame, text="Type")
        self.type_combo = uiw.uiComboBox(master=self.frame)
        self.type_combo.config(values=trigger.TRIGGER_TYPES)
        self.type_combo.bind("<<ComboBoxSelect>>", lambda: ())
        self.points_label = uiw.uiLabel(master=self.frame, text="Points")
        self.points_entry = uiw.EntryHelp(
            master=self.frame,
            text="Points awarded for activating this trigger."
        )
        self.items_label = uiw.uiLabel(master=self.frame, text="Items")
        self.items_listbox_var = tk.StringVar()
        self.items_listbox = uiw.uiListBox(
            master=self.frame, listvariable=self.items_listbox_var, selectmode="multiple"
        )
        entries = []
        for i in items_on_map:
            item_id = i["id"]
            item_name = items[item_id]["name"]
            entry = f"{item_id}:{item_name} ({i['x']},{i['y']})"
            entries.append(entry)
        self.items_listbox_var.set(entries)

        self.fill_fields(items)

        self.btn = uiw.uiButton(
            master=self.frame, text="Select", command=self.select
        )

        self.name_label.grid(row=0, column=0, sticky="ew")
        self.name_entry.frame.grid(row=0, column=1, sticky="ew")
        self.type_label.grid(row=1, column=0, sticky="ew")
        self.type_combo.grid(row=1, column=1, sticky="ew")
        self.points_label.grid(row=2, column=0, sticky="ew")
        self.points_entry.frame.grid(row=2, column=1, sticky="ew")
        self.items_label.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.items_listbox.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.btn.grid(row=5, column=0, columnspan=2)

        self.top.wait_visibility()
        self.top.grab_set()
        self.top.wait_window(
            self.top
        )  # wait for itself destroyed, so like a modal dialog

    def fill_fields(self, items):
        if self.cur_trigger is not None:
            self.name_entry.entry.delete(0, tk.END)
            self.points_entry.entry.delete(0, tk.END)
            self.name_entry.entry.insert(0,self.cur_trigger["name"])
            self.type_combo.set(self.cur_trigger["type"])
            self.points_entry.entry.insert(0, self.cur_trigger["points"])

            for item_id in self.cur_trigger["item_ids"]:
                for i, entry in enumerate(self.items_listbox.get(0, tk.END)):
                    _id, _name = entry.split(":")
                    if item_id == _id:
                        self.items_listbox.select_set(i)
                        self.items_listbox.activate(i)
                        break

    def verify(self):

        if len(self.name_var) == 0:
            tk.messagebox.showwarning(
                "Error", "Missing a name for the new trigger. Names are descriptive. They do not have to be unique."
            )
            return False

        try:
            self.points_var = int(self.points_var)
        except ValueError:
            tk.messagebox.showwarning(
                "Error", "Missing a valid integer value for the points awarded by this trigger."
            )
            return False


        if self.type_var == "ITEM_AT_ITEM":
            if len(self.item_ids) == 2:
                return True
            else:
                tk.messagebox.showwarning(
                    "Error", "ITEM_AT_ITEM triggers must have exactly 2 items selected."
                )
                return False
        elif self.type_var == "OBJECT_AT_ITEM":
            if len(self.item_ids) == 1:
                return True
            else:
                tk.messagebox.showwarning(
                    "Error", "OBJECT_AT_ITEM triggers must have exactly 1 item selected."
                )
                return False
        else:
            return False

    def destroy(self):
        self.top.destroy()

    def select(self):
        self.name_var = self.name_entry.entry.get()
        self.type_var = self.type_combo.get()
        self.points_var = self.points_entry.entry.get()
        self.item_ids.clear()
        selected_items = self.items_listbox.curselection()
        for i in selected_items:
            item_entry = self.items_listbox.get(i)
            item_id, item_data = item_entry.split(":")
            self.item_ids.append(item_id)
        if self.verify():
            self.destroy()
        else:
            self.top.lift()
            self.top.attributes('-topmost',True)
            self.top.after_idle(self.top.attributes,'-topmost',False)

    def get_result(self):
        if self.verify():
            return {
                "name":self.name_var,
                "type":self.type_var,
                "points":self.points_var,
                "item_ids":self.item_ids
            }
        else:
            return None

class UIMapConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        """Sets window and frame information and calls function to build ui"""
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.logger = logger
        self.ldr = ldr

        self.add_remove_var = AddRemove.Info

        # Possible general config parameters.
        self.cell_size = 32  # in pixels

        # in pixels, the area around the map where row/column
        # labels are drawn.
        self.border_size = 32
        self.map_obj_char_size = 24  # font size
        self.map_item_char_size = 10  # font size

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

        self.bind("<<ShowFrame>>", self.reload_ui)

    def build_ui(self):
        """Generates UI of map

        Sets map info, generates canvas, draws tiles,
        draws placed objects, draws placed items, draws
        ai-controlled objects
        """
        self.main_frame = uiw.uiQuietFrame(master=self)
        self.left_frame = uiw.uiScrollFrame(master=self.main_frame)
        self.map_selection_frame = uiw.uiLabelFrame(
            master=self.left_frame.sub_frame, text="Maps"
        )
        self.map_container_frame = uiw.uiQuietFrame(master=self.main_frame)
        self.map_frame = uiw.uiQuietFrame(master=self.map_container_frame)
        # self.map_data_frame = uiScrollFrame(master=self.left_frame)
        self.map_info_frame = uiw.uiLabelFrame(
            master=self.left_frame.sub_frame, text="Map Info"
        )
        self.side_frame = uiw.uiLabelFrame(
            master=self.left_frame.sub_frame, text="Sides"
        )
        self.paint_frame = uiw.uiQuietFrame(master=self.main_frame)
        self.add_remove_frame = uiw.uiQuietFrame(master=self.paint_frame)
        self.obj_selection_frame = uiw.uiLabelFrame(
            master=self.paint_frame, text="Objects"
        )
        self.item_selection_frame = uiw.uiLabelFrame(
            master=self.paint_frame, text="Items"
        )
        self.button_row = uiw.uiQuietFrame(master=self.main_frame)
        self.title_label = uiw.uiLabel(
            master=self.main_frame, text="Map Configuration"
        )

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.left_frame.pack(side=tk.LEFT, fill="y", expand=False)
        self.map_container_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # self.map_data_frame.pack(side=tk.TOP, fill="y")
        self.map_selection_frame.pack(side=tk.TOP, fill="y")
        self.map_selection_frame.rowconfigure(0, weight=1)
        self.map_info_frame.pack(side=tk.TOP, fill="y")
        self.map_info_frame.rowconfigure(0, weight=1)
        self.side_frame.pack(side=tk.TOP, fill="y")
        self.side_frame.rowconfigure(0, weight=1)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.paint_frame.pack(side=tk.RIGHT, fill="y", before=self.map_frame)
        self.add_remove_frame.pack(side=tk.TOP, fill="x")
        self.add_remove_frame.rowconfigure(0, weight=1)
        self.add_remove_frame.columnconfigure(0, weight=1)
        self.obj_selection_frame.pack(side=tk.TOP, fill="y", expand=True)
        self.obj_selection_frame.rowconfigure(0, weight=1)
        self.item_selection_frame.pack(side=tk.TOP, fill="y", expand=True)
        self.item_selection_frame.rowconfigure(0, weight=1)

        # MAP SELECTION
        self.map_select_listbox_var = tk.StringVar()
        self.map_select_listbox = uiw.uiListBox(
            master=self.map_selection_frame,
            listvariable=self.map_select_listbox_var,
            selectmode="single",
        )
        self.map_select_listbox.grid(row=0, column=0, sticky="ew")
        self.map_select_listbox.bind("<<ListboxSelect>>", self.show_map)

        # MAP INFO
        # self.map_info_frame.columnconfigure(1,weight=1)

        self.map_id_label = uiw.uiLabel(master=self.map_info_frame, text="ID")
        self.map_id_entry = uiw.EntryHelp(
            master=self.map_info_frame, text="The unique ID of the map."
        )
        self.map_name_label = uiw.uiLabel(
            master=self.map_info_frame, text="Name"
        )
        self.map_name_entry = uiw.EntryHelp(
            master=self.map_info_frame,
            text="The name of the map (does not have to be unique).",
        )
        self.map_desc_label = uiw.uiLabel(
            master=self.map_info_frame, text="Description"
        )
        self.map_desc_text = uiw.uiTextbox(master=self.map_info_frame)
        self.map_desc_text.configure(width=16, height=5, state=tk.NORMAL)
        self.map_width_label = uiw.uiLabel(
            master=self.map_info_frame, text="Width"
        )
        self.map_width_entry = uiw.EntryHelp(
            master=self.map_info_frame,
            text="The playable width of the map in number of cells. NOTE: "
            + "The actual width will be two greater to compensate for the "
            + "edges."
        )
        self.map_height_label = uiw.uiLabel(
            master=self.map_info_frame, text="Height"
        )
        self.map_height_entry = uiw.EntryHelp(
            master=self.map_info_frame,
            text="The playable height of the map in number of cells. NOTE: "
            + "The actual width will be two greater to compensate for the "
            + "edges."
        )
        self.map_edge_id_label = uiw.uiLabel(
            master=self.map_info_frame, text="Edge Obj ID"
        )
        self.map_edge_id_entry = uiw.EntryHelp(
            master=self.map_info_frame,
            text="The ID of the object at the outer edge of the map. "
            + "This should be an indestructible object. Copies of this object "
            + "will be added automatically to fence in the playable area."
        )

        self.map_id_label.grid(row=0, column=0, sticky="ew")
        self.map_id_entry.frame.grid(row=0, column=1, sticky="ew")
        self.map_name_label.grid(row=1, column=0, sticky="ew")
        self.map_name_entry.frame.grid(row=1, column=1, sticky="ew")
        self.map_width_label.grid(row=2, column=0, sticky="ew")
        self.map_width_entry.frame.grid(row=2, column=1, sticky="ew")
        self.map_height_label.grid(row=3, column=0, sticky="ew")
        self.map_height_entry.frame.grid(row=3, column=1, sticky="ew")
        self.map_desc_label.grid(row=4, column=0, columnspan=2, sticky="ew")
        self.map_desc_text.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.map_edge_id_label.grid(row=6, column=0, sticky="ew")
        self.map_edge_id_entry.frame.grid(row=6, column=1, sticky="ew")

        # SIDE INFO
        # self.side_frame.columnconfigure(0,weight=1)
        self.side_select_listbox_var = tk.StringVar()
        self.side_select_listbox = uiw.uiListBox(
            master=self.side_frame,
            listvariable=self.side_select_listbox_var,
            selectmode="single",
        )
        self.side_select_listbox.bind("<<ListboxSelect>>", self.show_side)

        self.side_id_label = uiw.uiLabel(master=self.side_frame, text="ID")
        self.side_id_entry = uiw.EntryHelp(
            master=self.side_frame,
            text="A side is a placeholder for a team of agents. Each side "
            + "must have a unique ID.",
        )
        self.side_name_label = uiw.uiLabel(master=self.side_frame, text="Name")
        self.side_name_entry = uiw.EntryHelp(
            master=self.side_frame,
            text="The name of the side. Names are used to distinguish sides "
            + "during match setup.",
        )
        self.side_num_agents_label = uiw.uiLabel(
            master=self.side_frame, text="Num. Agents"
        )
        self.side_num_agents_entry = uiw.EntryHelp(
            master=self.side_frame,
            text="The number of agents a team must have. Team size cannot "
            + "be larger than the number of starting locations. It can be "
            + "less if an asymmetric match is desired or if random placement is "
            + "enabled.",
        )
        self.side_color_label = uiw.uiLabel(
            master=self.side_frame, text="Color"
        )
        self.side_color_entry = uiw.EntryHelp(
            master=self.side_frame,
            text="The placement token color. This is only used on this "
            + "configuration screen to denote team ownership of agent "
            + "placement tokens. It will not recolor sprites. NOTE: colors "
            + "must be given as hex RGB values (e.g. #FFFFFF) or as a "
            + "recognized tkinter named color. Color strings are NOT "
            + "currently validated by MAIA.",
        )
        self.side_random_label = uiw.uiLabel(
            master=self.side_frame, text="Random"
        )
        self.side_random_entry = uiw.EntryHelp(
            master=self.side_frame,
            text="Are agents randomly assigned starting locations? "
            + "If 'true', agents will be randomly distributed over the "
            + "starting locations. If 'false, starting location is determined "
            + "by order. true, t, 1, yes, y eval to true. Everything else is "
            + "false.",
        )
        self.side_points_to_win_label = uiw.uiLabel(
            master=self.side_frame, text="Points to Win"
        )
        self.side_points_to_win_entry = uiw.EntryHelp(
            master=self.side_frame,
            text="This positive integer value specifies how many points "
            + "this team must score to win the match. All teams start with "
            + "zero points. Points are scored by damaging other agents or by "
            + "activating triggers."
        )

        # #####################################################################################
        # Trigger UI
        self.side_trigger_frame = uiw.uiLabelFrame(
            master=self.side_frame, text="Triggers"
        )
        self.side_trigger_frame.configure(
            padx=20, pady=20
        )

        self.side_trigger_listbox_var = tk.StringVar()
        self.side_trigger_listbox = uiw.uiListBox(
            master=self.side_trigger_frame,
            listvariable=self.side_trigger_listbox_var,
            selectmode='single'
        )

        self.side_add_trigger_button = uiw.uiButton(
            master=self.side_trigger_frame,
            text="Add Trigger",
            command=self.add_trigger
        )

        self.side_alter_trigger_button = uiw.uiButton(
            master=self.side_trigger_frame,
            text="Alter Trigger",
            command=self.alter_trigger
        )

        self.side_remove_trigger_button = uiw.uiButton(
            master=self.side_trigger_frame,
            text="Remove Trigger",
            command=self.remove_trigger
        )

        self.side_trigger_listbox.pack(side=tk.TOP, fill="x")
        self.side_add_trigger_button.pack(side=tk.TOP, fill="x")
        self.side_alter_trigger_button.pack(side=tk.TOP, fill="x")
        self.side_remove_trigger_button.pack(side=tk.TOP, fill="x")

        # #######################################################################################

        self.side_select_listbox.grid(
            row=0, column=0, columnspan=2, sticky="ew"
        )
        self.side_id_label.grid(row=1, column=0, sticky="ew")
        self.side_id_entry.frame.grid(row=1, column=1, sticky="ew")
        self.side_name_label.grid(row=2, column=0, sticky="ew")
        self.side_name_entry.frame.grid(row=2, column=1, sticky="ew")
        self.side_num_agents_label.grid(row=3, column=0, sticky="ew")
        self.side_num_agents_entry.frame.grid(row=3, column=1, sticky="ew")
        self.side_color_label.grid(row=4, column=0, sticky="ew")
        self.side_color_entry.frame.grid(row=4, column=1, sticky="ew")
        self.side_random_label.grid(row=5, column=0, sticky="ew")
        self.side_random_entry.frame.grid(row=5, column=1, sticky="ew")
        self.side_points_to_win_label.grid(row=6, column=0, sticky="ew")
        self.side_points_to_win_entry.frame.grid(row=6, column=1, sticky="ew")
        self.side_trigger_frame.grid(row=7, column=0, columnspan=2, sticky="ew")

        self.side_new_button = uiw.uiButton(
            master=self.side_frame, command=self.new_side, text="Create Side"
        )
        self.side_new_button.grid(row=8, column=0, columnspan=2, sticky="ew")
        self.side_update_button = uiw.uiButton(
            master=self.side_frame,
            command=self.update_side,
            text="Update Side"
        )
        self.side_update_button.grid(
            row=9, column=0, columnspan=2, sticky="ew"
        )
        self.side_delete_button = uiw.uiCarefulButton(
            master=self.side_frame,
            command=self.delete_side,
            text="Delete Side"
        )
        self.side_delete_button.grid(
            row=10, column=0, columnspan=2, sticky="ew"
        )

        # OBJ SELECTION
        self.add_obj_button = uiw.uiButton(
            master=self.add_remove_frame,
            command=self.toggle_add_obj,
            text="Add Object",
            bg="red",
        )
        self.add_obj_button.config(bg="red")
        self.add_obj_button.grid(row=1, column=0, sticky="ew")
        self.remove_obj_button = uiw.uiButton(
            master=self.add_remove_frame,
            command=self.toggle_remove_obj,
            text="Remove Object",
        )
        self.remove_obj_button.config(bg="red")
        self.remove_obj_button.grid(row=2, column=0, sticky="ew")

        self.add_item_button = uiw.uiButton(
            master=self.add_remove_frame,
            command=self.toggle_add_item,
            text="Add Item",
            bg="red",
        )
        self.add_item_button.config(bg="red")
        self.add_item_button.grid(row=3, column=0, sticky="ew")
        self.remove_item_button = uiw.uiButton(
            master=self.add_remove_frame,
            command=self.toggle_remove_item,
            text="Remove Item",
        )
        self.remove_item_button.config(bg="red")
        self.remove_item_button.grid(row=4, column=0, sticky="ew")

        self.add_start_button = uiw.uiButton(
            master=self.add_remove_frame,
            command=self.toggle_add_start,
            text="Add Start",
            bg="red",
        )
        self.add_start_button.config(bg="red")
        self.add_start_button.grid(row=5, column=0, sticky="ew")
        self.remove_start_button = uiw.uiButton(
            master=self.add_remove_frame,
            command=self.toggle_remove_start,
            text="Remove Start",
        )
        self.remove_start_button.config(bg="red")
        self.remove_start_button.grid(row=6, column=0, sticky="ew")

        self.draw_label = uiw.uiLabel(
            master=self.add_remove_frame, text="Toggle Add or Remove"
        )
        self.draw_label.grid(row=0, column=0, sticky="ew")
        self.draw_label.columnconfigure(0, weight=1)
        self.obj_select_listbox_var = tk.StringVar()
        self.obj_select_listbox = uiw.uiListBox(
            master=self.obj_selection_frame,
            listvariable=self.obj_select_listbox_var,
            selectmode="single",
        )
        self.obj_select_listbox.bind("<<ListboxSelect>>", self.object_clicked)
        self.obj_select_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.item_select_listbox_var = tk.StringVar()
        self.item_select_listbox = uiw.uiListBox(
            master=self.item_selection_frame,
            listvariable=self.item_select_listbox_var,
            selectmode="single",
        )
        self.item_select_listbox.bind("<<ListboxSelect>>", self.item_clicked)
        self.item_select_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # BUTTON ROW
        self.map_create_button = uiw.uiButton(
            master=self.button_row, command=self.create_map, text="New Map"
        )
        self.map_create_button.pack(side=tk.LEFT)
        self.map_update_button = uiw.uiButton(
            master=self.button_row, command=self.update_map, text="Update Map"
        )
        self.map_update_button.pack(side=tk.LEFT)
        self.map_delete_button = uiw.uiCarefulButton(
            master=self.button_row, command=self.delete_map, text="Delete Map"
        )
        self.map_delete_button.pack(side=tk.LEFT)
        self.home_button = uiw.uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiw.uiCarefulButton(
            master=self.button_row,
            command=self.save_to_json,
            text="Save Map to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

    def reload_ui(self, event=None):
        self.populate_map_listbox()
        self.populate_obj_listbox()
        self.populate_item_listbox()

    def all_toggles_red(self):
        self.add_obj_button.config(bg="red")
        self.remove_obj_button.config(bg="red")
        self.add_item_button.config(bg="red")
        self.remove_item_button.config(bg="red")
        self.add_start_button.config(bg="red")
        self.remove_start_button.config(bg="red")

    def toggle_add_obj(self):
        self.all_toggles_red()
        if self.add_remove_var == AddRemove.AddObject:
            self.add_remove_var = AddRemove.Info
        else:
            self.add_remove_var = AddRemove.AddObject
            self.add_obj_button.config(bg="green")

    def toggle_remove_obj(self):
        self.all_toggles_red()
        if self.add_remove_var == AddRemove.DelObject:
            self.add_remove_var = AddRemove.Info
        else:
            self.add_remove_var = AddRemove.DelObject
            self.remove_obj_button.config(bg="green")

    def toggle_add_item(self):
        self.all_toggles_red()
        if self.add_remove_var == AddRemove.AddItem:
            self.add_remove_var = AddRemove.Info
        else:
            self.add_remove_var = AddRemove.AddItem
            self.add_item_button.config(bg="green")

    def toggle_remove_item(self):
        self.all_toggles_red()
        if self.add_remove_var == AddRemove.DelItem:
            self.add_remove_var = AddRemove.Info
        else:
            self.add_remove_var = AddRemove.DelItem
            self.remove_item_button.config(bg="green")

    def toggle_add_start(self):
        self.all_toggles_red()
        if self.add_remove_var == AddRemove.AddStart:
            self.add_remove_var = AddRemove.Info
        else:
            self.add_remove_var = AddRemove.AddStart
            self.add_start_button.config(bg="green")

    def toggle_remove_start(self):
        self.all_toggles_red()
        if self.add_remove_var == AddRemove.DelStart:
            self.add_remove_var = AddRemove.Info
        else:
            self.add_remove_var = AddRemove.DelStart
            self.remove_start_button.config(bg="green")

    def populate_map_listbox(self):

        self.map_select_listbox.delete(0, tk.END)
        map_data = self.ldr.get_map_templates()
        entries = []
        for m in map_data.values():
            entry = f"{m['id']}:{m['name']}"
            entries.append(entry)
        self.map_select_listbox_var.set(entries)

    def populate_obj_listbox(self):

        self.obj_select_listbox.delete(0, tk.END)
        obj_data = self.ldr.get_obj_templates()
        entries = []
        for o in obj_data.values():
            entry = f"{o['id']}:{o['name']}"
            entries.append(entry)
        self.obj_select_listbox_var.set(entries)

    def populate_item_listbox(self):

        self.item_select_listbox.delete(0, tk.END)
        item_data = self.ldr.get_item_templates()
        entries = []
        for i in item_data.values():
            entry = f"{i['id']}:{i['name']}"
            entries.append(entry)
        self.item_select_listbox_var.set(entries)

    def object_clicked(self, event=None):
        self.item_select_listbox.selection_clear(0, tk.END)

    def item_clicked(self, event=None):
        self.obj_select_listbox.selection_clear(0, tk.END)

    def create_map(self):
        map_data = self.ldr.get_map_templates()
        good_id = False
        while not good_id:
            map_id = tk.simpledialog.askstring(
                "New Map ID",
                "Please enter a unique ID for the new map.\nThe map will "
                + "be populated with default data. Use the 'Update Map' "
                + "button to further customize the map.",
            )
            if len(map_id) == 0:
                tk.messagebox.showwarning(
                    "Error",
                    "You must enter a non-empty map ID."
                )
            elif map_id in map_data.keys():
                tk.messagebox.showwarning(
                    "Error", "This ID already exists, please enter a new ID."
                )
            else:
                good_id = True

            new_map_data = {
                "id": map_id,
                "name": "NO NAME",
                "width": 10,
                "height": 10,
                "edge_obj_id": "",
                "desc": "",
                "objects": [],
                "items": [],
                "sides": {},
            }

            map_data.update({map_id: new_map_data})
            self.populate_map_listbox()

    def verify_new_map_size(self, cur_map, new_height, new_width):
        for obj in cur_map["objects"]:
            x = obj["x"]
            y = obj["y"]
            if x < 1 or y < 1 or x >= new_width or y >= new_height:
                return False
        for itm in cur_map["items"]:
            x = itm["x"]
            y = itm["y"]
            if x < 1 or y < 1 or x >= new_width or y >= new_height:
                return False
        for side in cur_map["sides"].values():
            for start in side["starting_locations"]:
                x = start["x"]
                y = start["y"]
                if x < 1 or y < 1 or x >= new_width or y >= new_height:
                    return False

        return True

    def update_map(self):

        cur_map = self.get_currently_selected_map()
        if cur_map is not None:
            map_data = self.ldr.get_map_templates()
            map_id = self.map_id_entry.entry.get()
            if map_id != cur_map["id"]:
                if map_id in map_data.keys():
                    tk.messagebox.showwarning(
                        "Duplicate Map ID",
                        "The new map ID already exists. Map IDs must be "
                        + "unique. No changes have been made to the map.",
                    )
                    return
                else:
                    old_id = cur_map["id"]
                    cur_map["id"] = map_id
                    del map_data[old_id]
                    map_data[map_id] = cur_map
            map_name = self.map_name_entry.entry.get()
            if map_name != cur_map["name"]:
                if len(map_name) > 0:
                    cur_map["name"] = map_name
                else:
                    tk.messagebox.showwarning(
                        "Empty Name",
                        "Map name cannot be empty."
                    )
            map_desc = self.map_desc_text.get(1.0, tk.END)
            cur_map["desc"] = map_desc.strip()
            map_width = self.map_width_entry.entry.get()
            map_height = self.map_height_entry.entry.get()
            try:
                map_width = int(map_width)
                map_height = int(map_height)
                if map_width < 1 or map_height < 1:
                    raise Exception("New height or width is less than 1.")
                else:
                    good = self.verify_new_map_size(
                        cur_map, map_width, map_height
                    )
                    if good:
                        cur_map["width"] = map_width
                        cur_map["height"] = map_height
                    else:
                        raise Exception(
                            "There are objects, items or starting locations "
                            + "outside the new map bounds. You will need "
                            + "to move or remove them before resizing the map."
                        )
            except Exception as e:
                tk.messagebox.showwarning(
                    "Invalid Map Width or Height",
                    f"{e} {map_width} {map_height}"
                )

            map_edge_obj_id = self.map_edge_id_entry.entry.get()
            edge_obj = self.ldr.get_obj_template(map_edge_obj_id)
            if edge_obj is not None:
                cur_map["edge_obj_id"] = map_edge_obj_id
            else:
                tk.messagebox.showwarning(
                    "Invalid Map Edge Object",
                    "The edge object ID must be a legitimate object ID.",
                )

            self.populate_map_listbox()

            for i, map_entry in enumerate(
                self.map_select_listbox.get(0, tk.END)
            ):
                map_id, map_name = map_entry.split(":")
                if map_id == cur_map["id"]:
                    self.map_select_listbox.selection_clear(0, tk.END)
                    self.map_select_listbox.selection_set(i)
                    self.map_select_listbox.activate(i)
                    self.show_map()

    def delete_map(self):
        cur_map = self.get_currently_selected_map()
        if cur_map is not None:
            self.ldr.delete_map(cur_map["id"])
            self.populate_map_listbox()

    def goto_home(self):
        self.controller.show_frame("home_page")

    def save_to_json(self):
        self.ldr.save_map_templates()

    def add_trigger(self):
        cur_side = self.get_currently_selected_side()
        if cur_side is not None:
            cur_map = self.get_currently_selected_map()
            items_on_map = cur_map["items"]
            dialog = UITrigger(self.ldr.get_item_templates(), items_on_map)
            result = dialog.get_result()
            if result is not None:
                cur_side["triggers"].append(result)
            self.show_triggers(cur_side)

    def alter_trigger(self):
        cur_trigger = self.get_currently_selected_trigger()
        if cur_trigger is not None:
            cur_side = self.get_currently_selected_side()
            cur_map = self.get_currently_selected_map()
            items_on_map = cur_map["items"]
            dialog = UITrigger(self.ldr.get_item_templates(), items_on_map, cur_trigger)
            result = dialog.get_result()
            if result is not None:
                cur_trigger["type"] = result["type"]
                cur_trigger["name"] = result["name"]
                cur_trigger["points"] = result["points"]
                cur_trigger["item_ids"] = result["item_ids"]
            self.show_triggers(cur_side)

    def remove_trigger(self):
        trigger_index = self.side_trigger_listbox.curselection()
        if len(trigger_index) == 1:
            cur_side = self.get_currently_selected_side()
            triggers = cur_side["triggers"]
            del triggers[trigger_index[0]]
            self.show_triggers(cur_side)

    def new_side(self, event=None):
        cur_map = self.get_currently_selected_map()
        if cur_map is not None:
            sides = cur_map["sides"]
            side_id = tk.simpledialog.askstring(
                "New Side ID", "Enter a new side ID. It must be unique."
            )
            if side_id is not None:
                if len(side_id) == 0:
                    tk.messagebox.showwarning(
                        "Invalid Side ID", "A side ID cannot be empty."
                    )
                elif side_id in sides:
                    tk.messagebox.showwarning(
                        "Invalid Side ID",
                        "A side ID must be unique. There is already a "
                        + f"side with the ID {side_id}.",
                    )
                else:
                    new_side = {
                        "id": side_id,
                        "color": "#000000",
                        "name": side_id,
                        "num_agents": 0,
                        "random_placement": False,
                        "starting_locations": [],
                        "points_to_win":0,
                        "triggers":[]
                    }
                    sides[side_id] = new_side
                    self.show_map_info(cur_map)
                    self.select_side(side_id)

    def update_side(self, event=None):
        side = self.get_currently_selected_side()
        if side is not None:
            cur_map = self.get_currently_selected_map()
            # Name
            side_name = self.side_name_entry.entry.get()
            if len(side_name) == 0:
                tk.messagebox.showwarning(
                    "Invalid Side Name", "A side name cannot be empty."
                )
            else:
                side["name"] = side_name

            # Num agents
            num_agents = self.side_num_agents_entry.entry.get()
            try:
                num_agents = int(num_agents)
                if num_agents < 0:
                    tk.messagebox.showwarning(
                        "Invalid Number of Agents",
                        "The number of agents cannot be negative.",
                    )
                else:
                    side["num_agents"] = num_agents
            except Exception:
                tk.messagebox.showwarning(
                    "Invalid Number of Agents",
                    "The value provided cannot be cast to an integer.",
                )

            # Color - There are no checks.
            color = self.side_color_entry.entry.get()
            side["color"] = color

            # Random placement
            rand_placement = self.side_random_entry.entry.get()
            side["random_placement"] = zfunctions.to_bool(rand_placement)

            # Points to win
            points_to_win = self.side_points_to_win_entry.entry.get()
            side["points_to_win"] = points_to_win

            # ID
            side_id = self.side_id_entry.entry.get()
            if side_id != side["id"]:

                sides = cur_map["sides"]
                if len(side_id) == 0:
                    tk.messagebox.showwarning(
                        "Invalid Side ID", "A side ID cannot be empty."
                    )
                elif side_id in sides:
                    tk.messagebox.showwarning(
                        "Invalid Side ID",
                        "A side ID must be unique. There is already a side "
                        + f"with the ID {side_id}.",
                    )
                else:
                    for k, v in sides.items():
                        if v["id"] == side["id"]:
                            del sides[v["id"]]
                            break
                    side["id"] = side_id
                    sides[side_id] = side

            self.show_side_entries(cur_map)
            self.select_side(side["id"])

    def delete_side(self, event=None):
        cur_side = self.get_currently_selected_side()
        if cur_side is not None:
            cur_map = self.get_currently_selected_map()
            sides = cur_map["sides"]
            for side_id, side in sides.items():
                if side["id"] == cur_side["id"]:
                    del sides[side_id]
                    break
            self.show_side_entries(cur_map)

    def get_currently_selected_map(self):
        map_index = self.map_select_listbox.curselection()
        if len(map_index) == 1:
            map_entry = self.map_select_listbox.get(map_index[0])
            map_id, map_name = map_entry.split(":")
            return self.ldr.get_map_template(map_id)
        else:
            return None

    def get_currently_selected_side(self):
        side_index = self.side_select_listbox.curselection()
        if len(side_index) == 1:
            side_entry = self.side_select_listbox.get(side_index[0])
            side_id, side_name = side_entry.split(":")
            cur_map = self.get_currently_selected_map()
            if cur_map is not None:
                return cur_map["sides"][side_id]
            else:
                return None
        else:
            return None

    def get_currently_selected_trigger(self):
        cur_side = self.get_currently_selected_side()
        if cur_side is not None:
            trigger_index = self.side_trigger_listbox.curselection()
            if len(trigger_index) == 1:
                triggers = cur_side["triggers"]
                return triggers[trigger_index[0]]
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

    def select_side(self, _id):

        for i, side_entry in enumerate(
            self.side_select_listbox.get(0, tk.END)
        ):
            side_id, side_name = side_entry.split(":")
            if side_id == _id:
                self.side_select_listbox.selection_clear(0, tk.END)
                self.side_select_listbox.selection_set(i)
                self.side_select_listbox.activate(i)
                self.show_side()

    def clear_map_info(self):
        self.map_id_entry.entry.delete(0, tk.END)
        self.map_name_entry.entry.delete(0, tk.END)
        self.map_desc_text.delete(1.0, tk.END)
        self.map_width_entry.entry.delete(0, tk.END)
        self.map_height_entry.entry.delete(0, tk.END)
        self.map_edge_id_entry.entry.delete(0, tk.END)
        self.side_select_listbox.delete(0, tk.END)

    def show_map_info(self, cur_map):
        self.clear_map_info()

        self.map_id_entry.entry.insert(0, cur_map["id"])
        self.map_name_entry.entry.insert(0, cur_map["name"])
        self.map_desc_text.insert(1.0, cur_map["desc"])
        self.map_width_entry.entry.insert(0, cur_map["width"])
        self.map_height_entry.entry.insert(0, cur_map["height"])
        self.map_edge_id_entry.entry.insert(0, cur_map["edge_obj_id"])

        self.show_side_entries(cur_map)

    def show_side_entries(self, cur_map):
        self.clear_side()
        # Add sides to the side listbox
        side_entries = []
        for side_id, side in cur_map["sides"].items():
            entry = f"{side['id']}:{side['name']}"
            side_entries.append(entry)
        self.side_select_listbox_var.set(side_entries)

    def show_map(self, event=None):

        if self.canvas is not None:
            self.canvas.destroy()
            self.x_bar.destroy()
            self.y_bar.destroy()
            self.canvas = None
            self.x_bar = None
            self.y_bar = None
            # self.cur_map = None

        cur_map = self.get_currently_selected_map()
        if cur_map is not None:

            self.show_map_info(cur_map)

            # Get map attributes
            map_width = cur_map["width"]
            map_height = cur_map["height"]

            self.char_offset = (self.cell_size - self.map_obj_char_size) / 2
            self.map_obj_font = tk.font.Font(
                family="TkFixedFont", size=self.map_obj_char_size
            )
            self.map_item_font = tk.font.Font(
                family="TkFixedFont", size=self.map_item_char_size
            )

            self.x_bar = tk.Scrollbar(self.map_frame, orient=tk.HORIZONTAL)
            self.y_bar = tk.Scrollbar(self.map_frame, orient=tk.VERTICAL)
            self.canvas = uiw.uiCanvas(
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
            self.canvas.bind("<Button-1>", self.map_mouse_click)

            self.draw_tiles(map_width, map_height)
            self.draw_rc_labels(map_width, map_height)
            self.draw_objects(cur_map)
            self.draw_edge_objs(cur_map)
            self.draw_starting_locations(cur_map)
            self.draw_items(cur_map)

    def clear_side(self):
        self.side_id_entry.entry.delete(0, tk.END)
        self.side_name_entry.entry.delete(0, tk.END)
        self.side_num_agents_entry.entry.delete(0, tk.END)
        self.side_color_entry.entry.delete(0, tk.END)
        self.side_random_entry.entry.delete(0, tk.END)
        self.side_points_to_win_entry.entry.delete(0, tk.END)


    def show_side(self, event=None):
        self.clear_side()
        cur_side = self.get_currently_selected_side()
        if cur_side is not None:
            self.side_id_entry.entry.insert(0, cur_side["id"])
            self.side_name_entry.entry.insert(0, cur_side["name"])
            self.side_num_agents_entry.entry.insert(0, cur_side["num_agents"])
            self.side_color_entry.entry.insert(0, cur_side["color"])
            self.side_random_entry.entry.insert(
                0, cur_side["random_placement"]
            )
            self.side_points_to_win_entry.entry.insert(
                0, cur_side["points_to_win"]
            )
            self.show_triggers(cur_side)

    def clear_triggers(self):
        self.side_trigger_listbox.delete(0, tk.END)

    def show_triggers(self, cur_side):
        self.clear_triggers()
        trigger_entries = []
        for i, t in enumerate(cur_side["triggers"]):
            entry = f"{i}:{t['name']}"
            trigger_entries.append(entry)
        self.side_trigger_listbox_var.set(trigger_entries)

    def map_mouse_click(self, event):
        """
        Handles a mouse click on the map canvas.

        What happens on a click depends on which (if any) of the add/remove
        toggle buttons are green (on).

        There are certain restrictions.

        Only 1 object can be in a cell.

        Only 1 starting location can be in
        a cell. A cell cannot contain an object AND starting location because
        starting locations will be filled (potentially) with agent objects when
        the sim starts.

        Items and objects can occupy the same location.

        There is no limit on the number of items in a cell; however, each item
        can only be on the map once.
        """
        cur_map = self.get_currently_selected_map()
        if cur_map is None:
            return

        x, y = self.canvas.mousexy_to_cellxy(event.x, event.y)
        if x >= 0 and y >= 0 \
                and x < cur_map["width"] and y < cur_map["height"]:

            # Find out what is in the cell, if anything.
            things = self.whats_in_cell_xy(cur_map, x, y)

            # Object
            if (
                self.add_remove_var == AddRemove.AddObject
                or self.add_remove_var == AddRemove.DelObject
            ):
                self.handle_add_remove_object(x, y, things, cur_map)

            # Item
            elif (
                self.add_remove_var == AddRemove.AddItem
                or self.add_remove_var == AddRemove.DelItem
            ):
                self.handle_add_remove_item(x, y, things, cur_map)

            # Starting location
            elif (
                self.add_remove_var == AddRemove.AddStart
                or self.add_remove_var == AddRemove.DelStart
            ):
                self.handle_add_remove_start(x, y, things, cur_map)

    def whats_in_cell_xy(self, cur_map, x, y):
        things = {
            "object_index": None,
            "item_indexes": [],
            "start_index": None
        }
        for i in range(len(cur_map["objects"])):
            obj = cur_map["objects"][i]
            if obj["x"] == x and obj["y"] == y:
                things["object_index"] = i
                break

        for i in range(len(cur_map["items"])):
            itm = cur_map["items"][i]
            if itm["x"] == x and itm["y"] == y:
                things["item_indexes"].append(i)

        side = self.get_currently_selected_side()
        if side is not None:
            for i in range(len(side["starting_locations"])):
                sl = side["starting_locations"][i]
                if sl["x"] == x and sl["y"] == y:
                    things["start_index"] = i
                    break

        return things

    def handle_add_remove_object(self, x, y, things, cur_map):
        if self.add_remove_var == AddRemove.AddObject:
            # If the cell has no obj or start loc already...
            if things["object_index"] is None \
                    and things["start_index"] is None:
                obj = self.get_currently_selected_obj()
                if obj is not None:
                    obj_entry = {"id": obj["id"], "x": x, "y": y}
                    cur_map["objects"].append(obj_entry)
                    self.canvas.draw_sprite(
                        x=x,
                        y=y,
                        uuid=f"{x}_{y}",
                        sprite_filename=obj["alive_sprite_filename"],
                        sprite_type="object"
                    )
        elif self.add_remove_var == AddRemove.DelObject:
            if things["object_index"] is not None:
                del cur_map["objects"][things["object_index"]]
                self.canvas.remove_obj(f"{x}_{y}")

    def handle_add_remove_item(self, x, y, things, cur_map):
        if self.add_remove_var == AddRemove.AddItem:
            itm = self.get_currently_selected_item()
            if itm is not None:

                for on_map_item in cur_map["items"]:
                    if on_map_item["id"] == itm["id"]:
                        tk.messagebox.showwarning(
                            "Error",
                            "A map cannot have more than one copy of an item."
                        )
                        return

                item_entry = {"id": itm["id"], "x": x, "y": y}
                cur_map["items"].append(item_entry)
                self.canvas.draw_sprite(
                    x=x,
                    y=y,
                    sprite_filename=itm["sprite_filename"],
                    uuid=f"{x}_{y}_{itm['id']}",
                    sprite_type="item",
                )
        elif self.add_remove_var == AddRemove.DelItem:
            if len(things["item_indexes"]) == 1:
                _id = cur_map["items"][things["item_indexes"][0]]["id"]
                del cur_map["items"][things["item_indexes"][0]]
                self.canvas.remove_item(f"{x}_{y}_{_id}")
            elif len(things["item_indexes"]) > 1:

                msg = f"The items present in cell {x},{y} are:\n"
                for index in things["item_indexes"]:
                    itm_map_entry = cur_map["items"][index]
                    itm = self.ldr.get_item_template(itm_map_entry["id"])
                    msg += f"[{index}] {itm['id']} {itm['name']}\n"
                msg += "\nGive number in the square brackets of the item "
                + "you wish to remove from the cell."

                index = tk.simpledialog.askinteger("Remove Item", msg)

                if index is not None and index in things["item_indexes"]:
                    _id = cur_map["items"][index]["id"]
                    del cur_map["items"][index]
                    self.canvas.remove_item(f"{x}_{y}_{_id}")
                else:
                    tk.messagebox.showwarning(
                        "Error", "Invalid index entered."
                    )
            else:
                pass
                # print("Nothing to delete")

    def handle_add_remove_start(self, x, y, things, cur_map):

        if self.add_remove_var == AddRemove.AddStart:
            side = self.get_currently_selected_side()
            # If a side is selected, and...
            if side is not None:
                # There isn't already a start or obj in this cell...
                if things["start_index"] is None and \
                        things["object_index"] is None:
                    facing = tk.simpledialog.askinteger(
                        "Enter Facing",
                        "The direction (in degrees) will the agent face "
                        + "when the match starts [0, 360)? 0 degrees faces "
                        + "east. Positive values rotate counter clockwise:\n"
                        + "0 - East\n"
                        + "90 - North\n"
                        + "180 - West\n"
                        + "270 - South"
                    )

                    if facing < 0 or facing > 360:
                        tk.messagebox.showwarning(
                            "Error", "Facing must be 0 to 360 degrees."
                        )
                    else:
                        start = {"x": x, "y": y, "facing": float(facing)}
                        index = len(side["starting_locations"])
                        side["starting_locations"].append(start)
                        self.canvas.draw_starting_location(
                            x, y, index, side["color"]
                        )

        elif self.add_remove_var == AddRemove.DelStart:
            side = self.get_currently_selected_side()

            if side is not None:
                if things["start_index"] is not None:
                    for i, sl in enumerate(side["starting_locations"]):
                        if sl["x"] == x and sl["y"] == y:
                            del side["starting_locations"][i]
                            self.canvas.remove_all_starting_locations()
                            self.draw_starting_locations(cur_map)
                            break
            else:
                tk.messagebox.showwarning(
                    "Error",
                    "You must select a side to remove a starting location."
                )

    def draw_tiles(self, width, height):
        """Draws tiles on canvas"""
        for x in range(width):
            for y in range(height):
                self.canvas.draw_tile(x=x, y=y, fill="#DDDDDD")

    def draw_rc_labels(self, width, height):
        """Draws tiles on canvas"""

        self.canvas.draw_row_labels(
            width=width, height=height, fill="#000000"
        )
        self.canvas.draw_column_labels(
            width=width, height=height, fill="#000000"
        )

    def draw_objects(self, cur_map):
        """Draws placed object on the map"""

        for obj_entry in cur_map["objects"]:

            _obj = self.ldr.get_obj_template(obj_entry["id"])
            x = obj_entry["x"]
            y = obj_entry["y"]
            sprite_filename = _obj["alive_sprite_filename"]
            self.canvas.draw_sprite(
                x=x,
                y=y,
                uuid=f"{x}_{y}",
                sprite_filename=sprite_filename,
                sprite_type="object",
            )

    def draw_edge_objs(self, cur_map):
        """
        Draws the edge objects
        """
        edge_obj_id = cur_map["edge_obj_id"]
        edge_obj = self.ldr.get_obj_template(edge_obj_id)
        if edge_obj is not None:
            map_width = cur_map["width"]
            map_height = cur_map["height"]
            sprite_filename = edge_obj["alive_sprite_filename"]

            # Draw top and bottom edges
            for x in range(map_width):
                self.canvas.draw_sprite(
                    x=x,
                    y=0,
                    uuid=f"{x}_{0}",
                    sprite_filename=sprite_filename,
                    sprite_type="object"
                )
                self.canvas.draw_sprite(
                    x=x,
                    y=map_height - 1,
                    uuid=f"{x}_{map_height - 1}",
                    sprite_filename=sprite_filename,
                    sprite_type="object",
                )

            # Draw left and right (minus the corner hexes)
            for y in range(1, map_height - 1):
                self.canvas.draw_sprite(
                    x=0,
                    y=y,
                    uuid=f"{0}_{y}",
                    sprite_filename=sprite_filename,
                    sprite_type="object"
                )
                self.canvas.draw_sprite(
                    x=map_width - 1,
                    y=y,
                    uuid=f"{map_width - 1}_{y}",
                    sprite_filename=sprite_filename,
                    sprite_type="object",
                )
        else:
            tk.messagebox.showwarning(
                "Warning",
                "This map does not have a valid edge object.\n\nEdge objects "
                + "define the edge of the map and prevent agents from moving "
                + "outside its bounds.\n\nTechnically, any object can be "
                + "used to define a map edge,\nbut it should be "
                + "indestructible (i.e. have a lot of health).",
            )

    def draw_items(self, cur_map):
        """Draws items on the map"""

        for item_entry in cur_map["items"]:

            itm = self.ldr.get_item_template(item_entry["id"])
            x = item_entry["x"]
            y = item_entry["y"]
            sprite_filename = itm["sprite_filename"]
            self.canvas.draw_sprite(
                x=x,
                y=y,
                uuid=f"{x}_{y}_{itm['id']}",
                sprite_filename=sprite_filename,
                sprite_type="item",
            )

    def draw_starting_locations(self, cur_map):
        """Adds ai-controlled object to obj list"""
        # Add possible team and ai-controlled obj locations
        sides = cur_map["sides"]

        for side in sides.values():
            color = side["color"]
            starting_locations = side["starting_locations"]

            for i in range(len(starting_locations)):
                loc = starting_locations[i]
                x = loc["x"]
                y = loc["y"]
                self.canvas.draw_starting_location(x, y, i, color)

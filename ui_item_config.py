import tkinter as tk
import ui_widgets as uiw


class UIItemConfig(tk.Frame):
    def __init__(self, controller, ldr, master=None, logger=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.configure(bg=uiw.BGCOLOR)
        self.logger = logger
        self.ldr = ldr
        self.build_ui()
        self.ui_map = None

    def validate_number_entry(self, input):
        """
        Validates each entered value (input) to ensure it is a number.
        """
        input.replace(".", "", 1)
        input.replace("-", "", 1)
        if input.isdigit() or input == "" or "-" in input or "." in input:
            return True

        else:
            return False

    def get_focused_entry(self):
        """
        Returns the currently focused entry in advanced config.
        """
        focused_entry = self.focus_get()
        return focused_entry

    def build_ui(self):
        """
        Initializes all widgets and places them.
        """
        # Make main frames

        self.main_frame = uiw.uiQuietFrame(master=self)
        self.item_selection_column = uiw.uiLabelFrame(
            master=self.main_frame, text="Items"
        )
        self.items_column = uiw.uiLabelFrame(
            master=self.main_frame, text="Item Info"
        )
        self.button_row = uiw.uiQuietFrame(master=self.main_frame)
        self.title_label = uiw.uiLabel(
            master=self.main_frame, text="Item Config"
        )
        self.validate_num = self.main_frame.register(
            self.validate_number_entry
        )

        # Place frames
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.title_label.pack(side=tk.TOP, fill="x")
        self.button_row.pack(side=tk.BOTTOM, fill="x")
        self.item_selection_column.pack(side=tk.LEFT, fill="y")
        self.items_column.pack(side=tk.LEFT, fill="y")

        # Item Selection Widgets
        self.select_item_listbox_var = tk.StringVar()
        self.select_item_listbox = uiw.uiListBox(
            master=self.item_selection_column,
            listvariable=self.select_item_listbox_var,
            selectmode="browse",
        )
        self.select_item_listbox.bind("<<ListboxSelect>>", self.show_item_info)
        self.select_item_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Item Info Widgets
        self.item_id_label = uiw.uiLabel(master=self.items_column, text="ID")
        self.item_id_entry = uiw.EntryHelp(
            master=self.items_column, text="The unique ID of the item."
        )
        self.item_name_label = uiw.uiLabel(
            master=self.items_column, text="Name"
        )
        self.item_name_entry = uiw.EntryHelp(
            master=self.items_column, text="The name of the item."
        )
        self.item_weight_label = uiw.uiLabel(
            master=self.items_column, text="Weight"
        )
        self.item_weight_entry = uiw.EntryHelp(
            master=self.items_column,
            text="The weight of the item. Weight (and bulk) are used to "
            + "determine whether an object (with the correct component) can "
            + "pick up an item."
        )
        self.item_bulk_label = uiw.uiLabel(
            master=self.items_column, text="Bulk"
        )
        self.item_bulk_entry = uiw.EntryHelp(
            master=self.items_column,
            text="The bulk (an abstract measure of side) of the item. "
            + "Bulk (and weight) are used to determine whether an object "
            + "(with the correct component) can pick up an item."
        )
        self.item_sprite_label = uiw.uiLabel(
            master=self.items_column, text="Sprite Filename"
        )
        self.item_sprite_entry = uiw.EntryHelp(
            master=self.items_column,
            text="The filename of the sprite used to display the item on "
            + "the map."
        )

        self.item_id_label.grid(row=0, column=0, sticky="ew")
        self.item_id_entry.frame.grid(row=0, column=1, sticky="ew")
        self.item_name_label.grid(row=1, column=0, sticky="ew")
        self.item_name_entry.frame.grid(row=1, column=1, sticky="ew")
        self.item_weight_label.grid(row=2, column=0, sticky="ew")
        self.item_weight_entry.frame.grid(row=2, column=1, sticky="ew")
        self.item_bulk_label.grid(row=3, column=0, sticky="ew")
        self.item_bulk_entry.frame.grid(row=3, column=1, sticky="ew")
        self.item_sprite_label.grid(row=4, column=0, sticky="ew")
        self.item_sprite_entry.frame.grid(row=4, column=1, sticky="ew")

        # Team Buttons

        self.new_item_button = uiw.uiButton(
            master=self.button_row,
            command=self.create_item,
            text="Create Item"
        )
        self.new_item_button.pack(side=tk.LEFT)
        self.update_item_button = uiw.uiButton(
            master=self.button_row,
            command=self.update_item,
            text="Update Item"
        )
        self.update_item_button.pack(side=tk.LEFT)
        self.delete_item_button = uiw.uiCarefulButton(
            master=self.button_row,
            command=self.delete_item,
            text="Delete Item"
        )
        self.delete_item_button.pack(side=tk.LEFT)

        # High-level Buttons
        self.home_button = uiw.uiButton(
            master=self.button_row, command=self.goto_home, text="Home"
        )
        self.home_button.pack(side=tk.RIGHT)
        self.save_to_json_button = uiw.uiCarefulButton(
            master=self.button_row,
            command=self.save_to_json,
            text="Save Items to JSON"
        )
        self.save_to_json_button.pack(side=tk.RIGHT)

        self.populate_item_listbox()

    def populate_item_listbox(self):
        """
        Gets information from the loader and assigns current values for each
        setting type.
        """
        self.clear_item_info()

        item_data = self.ldr.get_item_templates()

        item_entries = []
        for itm in item_data.values():
            entry = f"{itm['id']}:{itm['name']}"
            item_entries.append(entry)

        self.select_item_listbox.delete(0, tk.END)
        self.select_item_listbox_var.set(item_entries)

    def clear_item_info(self):
        self.item_id_entry.entry.delete(0, tk.END)
        self.item_name_entry.entry.delete(0, tk.END)
        self.item_weight_entry.entry.delete(0, tk.END)
        self.item_bulk_entry.entry.delete(0, tk.END)
        self.item_sprite_entry.entry.delete(0, tk.END)

    def show_item_info(self, event=None):
        """
        Updates the values stored in the item entry widgets.
        """
        self.clear_item_info()
        cur_item = self.get_currently_selected_item()
        if cur_item is not None:

            self.item_id_entry.entry.insert(0, cur_item["id"])
            self.item_name_entry.entry.insert(0, cur_item["name"])
            self.item_weight_entry.entry.insert(0, cur_item["weight"])
            self.item_bulk_entry.entry.insert(0, cur_item["bulk"])
            self.item_sprite_entry.entry.insert(0, cur_item["sprite_filename"])

    # CREATE NEW
    def create_item(self):
        """
        Creates a new item and adds it to the item dictionary.
        """

        item_data = self.ldr.get_item_templates()

        good_id = False
        while not good_id:
            item_id = tk.simpledialog.askstring(
                "New Item ID", "Please enter an ID for the new item."
            )
            if item_id is None:
                break
            elif len(item_id) == 0:
                tk.messagebox.showwarning(
                    "Invalid Item ID", "You must enter an item ID to continue"
                )
            elif item_id in item_data.keys():
                tk.messagebox.showwarning(
                    "Invalid Item ID",
                    "This ID already exists, please enter a new ID."
                )
            else:
                good_id = True

                new_item_data = {
                    "id": item_id,
                    "name": "",
                    "weight": 0,
                    "bulk": 0,
                    "sprite_filename": "",
                }
                item_data.update({item_id: new_item_data})
                self.populate_item_listbox()
                self.select_item(item_id)

    def select_item(self, _id):
        for i, entry in enumerate(self.select_item_listbox.get(0, tk.END)):
            item_id, item_name = entry.split(":")
            if item_id == _id:
                self.select_item_listbox.selection_clear(0, tk.END)
                self.select_item_listbox.selection_set(i)
                self.select_item_listbox.activate(i)
                self.show_item_info()
                break

    # UPDATE JSON FILES
    def update_item(self):
        """
        Updates the item's data with the loader.
        """
        item_data = self.ldr.get_item_templates()
        cur_item = self.get_currently_selected_item()
        if cur_item is not None:

            # ID
            new_id = self.item_id_entry.entry.get()
            if new_id != cur_item["id"]:
                if len(new_id) == 0:
                    tk.messagebox.showwarning(
                        "Invalid Item ID", "An item ID cannot be empty."
                    )
                elif new_id in item_data:
                    tk.messagebox.showwarning(
                        "Invalid Item ID",
                        "The new ID already exists. Item IDs must be unique.",
                    )
                else:
                    old_id = cur_item["id"]
                    cur_item["id"] = new_id
                    del item_data[old_id]
                    item_data[new_id] = cur_item

            # NAME
            new_name = self.item_name_entry.entry.get()
            if len(new_name) == 0:
                tk.messagebox.showwarning(
                    "Invalid Item Name", "Item names cannot be empty."
                )
            else:
                cur_item["name"] = new_name

            # WEIGHT
            new_weight = self.item_weight_entry.entry.get()
            try:
                new_weight = int(new_weight)
                cur_item["weight"] = new_weight
            except Exception:
                tk.messagebox.showwarning(
                    "Invalid Item Weight",
                    "The current weight cannot be cast to an integer.",
                )

            # BULK
            new_bulk = self.item_bulk_entry.entry.get()
            try:
                new_bulk = int(new_bulk)
                cur_item["bulk"] = new_bulk
            except Exception:
                tk.messagebox.showwarning(
                    "Invalid Item Bulk",
                    "The current bulk cannot be cast to an integer.",
                )

            # SPRITE: no checks
            new_sprite = self.item_sprite_entry.entry.get()
            cur_item["sprite_filename"] = new_sprite

            self.populate_item_listbox()

    # DELETE

    def delete_item(self):
        """
        Deletes the currently selected team from the JSON and team dictionary.
        """
        item_data = self.ldr.get_item_templates()
        cur_item = self.get_currently_selected_item()
        if cur_item is not None:
            del item_data[cur_item["id"]]
            self.populate_item_listbox()

    def get_currently_selected_item(self):
        item_index = self.select_item_listbox.curselection()
        if len(item_index) == 1:
            item_entry = self.select_item_listbox.get(item_index[0])
            item_id, item_name = item_entry.split(":")
            return self.ldr.get_item_template(item_id)
        else:
            return None

    def save_to_json(self):
        self.ldr.save_item_templates()

    def goto_home(self):
        self.controller.show_frame("home_page")

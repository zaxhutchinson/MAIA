##############################################################################
# UI WIDGETS
#
# Various custom tk widgets. Most of them just override default colors.
##############################################################################

import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
import tkinter.scrolledtext as scrolltext
import platform
from packages.tkmacosx import Button
from PIL import ImageTk, Image

import sprite_manager


BGCOLOR = "#E5E5E5"
TEXTCOLOR = "#222222"

BTN_DARK = "#495EA7"
BTN_LIGHT = "#FFFFFF"

CAREFUL_BTN_DARK = "red"

ENTRY_DARK = "#222222"
ENTRY_BG = "salmon1"

BOXFILLCOLOR = "#B2C1E3"

PADX=5
PADY=5

global_sprite_list = []

if platform.system() == "Darwin":
    FONT_SIZE = 16
else:
    FONT_SIZE = 12


class uiListBox(tk.Listbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, kwargs)
        if "selectmode" not in kwargs:
            kwargs["selectmode"]=tk.SINGLE
        self.config(
            selectmode=kwargs["selectmode"],
            bg=BOXFILLCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            relief=tk.FLAT,
            selectforeground=TEXTCOLOR,
            selectbackground=ENTRY_BG,
            exportselection=0,
            font=("Arial", FONT_SIZE),
        )


class uiScrollText(tk.scrolledtext.ScrolledText):
    def __init__(self, master=None):
        super().__init__(master)
        self.config(
            wrap=tk.WORD,
            relief=tk.FLAT,
            bg=BOXFILLCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            font=("Arial", FONT_SIZE),
        )


class uiButton(Button):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.config(
            text=kwargs["text"],
            command=kwargs["command"],
            bg=BTN_DARK,
            fg=BTN_LIGHT,
            activeforeground=BTN_DARK,
            activebackground=BTN_LIGHT,
            highlightthickness=1,
            highlightbackground=BTN_LIGHT,
            highlightcolor=BTN_LIGHT,
            relief=tk.FLAT,
            font=("Arial", FONT_SIZE),
        )

class uiCarefulButton(Button):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.config(
            text=kwargs["text"],
            command=kwargs["command"],
            bg=CAREFUL_BTN_DARK,
            fg=BTN_LIGHT,
            activeforeground=CAREFUL_BTN_DARK,
            activebackground=BTN_LIGHT,
            highlightthickness=1,
            highlightbackground=BTN_LIGHT,
            highlightcolor=BTN_LIGHT,
            relief=tk.FLAT,
            font=("Arial", FONT_SIZE),
        )

class uiLabel(tk.Label):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])

        if "text" in kwargs:
            if "font" not in kwargs:
                kwargs["font"] = ("Arial", FONT_SIZE)
            self.config(
                text=kwargs["text"],
                bg=BGCOLOR,
                fg=TEXTCOLOR,
                # highlightthickness=1,
                # highlightbackground=TEXTCOLOR,
                # highlightcolor=TEXTCOLOR,
                font=kwargs["font"],
            )
        elif "image" in kwargs:
            self.config(
                image=kwargs["image"],
                bg=BGCOLOR,
                fg=TEXTCOLOR,
                # highlightthickness=1,
                # highlightbackground=TEXTCOLOR,
                # highlightcolor=TEXTCOLOR,
            )


class uiTextbox(tk.Text):
    def __init__(self, **kwargs):
        super().__init__(kwargs.pop("master"), **kwargs)
        self.config(wrap="word", font=("Arial", FONT_SIZE))


class uiQuietFrame(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.config(
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            highlightbackground=BGCOLOR,
            padx=PADX,
            pady=PADY
        )

class uiLabelFrame(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.config(
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            highlightbackground=BGCOLOR,
            text=kwargs["text"],
            labelanchor="n",
            font=("Arial",15),
            padx=PADX,
            pady=PADY
        )

class uiNotebook(ttk.Notebook):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        # self.config(
        # relief=tk.FLAT,
        # borderwidth=0,
        # highlightthickness=0,
        # highlightbackground=DARKCOLOR
        # )
        # self.config(font=("Arial", FONT_SIZE))


class uiEntry(tk.Entry):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.config(
            bg=BOXFILLCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            insertbackground=TEXTCOLOR,
            font=("Arial", FONT_SIZE)
        )
        # self.bind("<FocusOut>", self.validate_out)

    def validate_out(self, event):
        if self.get().strip() == "":
            self.focus_set()


class EntryHelp:
    def __init__(self, master, text):
        self.master = master
        self.text = text

        self.frame = uiQuietFrame(master=master)
        self.frame.grid(sticky="nsew")

        # self.frame.columnconfigure(2)

        self.entry = uiEntry(master=self.frame, width=16)
        self.entry.grid(row=0, column=0)

        self.help_button = uiButton(
            master=self.frame,
            text="?",
            command=lambda: messagebox.showinfo("Help", self.text, parent=self.master),
        )
        self.help_button.configure(width=26)
        self.help_button.grid(row=0, column=1)


class ComboBoxHelp:
    def __init__(self, master, text):
        self.master = master
        self.text = text

        self.frame = uiQuietFrame(master=master)
        self.frame.grid(sticky="nsew")

        self.frame.columnconfigure(7)

        self.combobox = uiComboBox(master=self.frame)
        self.combobox.grid(row=0, column=0, columnspan=6)

        self.help_button = uiButton(
            master=self.frame,
            text="?",
            command=lambda: messagebox.showinfo("Help", self.text, parent=self.master),
        )
        self.help_button.configure(width=26)
        self.help_button.grid(row=0, column=7)


class uiComboBox(ttk.Combobox):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.config(font=("Arial", FONT_SIZE))


class uiCanvas(tk.Canvas):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        self.cell_size = kwargs["cell_size"]
        self.border_size = kwargs["border_size"]
        self.obj_char_size = kwargs["obj_char_size"]
        self.item_char_size = kwargs["item_char_size"]
        self.char_offset = kwargs["char_offset"]
        self.obj_font = kwargs["obj_font"]
        self.item_font = kwargs["item_font"]
        self.rcfont = tk.font.Font(
            family="TkFixedFont", size=int(self.obj_char_size / 2)
        )
        self.map_font = tk.font.Font(
            family="TkFixedFont", size=int(self.cell_size-10)
        )
        self.config(
            width=kwargs["width"],
            height=kwargs["height"],
            xscrollcommand=kwargs["xscrollcommand"],
            yscrollcommand=kwargs["yscrollcommand"],
            scrollregion=kwargs["scrollregion"],
            bg=BOXFILLCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
        )
        self.sprites = []
        self.tiles = {}
        self.objects = {}
        self.items = {}
        self.starting_locations = {}

    def mousexy_to_cellxy(self, x, y):
        x = int((self.canvasx(x) - self.border_size) // self.cell_size)
        y = int((self.canvasy(y) - self.border_size) // self.cell_size)
        return x,y


    def draw_tile(self, **kwargs):
        """Draws tile"""
        x = kwargs["x"]
        y = kwargs["y"]
        x0 = x * self.cell_size + self.border_size
        y0 = y * self.cell_size + self.border_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        tile = self.create_rectangle(x0, y0, x1, y1, fill=kwargs["fill"], width=2)
        self.tiles[(x,y)] = tile

        # self._create(
        #     'rectangle',
        #     [x0,y0,x1,y1],
        #     {'fill':kwargs['fill']}
        # )
    

    def draw_circle(self, x, y, color, diameter):
        x0 = x * self.cell_size + self.border_size + ((self.cell_size - diameter) // 2)
        y0 = y * self.cell_size + self.border_size + ((self.cell_size - diameter) // 2)
        x1 = x0 + diameter
        y1 = y0 + diameter
        self.create_oval(x0, y0, x1, y1, fill=color)

    def draw_character(self, x, y, character, color):
        x0 = x * self.cell_size + self.border_size + (self.cell_size // 2)
         # Magic number 4 almost certainly does not work for other font sizes.
        y0 = y * self.cell_size + self.border_size + ((self.cell_size-4) // 2)
        self.create_text(x0, y0, text=character, fill=color, font=self.map_font)

    def draw_starting_location(self, x, y, loc_num, color):
        circ_id = self.draw_circle(x, y, color, self.cell_size-5)
        char_id = self.draw_character(x, y, str(loc_num), "black")
        self.starting_locations[(x,y)] = (circ_id, char_id)

    def draw_sprite(self, **kwargs):
        """Draws object

        Tries to draw sprite based on object status
        Defaults to text based representation if unsuccessful
        """
        x = (  # x coord
            kwargs["x"] * self.cell_size
            + self.border_size
        )
        y = (  # y coord
            kwargs["y"] * self.cell_size
            + self.border_size
        )

        try:
            sprite = sprite_manager.load_image(kwargs["sprite_filename"])
            width, height = sprite.size
            x += (width // 2) + ((self.cell_size - width) // 2)
            y += (height // 2) + ((self.cell_size - height) // 2)
            facing = 0
            if "facing" in kwargs:
                # sim uses clock-wise coords, ui uses counter-clockwise coords
                facing = kwargs["facing"] * -1
            sprite.rotate(facing)
            tk_sprite = ImageTk.PhotoImage(sprite)
            self.sprites.append(tk_sprite)
            obj = self.create_image(x, y, image=tk_sprite)
            self.objects[(kwargs["x"], kwargs["y"])] = obj
        except:
            raise
                # x += self.char_offset + (self.obj_char_size / 2)
                # y += self.char_offset + (self.obj_char_size / 2)
                # return self.create_text(
                #     x, y, text=kwargs["character"], fill=kwargs["color_alive"], font=self.obj_font
                # )
        # else:
        #     try:
        #         self.sprite = sprite_manager.load_image(kwargs["dead_sprite_filename"])
        #         width, height = sprite.size
        #         x += (width // 2) + ((self.cell_size - width) // 2)
        #         y += (height // 2) + ((self.cell_size - height) // 2)
        #         facing = 0
        #         if "facing" in kwargs:
        #             # sim uses clock-wise coords, ui uses counter-clockwise coords
        #             facing = kwargs["facing"] * -1
        #         sprite.rotate(facing)
        #         tk_sprite = ImageTk.PhotoImage(sprite)
        #         self.sprites.append(tk_sprite)
        #         obj = self.create_image(x, y, image=tk_sprite)
        #         self.objects[(kwargs["x"], kwargs["y"])] = obj
        #     except:
        #         raise
        #         # x += self.char_offset + (self.obj_char_size // 2)
        #         # y += self.char_offset + (self.obj_char_size // 2)
        #         # return self.create_text(
        #         #     x, y, text=kwargs["character"], fill=kwargs["color_dead"], font=self.obj_font
        #         # )

    def remove_obj_at(self, x, y):
        self.remove_obj(self.objects[(x,y)])

    def remove_obj(self, obj_id):
        """Removes object"""
        self.delete(obj_id)


    def redraw_obj(self, **kwargs):
        """Redraws object"""
        self.remove_obj(kwargs["obj_id"])
        return self.draw_obj(**kwargs)

    def update_drawn_obj(self, **kwargs):
        """Updates drawn object"""
        # self.delete(kwargs['obj_id'])
        dd = kwargs["dd"]
        x = (
            dd["x"] * self.cell_size
            + self.obj_char_size / 2
            + self.char_offset
            + self.cell_size
        )
        y = (
            dd["y"] * self.cell_size
            + self.obj_char_size / 2
            + self.char_offset
            + self.cell_size
        )
        self.coords(kwargs["obj_id"], x, y)

    def draw_item(self, **kwargs):
        """Draws item

        Tries to draw sprite
        Defaults to text based representation if unsuccessful
        """
        dd = kwargs["dd"]
        x = (
            dd["x"] * self.cell_size
            + self.obj_char_size / 2
            + self.char_offset
            + self.cell_size
        )
        y = (
            dd["y"] * self.cell_size
            + self.obj_char_size / 2
            + self.char_offset
            + self.cell_size
        )
        try:
            self.sprite = Image.open(dd["sprite_path"])
            global_sprite_list.append(self.sprite.copy())
            global_sprite_list[-1] = ImageTk.PhotoImage(global_sprite_list[-1])
            return self.create_image(x, y, image=global_sprite_list[-1])
        except:
            return self.create_text(
                x, y, text=dd["text"], fill=dd["fill"], font=self.obj_font
            )

    def remove_item(self, item_id):
        """Removes an item from the canvas"""
        self.delete(item_id)

    def update_drawn_item(self, **kwargs):
        """Updates drawn item"""
        dd = kwargs["dd"]
        x = (
            dd["x"] * self.cell_size
            + self.obj_char_size / 2
            + self.char_offset
            + self.cell_size
        )
        y = (
            dd["y"] * self.cell_size
            + self.obj_char_size / 2
            + self.char_offset
            + self.cell_size
        )
        self.coords(kwargs["itemID"], x, y)

    def draw_row_labels(self, **kwargs):
        width = kwargs["width"]
        height = kwargs["height"]

        label_ids = []

        top = self.obj_char_size / 2 + self.char_offset
        bottom = height * self.cell_size + self.obj_char_size / 2 + self.char_offset + self.border_size

        for i in range(width):
            x = i * self.cell_size + self.obj_char_size / 2 + self.char_offset + self.border_size
            label_ids.append(
                self.create_text(
                    x, top,
                    text=str(i),
                    fill=kwargs["fill"],
                    font=self.rcfont
                )
            )

            label_ids.append(
                self.create_text(
                    x, bottom,
                    text=str(i),
                    fill=kwargs["fill"],
                    font=self.rcfont
                )
            )

        return label_ids

    def draw_column_labels(self, **kwargs):
        width = kwargs["width"]
        height = kwargs["height"]

        label_ids = []

        left = self.obj_char_size / 2 + self.char_offset
        right = width * self.cell_size + self.obj_char_size / 2 + self.char_offset + self.border_size

        for i in range(height):
            y = i * self.cell_size + self.obj_char_size / 2 + self.char_offset + self.border_size
            label_ids.append(
                self.create_text(
                    left, y,
                    text=str(i),
                    fill=kwargs["fill"],
                    font=self.rcfont
                )
            )

            label_ids.append(
                self.create_text(
                    right, y,
                    text=str(i),
                    fill=kwargs["fill"],
                    font=self.rcfont
                )
            )

        return label_ids

    def draw_rc_number(self, **kwargs):
        """Draws RDNumber"""
        x = kwargs["x"] * self.cell_size + self.obj_char_size / 2 + self.char_offset
        y = kwargs["y"] * self.cell_size + self.obj_char_size / 2 + self.char_offset
        return self.create_text(
            x, y, text=kwargs["text"], fill=kwargs["fill"], font=self.rcfont
        )

        # Circumvents a tk call...speed up is marginal.
        # self._create(
        #     'text',
        #     [x,y],
        #     {
        #         'text':kwargs['text'],
        #         'fill':kwargs['fill'],
        #         'font':self.rcfont
        #     }
        # )

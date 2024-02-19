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

BGCOLOR='#E5E5E5'
TEXTCOLOR='#222222'

BTN_DARK='#495EA7'
BTN_LIGHT='#FFFFFF'

ENTRY_DARK='#222222'
ENTRY_BG='salmon1'

BOXFILLCOLOR='#B2C1E3'

class uiListBox(tk.Listbox):
    def __init__(self,master=None):
        super().__init__(master)
        self.config(
            selectmode=tk.SINGLE,
            bg=BOXFILLCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            relief=tk.FLAT,
            selectforeground=TEXTCOLOR,
            selectbackground=ENTRY_BG,
            exportselection=0,
            font = (12)
        )


class uiScrollText(tk.scrolledtext.ScrolledText):
    def __init__(self,master=None):
        super().__init__(master)
        self.config(
            wrap = tk.WORD,
            relief=tk.FLAT,
            bg=BOXFILLCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            font = (12)
        )

class uiButton(tk.Button):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])
        self.config(
            text=kwargs['text'],
            command=kwargs['command'],
            bg=BTN_DARK,
            fg=BTN_LIGHT,
            activeforeground=BTN_DARK,
            activebackground=BTN_LIGHT,
            highlightthickness=1,
            highlightbackground=BTN_LIGHT,
            highlightcolor=BTN_LIGHT,
            relief=tk.FLAT,
            font=(12)
        )

class uiLabel(tk.Label):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])
        self.config(
            text=kwargs['text'],
            bg=BGCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            font=(12) #changed by HK, originally no font parameter
        )

class uiQuietFrame(tk.Frame):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])
        self.config(
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            highlightbackground=BGCOLOR
        )

class uiNotebook(ttk.Notebook):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])
        #self.config(
            #relief=tk.FLAT,
            #borderwidth=0,
            #highlightthickness=0,
            #highlightbackground=DARKCOLOR
        #)

class uiEntry(tk.Entry):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])
        self.config(
            bg=BOXFILLCOLOR,
            fg=TEXTCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR,
            insertbackground=TEXTCOLOR
        )

class uiComboBox(ttk.Combobox):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])


class uiCanvas(tk.Canvas):
    def __init__(self,**kwargs):
        super().__init__(kwargs['master'])
        self.cell_size=kwargs['cell_size']
        self.obj_char_size=kwargs['obj_char_size']
        self.item_char_size=kwargs['item_char_size']
        self.char_offset=kwargs['char_offset']
        self.obj_font = kwargs['obj_font']
        self.item_font = kwargs['item_font']
        self.rcfont = tk.font.Font(family='TkFixedFont',size=int(self.obj_char_size/2))
        self.config(
            width=kwargs['width'],
            height=kwargs['height'],
            xscrollcommand=kwargs['xscrollcommand'],
            yscrollcommand=kwargs['yscrollcommand'],
            scrollregion=kwargs['scrollregion'],
            bg=BOXFILLCOLOR,
            highlightthickness=1,
            highlightbackground=TEXTCOLOR,
            highlightcolor=TEXTCOLOR
        )


    def drawTile(self,**kwargs):
        x0=kwargs['x']*self.cell_size
        y0=kwargs['y']*self.cell_size
        x1=x0+self.cell_size
        y1=y0+self.cell_size
        return self.create_rectangle(
            x0,y0,x1,y1,
            fill=kwargs['fill']
        )

        # self._create(
        #     'rectangle',
        #     [x0,y0,x1,y1],
        #     {'fill':kwargs['fill']}
        # )
    def drawObj(self,**kwargs):
        dd=kwargs['dd']
        x=dd['x'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        y=dd['y'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        return self.create_text(
            x,y,
            text=dd['text'],
            fill=dd['fill'],
            font=self.obj_font
        )
    def removeObj(self,objID):
        self.delete(objID)
    def redrawObj(self,**kwargs):
        self.removeObj(kwargs['objID'])
        return self.drawObj(**kwargs)
    def updateDrawnObj(self,**kwargs):
        #self.delete(kwargs['objID'])
        dd=kwargs['dd']
        x=dd['x'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        y=dd['y'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        self.coords(kwargs['objID'],x,y)
    def drawItem(self,**kwargs):
        dd=kwargs['dd']
        x=dd['x'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        y=dd['y'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        return self.create_text(
            x,y,
            text=dd['text'],
            fill=dd['fill'],
            font=self.item_font
        )
    def updateDrawnItem(self,**kwargs):
        dd=kwargs['dd']
        x=dd['x'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        y=dd['y'] * self.cell_size + self.obj_char_size/2 + self.char_offset +self.cell_size
        self.coords(kwargs['itemID'],x,y)

    def drawRCNumber(self,**kwargs):
        x = kwargs['x']* self.cell_size + self.obj_char_size/2 + self.char_offset
        y = kwargs['y']* self.cell_size + self.obj_char_size/2 + self.char_offset
        return self.create_text(
            x,y,
            text=kwargs['text'],
            fill=kwargs['fill'],
            font=self.rcfont
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

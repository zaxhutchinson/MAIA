import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as scrolltext
import queue
import cProfile

from ui_widgets import *

class UISim(tk.Toplevel):
    def __init__(self,map_width,map_height,sim,omsgr,master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=DARKCOLOR)
        self.title("MAIA - Sim UI")

        self.cell_size=32
        self.char_size=24
        self.char_offset = (self.cell_size-self.char_size)/2
        self.map_font = tk.font.Font(family='TkFixedFont',size=self.char_size)

        # Store data
        self.sim = sim
        self.omsgr = omsgr
        self.map_width=map_width
        self.map_height=map_height

        # Create the left and right frames
        self.mapFrame = uiQuietFrame(master=self)
        self.mapFrame.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)
        self.logFrame = uiQuietFrame(master=self)
        self.logFrame.pack(fill=tk.BOTH,expand=True,side=tk.RIGHT)

        # Create the map canvas
        self.xbar = tk.Scrollbar(self.mapFrame,orient=tk.HORIZONTAL)
        self.ybar = tk.Scrollbar(self.mapFrame,orient=tk.VERTICAL)
        self.canvas = uiCanvas(
            master=self.mapFrame,
            width=800,
            height=800,
            xscrollcommand=self.xbar.set,
            yscrollcommand=self.ybar.set,
            scrollregion=(0,0,(self.map_width+2)*self.cell_size,(self.map_height+2)*self.cell_size),
            cell_size=self.cell_size,
            char_size=self.char_size,
            char_offset=self.char_offset,
            font = self.map_font
        )
        self.ybar.configure(command=self.canvas.yview)
        self.xbar.configure(command=self.canvas.xview)
        self.ybar.pack(side=tk.RIGHT,fill=tk.Y)
        self.xbar.pack(side=tk.BOTTOM,fill=tk.X)
        self.canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.canvas.yview_moveto(0.0)
        self.canvas.xview_moveto(0.0)
        
        # Create the log
        self.scrollLog = uiScrollText(master=self.logFrame)
        self.scrollLog.pack(fill=tk.BOTH,expand=True,side=tk.TOP)
        self.scrollLog.configure(state='disabled')

        self.dataFrame1 = uiQuietFrame(master=self.logFrame)
        self.dataFrame1.pack(fill=tk.BOTH,expand=True,side=tk.TOP)
        self.lbTurnsToRun = uiLabel(master=self.dataFrame1,text="Turns To Run")
        self.lbTurnsToRun.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)
        self.tbTurnsToRun = uiEntry(master=self.dataFrame1)
        self.tbTurnsToRun.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)


        
        # self.dataFrame2 = uiQuietFrame(master=self.logFrame)
        # self.dataFrame2.pack(fill=tk.BOTH,expand=True,side=tk.TOP)

        self.btnFrame1 = uiQuietFrame(master=self.logFrame)
        self.btnFrame1.pack(fill=tk.BOTH,expand=True,side=tk.TOP)
        self.btnRunXTurns = uiButton(master=self.btnFrame1,text="Run X Turns",command=self.runXTurns)
        self.btnRunXTurns.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)

        self.logFrame.after(100, self.updateLog)

        self.updateMap()
        
        #TEST JUNK
        # self.canvas.create_text(50,50,text="Hello world")
        #self.canvas.create_rectangle(50,50,450,450,fill="green")
    def displayMsg(self,msg):
        m = msg.getText()
        self.scrollLog.configure(state='normal')
        self.scrollLog.insert(tk.END,m+"\n")
        self.scrollLog.configure(state='disabled')
        self.scrollLog.yview(tk.END)

    def updateMap(self):
        self.canvas.delete(tk.ALL)
        draw_data = self.sim.getObjDrawData()

        w = self.map_width+2
        h = self.map_height+2

        for x in range(w):
            for y in range(h):
                
                # box=(
                #     x*self.cell_size,
                #     y*self.cell_size,
                #     x*self.cell_size+self.cell_size,
                #     y*self.cell_size+self.cell_size,
                # )
                if x != 0 and x != w-1 and y != 0 and y != h-1:
                    self.canvas.drawTile(
                        x=x,
                        y=y,
                        fill='gray25'
                    )

                if (x==0 and (y != 0 and y != h-1)) or (x==w-1 and(y!=0 and y!=h-1)):
                    self.canvas.drawRCNumber(
                        x=x,y=y,
                        fill='gray35',
                        text=str(y-1)
                    )
                elif (y==0 and (x != 0 and x != w-1)) or (y==h-1 and(x!=0 and x!=w-1)):
                    self.canvas.drawRCNumber(
                        x=x,y=y,
                        fill='gray35',
                        text=str(x-1)
                    )
        for dd in draw_data:
            self.canvas.drawObj(dd=dd)

    def updateLog(self):
        while True:
            try:
                m=self.omsgr.getMsg()
            except queue.Empty:
                break
            else:
                self.displayMsg(m)
        self.logFrame.after(100,self.updateLog)

    def runXTurns(self):
        turns_to_run = self.tbTurnsToRun.get()
        if turns_to_run.isdigit():
            turns_to_run = int(turns_to_run)
            self.sim.runSim(turns_to_run)

        #with cProfile.Profile() as pr:
        self.updateMap()
        #pr.print_stats()

        

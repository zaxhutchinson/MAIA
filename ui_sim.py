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

from ui_widgets import *

class UISim(tk.Toplevel):
    def __init__(self,map_width,map_height,sim,omsgr,master=None,logger=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=BGCOLOR)
        self.title("MAIA - Sim UI")
        self.logger=logger

        self.cell_size=32
        self.map_obj_char_size=24
        self.map_item_char_size=10
        self.char_offset = (self.cell_size-self.map_obj_char_size)/2
        self.map_obj_font = tk.font.Font(family='TkFixedFont',size=self.map_obj_char_size)
        self.map_item_font = tk.font.Font(family='TkFixedFont',size=self.map_item_char_size)

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
            obj_char_size=self.map_obj_char_size,
            item_char_size=self.map_item_char_size,
            char_offset=self.char_offset,
            obj_font = self.map_obj_font,
            item_font = self.map_item_font
        )
        self.ybar.configure(command=self.canvas.yview)
        self.xbar.configure(command=self.canvas.xview)
        self.ybar.pack(side=tk.RIGHT,fill=tk.Y)
        self.xbar.pack(side=tk.BOTTOM,fill=tk.X)
        self.canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        self.canvas.yview_moveto(0.0)
        self.canvas.xview_moveto(0.0)
        
        # Create the log notebook and tabs
        self.logNotebook = uiNotebook(master=self.logFrame)
        self.logNotebook.pack(fill=tk.BOTH,expand=True,side=tk.TOP)

        self.mainLogFrame = uiQuietFrame(master=self.logNotebook)
        self.logNotebook.add(self.mainLogFrame,text='Main')
        self.mainScrollLog = uiScrollText(master=self.mainLogFrame)
        self.mainScrollLog.pack(fill=tk.BOTH,expand=True,side=tk.TOP)
        self.mainScrollLog.configure(state='disabled')

        # Add the buttons
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
        self.btnDisplayPoints = uiButton(master=self.btnFrame1,text="Display Points",command=self.displayPoints)
        self.btnDisplayPoints.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)

        self.logFrame.after(100, self.updateLog)

        # Draw the background tiles
        self.canvas_background_tile_ids = []
        self.canvas_background_RCnum_ids = []
        self.drawTiles()

        self.obj_drawIDs = {}
        self.initObjects()

        self.item_drawIDs = {}
        self.initItems()
        
        #TEST JUNK
        # self.canvas.create_text(50,50,text="Hello world")
        #self.canvas.create_rectangle(50,50,450,450,fill="green")
    def displayMsgMain(self,msg):
        m = msg.getText()
        self.mainScrollLog.configure(state='normal')
        self.mainScrollLog.insert(tk.END,m+"\n")
        self.mainScrollLog.configure(state='disabled')
        self.mainScrollLog.yview(tk.END)

    def drawTiles(self):
        
        w = self.map_width+2
        h = self.map_height+2

        for x in range(w):
            for y in range(h):

                if x != 0 and x != w-1 and y != 0 and y != h-1:
                    tile_id = self.canvas.drawTile(
                        x=x,
                        y=y,
                        fill='snow4'
                    )
                    self.canvas_background_tile_ids.append(tile_id)

                if (x==0 and (y != 0 and y != h-1)) or (x==w-1 and(y!=0 and y!=h-1)):
                    RCnum_id = self.canvas.drawRCNumber(
                        x=x,y=y,
                        fill='gray35',
                        text=str(y-1)
                    )
                    self.canvas_background_RCnum_ids.append(RCnum_id)
                elif (y==0 and (x != 0 and x != w-1)) or (y==h-1 and(x!=0 and x!=w-1)):
                    RCnum_id = self.canvas.drawRCNumber(
                        x=x,y=y,
                        fill='gray35',
                        text=str(x-1)
                    )
                    self.canvas_background_RCnum_ids.append(RCnum_id)
    
    #####################################################
    # OBJECT DRAWING
    def addObjectDrawID(self,_uuid,_drawID):
        self.obj_drawIDs[_uuid]=_drawID
    def getObjectDrawID(self,_uuid):
        try:
            return self.obj_drawIDs[_uuid]
        except KeyError:
            self.logger.error("UISim: KeyError "+str(_uuid)+" in getObjectDrawID().")
            return None
    def removeObjectDrawID(self,_uuid):
        objID = self.getObjectDrawID(_uuid)
        if objID != None:
            self.canvas.removeObj(objID)
            del self.obj_drawIDs[_uuid]
    
    def initObjects(self):
        #self.canvas.delete(tk.ALL)
        draw_data = self.sim.getObjDrawData()
                
        for dd in draw_data:
            obj_id = self.canvas.drawObj(dd=dd)
            self.addObjectDrawID(dd['uuid'],obj_id)
    def updateObjects(self):
        draw_data = self.sim.getObjDrawData()
        for dd in draw_data:
            if dd['redraw']:
                objID = self.getObjectDrawID(dd['uuid'])
                objID = self.canvas.redrawObj(dd=dd,objID=objID)
                self.addObjectDrawID(dd['uuid'],objID)
            else:
                objID = self.getObjectDrawID(dd['uuid'])
                self.canvas.updateDrawnObj(dd=dd,objID=objID)

    ######################################################
    # ITEM DRAWING
    def addItemDrawID(self,_uuid,_drawID):
        self.item_drawIDs[_uuid]=_drawID
    def getItemDrawID(self,_uuid):
        try:
            return self.item_drawIDs[_uuid]
        except KeyError:
            self.logger.error("UISim: KeyError "+str(_uuid)+" in getItemDrawID().")
            return None
    def removeItemDrawID(self,_uuid):
        del self.item_drawIDs[_uuid]
    def initItems(self):
        draw_data = self.sim.getItemDrawData()
        for dd in draw_data:
            item_id = self.canvas.drawItem(dd=dd)
            self.addItemDrawID(dd['uuid'],item_id)
    def updateItems(self):
        draw_data = self.sim.getItemDrawData()
        for dd in draw_data:
            item_id = self.getItemDrawID(dd['uuid'])
            self.canvas.updateDrawnItem(dd=dd,itemID=item_id)

    def updateLog(self):
        while True:
            try:
                m=self.omsgr.getMsg()
            except queue.Empty:
                break
            else:
                self.displayMsgMain(m)
        self.logFrame.after(100,self.updateLog)

    def runXTurns(self):
        turns_to_run = self.tbTurnsToRun.get()
        if turns_to_run.isdigit():
            turns_to_run = int(turns_to_run)
            self.sim.runSim(turns_to_run)


        self.updateObjects()
        self.updateItems()

    def displayPoints(self):
        self.sim.getPointsData()


        

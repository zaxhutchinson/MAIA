import tkinter as tk
import sys

import ui_setup
import vec2
import math
import zmap
from log import *



if __name__ == "__main__":
    # Initialize the log files
    LogInit()
    

    # Start App
    root = tk.Tk()
    maia_app = ui_setup.UISetup(master=root)
    maia_app.Run()



# def getLine(v,angle):
#     m = math.tan(angle)
#     n = v.getY() - m * v.getX()
#     return (m,n)

# A = vec2.Vec2(0,0)
# B = vec2.Vec2(5,5)

# l = getLine(A,23.0*math.pi/4.0)
# print(l)
# print(B.distanceToLine(l[0],l[1]))



# objA = l.getObject(0)
# objB = l.getObject(0)

# objA.addDamage(5)

# print(objA.getCurrentHealth())
# print(objA.isAlive())


# ms = l.getMapSetting(0)
# print(ms.name,ms.placed_objects)

# mymap = zmap.Map(ms)
# mymap.generateMap(l)



# class A:
#     name = "123"

# a = globals()['A']()
# print(isinstance(a,A),a.name)

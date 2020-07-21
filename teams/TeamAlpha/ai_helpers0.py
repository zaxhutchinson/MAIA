import sys
##############################################################################
##############################################################################
# VIEW RELATED STUFF
##############################################################################
##############################################################################

##################################
# Pretty Print the view coming from the simulation.
# This method will print an indented version of the view using the
# output file specified. By default it sends output to stdout.
# Users can but in general should not need to pass in a value for indent.
def prettyPrintView(view, out=sys.stdout, indent=""):
    if type(view) != dict:
        # If view is a list, pass its contents back to the method.
        if type(view)==list:
            for i in view:
                prettyPrintView(i,out,indent+"  ")
            return
        # If it isn't a list or dict, assume its a single value.
        else:
            out.write(": "+str(view))
            return
    
    # Print key and recurse.
    for k,v in view.items():
        out.write('\n'+indent+str(k))

        prettyPrintView(v, out, indent+"  ")

    out.write('\n')


def getSubView(view, *args):
    try:
        subview = view[args[0]]
        return getSubView(subview, *args[1:])
    except IndexError:
        return view
    except TypeError:
        return None
    except:
        return None



##################################
# Search scan view for pings containing specific objnames.
# Returns a dictionary of pings that contain the objname.
# Each entry in the returned dict is a list keyed by direction.
# 
def searchScanForObjname(view,name):
    found_pings = {}

    comp_views = getSubView(view,'comp')

    if comp_views != None:

        scan_views = {}

        for k,v in comp_views.items():

            scan_views=[]

            # Find all comp views from scanner components
            for cv in v:
                if cv['ctype']=="Scanner":
                    scan_views.append(cv)

            # Search the scan views for pings with a matching obj name.
            for sv in scan_views:
                for vec,data in sv['pings'].items():
                    if data['objname']==name:
                        if k not in found_pings:
                            found_pings[k]={}
                            found_pings[k][vec]=[]
                        elif vec not in found_pings[k]:
                            found_pings[k][vec]=[]
                        found_pings[k][vec].append(data)
    return found_pings








##############################################################################
##############################################################################
# COMMAND RELATED
##############################################################################
##############################################################################

class CmdMaker:
    def __init__(self):
        self.cmds = {}

    def getCmds(self):
        return self.cmds

    def addCmd(self,tick,slot,cmd):
        tick = str(tick)
        if tick not in self.cmds:
            self.cmds[tick]={}
        self.cmds[tick][str(slot)]=cmd


##############################################################################
# FIXED GUN COMMAND FUNCTIONS
#
# Creates a fire command
def CMD_Fire():
    cmd = {}
    cmd['command']='FIRE'
    return cmd

# Creates a reload command
def CMD_Reload():
    cmd = {}
    cmd['command']='RELOAD'
    return cmd

##############################################################################
# ENGINE COMMAND FUNCTIONS
#
# Creates a turn command
def CMD_Turn(turnrate):
    cmd = {}
    cmd['command']='SET_TURNRATE'
    cmd['turnrate']=turnrate
    return cmd

# Creates a set speed command
def CMD_SetSpeed(speed):
    cmd = {}
    cmd['command']='SET_SPEED'
    cmd['speed']=speed
    return cmd

##############################################################################
# SCANNER COMMAND FUNCTIONS
#
# Initiate a scan
def CMD_Scan():
    cmd = {}
    cmd['command']='SCAN'
    return cmd

##############################################################################
# RADIO FUNCTIONS
#
# Broadcast message
def CMD_Broadcast(message):
    cmd = {}
    cmd['command']='BROADCAST'
    cmd['message']=message
    return cmd
def CMD_SetRange(_range):
    cmd = {}
    cmd['command']='SET_RANGE'
    cmd['message']=_range
    return cmd

##############################################################################
# GENERIC COMMAND FUNCTIONS
#
# Activates the component,
def CMD_Activate():
    cmd={}
    cmd['command']='ACTIVATE'
    return cmd

# Deactivates the component.
def CMD_Deactivate():
    cmd={}
    cmd['command']='DEACTIVATE'
    return cmd

##############################################################################
# 
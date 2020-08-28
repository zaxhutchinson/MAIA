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
    except:
        return None


##################################################
# GETTERS FOR SELF VIEW DATA
def getSelf(view):
    return getSubView(view,'self')
def getFacing(view):
    return getSubView(view,'self','facing')
def getHealth(view):
    return getSubView(view,'self','health')
def getDamage(view):
    return getSubView(view,'self','damage')
def getX(view):
    return getSubView(view,'self','x')
def getY(view):
    return getSubView(view,'self','y')
def getCellX(view):
    return getSubView(view,'self','cell_x')
def getCellY(view):
    return getSubView(view,'self','cell_y')
def getTeamName(view):
    return getSubView(view,'self','teamname')
def getCallSign(view):
    return getSubView(view,'self','callsign')
def getSquad(view):
    return getSubView(view,'self','squad')
def getComps(view):
    return getSubView(view,'self','comps')
def getCompBySlotID(view,slot_id):
    return getSubView(view,'self','comps',slot_id)

# Returns a dictionary where k=ctype and v=[slot_ids]
# Good use is to call and store on T0 for future reference
def getSlotIDsByCtype(view):
    comps_by_ctype={}

    comps = getComps(view)

    for slot_id,comp in comps.items():

        ctype = comp['ctype']

        if ctype not in comps_by_ctype:
            comps_by_ctype[ctype]=[]
        
        comps_by_ctype[ctype].append(slot_id)

    return comps_by_ctype

#####################################################
# Gun related functions
def canWeaponFire(view,slotID):
    comp = getCompBySlotID(view,slotID)
    return comp['reload_ticks_remaining']==0 and comp['ammunition']>0
def doesWeaponNeedReloading(view, slotID):
    comp = getCompBySlotID(view,slotID)
    return comp['reload_ticks_remaining'] > 0 and not comp['reloading']
def isWeaponReloading(view, slotID):
    comp = getCompBySlotID(view,slotID)
    return comp['reloading']

##################################
# Search radar view for pings containing specific objnames.
# Returns a dictionary of pings that contain the objname.
# Each entry in the returned dict is a list keyed by direction.
# 
def searchRadarForObjname(view,name):
    found_pings = {}

    comp_views = getSubView(view,'comp')

    if comp_views != None:

        radar_views = {}

        for k,v in comp_views.items():

            radar_views=[]

            # Find all comp views from radar components
            for cv in v:
                if cv['ctype']=="Radar":
                    radar_views.append(cv)

            # Search the radar views for pings with a matching obj name.
            for sv in radar_views:
                for vec,data in sv['pings'].items():
                    if data['name']==name:
                        if k not in found_pings:
                            found_pings[k]={}
                            found_pings[k][vec]=[]
                        elif vec not in found_pings[k]:
                            found_pings[k][vec]=[]
                        found_pings[k][vec].append(data)
    return found_pings



##############################################################################
# COMP VIEW

# getCompViewsOfVtype
# Returns a list of all the views within the comp view with a specific vtype.
def getCompViewsOfVtype(view, vtype):
    views = []
    comp_subview = getSubView(view,'comp')
    if comp_subview != None:
        for cv in comp_subview:
            if cv['vtype'] == vtype:
                views.append(cv)
    return views





##############################################################################
##############################################################################
# COMMAND RELATED
##############################################################################
##############################################################################

# Command Maker helps creating the command dictionary the simulation expects
# to be returned from the runAI method. Create the object and store.
# Add commands use addCmd. Use getCmds() as your return from runAI().
# At the start of your runAI(), include a call to reset().
class CmdMaker:
    def __init__(self):
        self.cmds = {}

    def reset(self):
        self.cmds.clear()

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
# RADAR COMMAND FUNCTIONS
#
# Initiate a radar transmission
def CMD_TransmitRadar():
    cmd = {}
    cmd['command']='TRANSMIT_RADAR'
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
# JUNK STUFF

def sign(value):
    if value==0:
        return 1
    else:
        return value / abs(value)
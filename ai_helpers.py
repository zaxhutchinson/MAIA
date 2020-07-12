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
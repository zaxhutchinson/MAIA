# An aid to build commands
#   comp_id: the component id
#   command: the command string (see list of commands)
#   value: an optional value that might be used by a command
#   index: comps are stored in lists, so there can be more than one. If that
#       is the case, you can use this to command the additional comps.

def BuildCommand(time,comp_id,command,value=0.0,index=0):
    d = {}
    d['time'] = time
    d['id'] = comp_id
    d['command']=command
    d['value']=value
    d['index']=index

    return d

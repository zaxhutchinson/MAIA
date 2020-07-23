#########
# VALID #
#########

# Is used to validate AI commands returning to the simulation. This makes it easier
# on the rest of the code if we've weeded out badly formed commands before they
# ever hit the processing part.

class CommandValidator:
    def __init__(self):
        self.commands = {}
        self.commands['FIRE'] = {}
        self.commands['RELOAD'] = {}
        self.commands['SET_SPEED'] = {
            'speed':[int,float]
        }
        self.commands['SET_TURNRATE'] = {
            'turnrate':[int,float]
        }
        self.commands['TRANSMIT_RADAR'] = {}
        self.commands['BROADCAST'] = {
            'message':[int,float,str,list,tuple,dict]
        }
        self.commands['SET_RANGE'] = {
            'range':[int,float]
        }

    def validateCommands(self,cmds):

        # cmds is None
        if cmds == None:
            return {}

        # Not a dictionary, so nothing's legit.
        if type(cmds) != dict:
            cmds.clear()
            print("Not a dictionary")
            return {}

        bad_cmds1 = []

        # k = tick, v = cmds by slot id
        for tick,slot_dict in cmds.items():

            # Not a dictionary, remove
            if type(slot_dict) != dict:
                bad_cmds1.append(tick)
                print("Not a dict 2")
                continue

            # Empty dict, remove
            if len(slot_dict)==0:
                bad_cmds1.append(tick)
                print("Empty Dict")
                continue

            bad_cmds2 = []

            for slot_id,command in slot_dict.items():

                # Command isn't a dict.
                if type(command) != dict:
                    bad_cmds2.append(slot_id)
                    print("Command isn't dict")
                    continue

                # Command is missing the command entry
                if 'command' not in command:
                    bad_cmds2.append(slot_id)
                    print("command is missing command entry")
                    continue

                if command['command'] not in self.commands:
                    bad_cmds2.append(slot_id)
                    print("Command "+command['command']+" is not a valid command.")
                    continue

                cmd_format = self.commands[command['command']]

                # command contains extra junk
                if len(cmd_format)+1 != len(command):
                    bad_cmds2.append(slot_id)
                    print("command contains extra shite")
                    continue

                for k,v in cmd_format.items():

                    # Required command info is missing
                    if k not in command:
                        bad_cmds2.append(slot_id)
                        print("required info is missing")
                        break

                    # If the command info is of the wrong data type, toss.
                    if type(command[k]) not in v:
                        print("Data '"+k+"' has wrong type "+str(type(command[k])))
                        bad_cmds2.append(slot_id)
                        break

            # Delete all the malformed component commands
            #print("deleting2",bad_cmds2)
            for bc in bad_cmds2:
                del cmds[tick][bc]

            # We might have emptied all commands for this tick. Check for empty again.
            # Empty dict, remove
            if len(slot_dict)==0:
                bad_cmds1.append(tick)
                print("Empty Dict")
                continue

        # Delete all commands for this tick.
        #print("deleting1",bad_cmds1)
        for bc in bad_cmds1:
            del cmds[bc]

        return cmds
                

if __name__ == "__main__":
    cv = CommandValidator()

    cmd = {'0': {'0': {'command': 'BROADCAST', 'message': []}},'1': {'5': {'commad': 'SET_RANGE', 'range': 1.0}}}

    print(cmd)

    newcmd = cv.validateCommands(cmd)

    print(newcmd)
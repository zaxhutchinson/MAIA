##############################################################################
# VALID
#
# Is used to validate AI commands returning to the simulation. This makes it
# easier
# on the rest of the code if we've weeded out badly formed commands before they
# ever hit the processing part.
##############################################################################


class CommandValidator:
    def __init__(self):
        """Initializes prossible commands and their inputs/input types"""
        self.commands = {}
        self.commands["FIRE"] = {}
        self.commands["RELOAD"] = {}
        self.commands["SET_SPEED"] = {"speed": [int, float]}
        self.commands["SET_TURNRATE"] = {"turnrate": [int, float]}
        self.commands["ACTIVATE_RADAR"] = {}
        self.commands["DEATIVATE_RADAR"] = {}
        self.commands["BROADCAST"] = {"message": [
            int, float, str, list, tuple, dict
        ]}
        self.commands["SET_RANGE"] = {"range": [int, float]}
        self.commands["TAKE_ITEM"] = {
            "item_name": [str, type(None)],
            "item_index": [int, type(None)],
            "item_uuid": [str, type(None)],
            "location": [str, type(None)],
        }
        self.commands["DROP_ITEM"] = {"location": [str, type(None)]}

    def validate_commands(self, cmds):
        """Determines if commands are well-formed"""
        # cmds is None
        if cmds is None:
            return {}

        # Not a dictionary, so nothing's legit.
        if type(cmds) is not dict:
            cmds.clear()
            # log.LogDebug("COMMAND VALIDATOR: Not a dictionary\n"+str(cmd))
            return {}

        good_cmds = []

        # k = tick, v = cmds by slot id
        for ctype, command in cmds.items():

            # Not a dictionary, remove
            if type(command) is not dict:
                del cmds[ctype]

            # Empty dict, remove
            elif len(command) == 0:
                del cmds[ctype]

            # No command entry
            elif "command" not in command:
                del cmds[ctype]

            # There is a command entry, but it is not a valid one.
            elif command["command"] not in self.commands:
                del cmds[ctype]

            # Now check the contents of the command
            else:

                # The command contains additional garbage.
                cmd_format = self.commands[command["command"]]
                if len(cmd_format) + 1 != len(command):
                    del cmds[ctype]

                for k, v in cmd_format.items():
                    if k not in command:
                        del cmds[ctype]
                        break

                    if type(command[k]) not in v:
                        del cmds[ctype]
                        break

        return cmds


# test of command validator?
if __name__ == "__main__":
    cv = CommandValidator()

    cmd = {
        "0": {"0": {"command": "BROADCAST", "message": []}},
        "1": {"5": {"commad": "SET_RANGE", "range": 1.0}},
    }

    newcmd = cv.validate_commands(cmd)

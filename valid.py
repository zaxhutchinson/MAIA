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

        bad_cmds1 = []

        # k = tick, v = cmds by slot id
        for tick, slot_dict in cmds.items():

            # Not a dictionary, remove
            if type(slot_dict) is not dict:
                bad_cmds1.append(tick)
                continue

            # Empty dict, remove
            if len(slot_dict) == 0:
                bad_cmds1.append(tick)
                continue

            bad_cmds2 = []

            for slot_id, command in slot_dict.items():

                # Command isn't a dict.
                if type(command) is not dict:
                    bad_cmds2.append(slot_id)
                    continue

                # Command is missing the command entry
                if "command" not in command:
                    bad_cmds2.append(slot_id)
                    continue

                if command["command"] not in self.commands:
                    bad_cmds2.append(slot_id)
                    continue

                cmd_format = self.commands[command["command"]]

                # command contains extra junk
                if len(cmd_format) + 1 != len(command):
                    bad_cmds2.append(slot_id)
                    continue

                for k, v in cmd_format.items():

                    # Required command info is missing
                    if k not in command:
                        bad_cmds2.append(slot_id)
                        break

                    # If the command info is of the wrong data type,
                    # throw it away.
                    if type(command[k]) not in v:
                        bad_cmds2.append(slot_id)
                        break

            # Delete all the malformed component commands

            for bc in bad_cmds2:
                del cmds[tick][bc]

            # We might have emptied all commands for this tick. Check for
            # empty again.
            # Empty dict, remove
            if len(slot_dict) == 0:
                bad_cmds1.append(tick)
                # log.LogDebug("COMMAND VALIDATOR: Empty Dict")
                continue

        # Delete all commands for this tick.

        for bc in bad_cmds1:
            del cmds[bc]

        return cmds


# test of command validator?
if __name__ == "__main__":
    cv = CommandValidator()

    cmd = {
        "0": {"0": {"command": "BROADCAST", "message": []}},
        "1": {"5": {"commad": "SET_RANGE", "range": 1.0}},
    }

    newcmd = cv.validate_commands(cmd)

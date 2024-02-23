# Creates a string out of the command dictionary.
# Nothing fancy. Used in logging.
def CmdToString(cmd):
    s = f"COMMAND: "
    for k, v in cmd.items():
        s += f"{k} [{str(v)}] "
    return s


def ActionToString(action):
    s = f"ACTION: "
    for k, v in action.data.items():
        s += f"{k} [{str(v)}] "
    return s

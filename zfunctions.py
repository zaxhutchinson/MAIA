def cmd_to_string(cmd):
    """Creates a string out of the command dictionary

    Used in logging
    """
    s = f"COMMAND: "
    for k, v in cmd.items():
        s += f"{k} [{str(v)}] "
    return s


def action_to_string(action):
    """Creates a string out of the action dictionary"""
    s = f"ACTION: "
    for k, v in action.data.items():
        s += f"{k} [{str(v)}] "
    return s

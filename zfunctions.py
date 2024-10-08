def cmd_to_string(cmd):
    """Creates a string out of the command dictionary

    Used in logging
    """
    s = "COMMAND: "
    for k, v in cmd.items():
        s += f"{k} [{str(v)}] "
    return s


def action_to_string(action):
    """Creates a string out of the action dictionary"""
    s = "ACTION: "
    for k, v in action.data.items():
        s += f"{k} [{str(v)}] "
    return s


def is_real(i):
    try:
        float(i)
    except Exception:
        return False
    else:
        return True


def is_int(i):
    """Tests if i can be cast to an int."""
    try:
        int(i)
    except Exception:
        return False
    else:
        return True


def to_bool(value):
    value = str(value).lower()
    if value in ["true", "t", "y", "1", "yes"]:
        return True
    else:
        return False

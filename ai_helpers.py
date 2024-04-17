import sys

##############################################################################
##############################################################################
# VIEW RELATED STUFF
##############################################################################
##############################################################################


def pretty_print_view(view, out=sys.stdout, indent=""):
    """View coming from the simulation

    This method will print an indented version of the view (dict of world state) using the
    output file specified. By default it sends output to stdout.
    Users can but in general should not need to pass in a value for indent.
    """
    if type(view) is not dict:
        # If view is a list, pass its contents back to the method.
        if view is list:
            for i in view:
                pretty_print_view(i, out, indent + "  ")
            return
        # If it isn't a list or dict, assume its a single value.
        else:
            out.write(": " + str(view))
            return

    # Print key and recurse.
    for k, v in view.items():
        out.write("\n" + indent + str(k))

        pretty_print_view(v, out, indent + "  ")

    out.write("\n")


def get_sub_view(view, *args):
    """Gets sub view (dict of world state)"""
    try:
        subview = view[args[0]]
        return get_sub_view(subview, *args[1:])
    except IndexError:
        return view
    except:
        return None


##################################################
# GETTERS FOR SELF VIEW DATA
def get_self(view):
    """Gets self"""
    return get_sub_view(view, "self")


def get_facing(view):
    """Gets self facing"""
    return get_sub_view(view, "self", "facing")


def get_health(view):
    """Gets self health"""
    return get_sub_view(view, "self", "health")


def get_damage(view):
    """Gets self damage"""
    return get_sub_view(view, "self", "damage")


def get_x(view):
    """Gets self x location"""
    return get_sub_view(view, "self", "x")


def get_y(view):
    """Gets self y location"""
    return get_sub_view(view, "self", "y")


def get_cell_x(view):
    """Gets self cell x location w/i cell"""
    return get_sub_view(view, "self", "cell_x")


def get_cell_y(view):
    """Gets self cell y location w/i cell"""
    return get_sub_view(view, "self", "cell_y")


def get_team_name(view):
    """Gets self team name"""
    return get_sub_view(view, "self", "teamname")


def get_call_sign(view):
    """Gets self call sign"""
    return get_sub_view(view, "self", "callsign")


def get_squad(view):
    """Gets self squad"""
    return get_sub_view(view, "self", "squad")


def get_comps(view):
    """Gets self components"""
    return get_sub_view(view, "self", "comps")


def get_comp_by_slot_id(view, slot_id):
    """Gets self components by slot id"""
    return get_sub_view(view, "self", "comps", slot_id)


def get_slot_ids_by_ctype(view):
    """Gets slot ids by ctype

    Returns a dictionary where k=ctype and v=[slot_ids]
    Good use is to call and store on T0 for future reference
    """
    comps_by_ctype = {}

    comps = get_comps(view)

    for slot_id, comp in comps.items():

        ctype = comp["ctype"]

        if ctype not in comps_by_ctype:
            comps_by_ctype[ctype] = []

        comps_by_ctype[ctype].append(slot_id)

    return comps_by_ctype


#####################################################
# Gun related functions
def can_weapon_fire(view, slotID):
    """Returns if given weapon can fire"""
    comp = get_comp_by_slot_id(view, slotID)
    return comp["reload_ticks_remaining"] == 0 and comp["ammunition"] > 0


def does_weapon_need_reloading(view, slotID):
    """Returns if given weapon needs reloading"""
    comp = get_comp_by_slot_id(view, slotID)
    return comp["reload_ticks_remaining"] > 0 and not comp["reloading"]


def is_weapon_reloading(view, slotID):
    """Returns if given weapon is reloading"""
    comp = get_comp_by_slot_id(view, slotID)
    return comp["reloading"]


##################################
# Search radar view for pings containing specific objnames.
# Returns a dictionary of pings that contain the objname.
# Each entry in the returned dict is a list keyed by direction.
#
def search_radar_for_obj_name(view, name):
    """Search radar view for pings containing specific objnames.

    Returns a dictionary of pings that contain the objname.
    Each entry in the returned dict is a list keyed by direction.
    """
    found_pings = []

    comp_views = get_sub_view(view, "comp")

    if comp_views is not None:
        radar_views = {}
        for cview in comp_views:
            radar_views = []
            # Find all comp views from radar components
            if cview["ctype"] == "Radar":
                radar_views.append(cview)

            # Search the radar views for pings with a matching obj name.
            for sv in radar_views:
                pings = sv["pings"]
                for p in pings:
                    if p["name"] == name:
                        found_pings.append(p)
    return found_pings


##############################################################################
# COMP VIEW


def get_comp_views_of_vtype(view, vtype):
    """Gets component views of a vtype

    Returns a list of all the views within the comp view with a specific vtype."""
    views = []
    comp_subview = get_sub_view(view, "comp")
    if comp_subview is not None:
        for cv in comp_subview:
            if cv["vtype"] == vtype:
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
        """Initializes empty command list"""
        self.cmds = {}

    def reset(self):
        self.cmds.clear()

    def get_cmds(self):
        return self.cmds

    def add_cmd(self, tick, slot, cmd):
        tick = str(tick)
        if tick not in self.cmds:
            self.cmds[tick] = {}
        self.cmds[tick][str(slot)] = cmd


##############################################################################
# FIXED GUN COMMAND FUNCTIONS


def cmd_fire():
    """Creates a fire command"""
    cmd = {}
    cmd["command"] = "FIRE"
    return cmd


def cmd_reload():
    """Creates a reload command"""
    cmd = {}
    cmd["command"] = "RELOAD"
    return cmd


##############################################################################
# ENGINE COMMAND FUNCTIONS


def cmd_turn(turnrate):
    """Creates a turn command"""
    cmd = {}
    cmd["command"] = "SET_TURNRATE"
    cmd["turnrate"] = turnrate
    return cmd


def cmd_set_speed(speed):
    """Creates a set speed command"""
    cmd = {}
    cmd["command"] = "SET_SPEED"
    cmd["speed"] = speed
    return cmd


##############################################################################
# RADAR COMMAND FUNCTIONS


def cmd_activate_radar():
    """Creates a radar transmission activation command"""
    cmd = {}
    cmd["command"] = "ACTIVATE_RADAR"
    return cmd


def cmd_deactivate_radar():
    """Creates a radar transmission deactivation command"""
    cmd = {}
    cmd["command"] = "DEACTIVATE_RADAR"
    return cmd


##############################################################################
# RADIO FUNCTIONS


def cmd_broadcast(message):
    """Creates a broadcast message command"""
    cmd = {}
    cmd["command"] = "BROADCAST"
    cmd["message"] = message
    return cmd


def cmd_set_range(_range):
    """Creates a range command"""
    cmd = {}
    cmd["command"] = "SET_RANGE"
    cmd["message"] = _range
    return cmd


##############################################################################
# ARM FUNCTIONS


def cmd_take_item_by_uuid(_uuid, location=None):
    """Create a pick up item (determined by uuid) command"""
    cmd = {}
    cmd["command"] = "TAKE_ITEM"
    cmd["item_name"] = None
    cmd["item_index"] = None
    cmd["item_uuid"] = _uuid
    cmd["location"] = location
    return cmd


def cmd_take_item_by_name(name, location=None):
    """Create a pick up item (determined by name) command"""
    cmd = {}
    cmd["command"] = "TAKE_ITEM"
    cmd["item_name"] = name
    cmd["item_index"] = None
    cmd["item_uuid"] = None
    cmd["location"] = location
    return cmd


def cmd_take_item_by_index(index, location=None):
    """Create a pick up item (determined by index) command"""
    cmd = {}
    cmd["command"] = "TAKE_ITEM"
    cmd["item_name"] = None
    cmd["item_index"] = index
    cmd["item_uuid"] = None
    cmd["location"] = location
    return cmd


def cmd_drop_item(location):
    """Create a drop item command"""
    cmd = {}
    cmd["command"] = "DROP_ITEM"
    cmd["location"] = location
    return cmd


##############################################################################
# GENERIC COMMAND FUNCTIONS


def cmd_activate():
    """Create a activate component command"""
    cmd = {}
    cmd["command"] = "ACTIVATE"
    return cmd


def cmd_deactivate():
    """Create a deactivate component command"""
    cmd = {}
    cmd["command"] = "DEACTIVATE"
    return cmd


##############################################################################
# JUNK STUFF


def sign(value):
    """Returns the sign of a value"""
    if value == 0:
        return 1
    else:
        return value / abs(value)

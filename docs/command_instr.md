Command Instructions
by zax

##############
#  OVERVIEW  #
##############

This document gives an overview how AI routines should construct commands. Commands
are basically elaborate dictionaries and they follow a general template:

{
    "<TICK>": {
        "<SLOT_ID>": {
            "command":"<COMMAND>",
            "OTHER_DATA": <VALUE>
            ...
        }
    }
}

"<TICK>" : indicates on which iterative tick the commands stored under it are supposed to execute.
    This value is different from the global tick. Each turn of play can consist of more than
    one tick. For example, if the scenario uses 5 ticks per turn and you want something to execute
    on the second tick of the turn, "<TICK>" would be "1". This highlights that ticks are numbered
    starting from zero each turn.

"<SLOT_ID>" : the component id that should get this command. It is possible some objects under
    AI control have more than one engine for instance; therefore, they are disambiguated by
    the slot they occupy. All components are listed in the self view sent to each object and each
    is stored according to their slot_id.

"command" : the command to execute. See the command_list.txt file.

"OTHER_DATA" : some commands require other data to execute. For example, the SET_SPEED command
    also requires the speed value. Some commands might have more than one extra data point.


##############
# Discussion #
##############

As you might have noticed, you can have more than one command issued per tick. However, the
dictionary structure does not permit more than one command per component. The CnC component
additionally limits the number of total commands that will be accepted by the simulation. If 
you send more commands in a tick than your CnC component allows, only the first N will be 
executed in the order they come off the dictionary.
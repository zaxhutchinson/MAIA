# Planned Features
This file describes the planned features and a status on the work for each.

### Logs
1. Detailed command and action logs for each AI so developers can examine after action details.
2. Verbose logs for a play-by-play within the simulation itself.
3. Make all logs visible through tabs within the simulation.

### WorldState
1. Holds general state info which can be changed by object and item manipulation.
2. Move victory conditions into WorldState
3. Monitor for item and object state checks.


# Problem List

### Order of Action Execution
1. There is a vital question (or set of questions) concerning the order that actions are executed for a given object. I am loathe to have it depend on the order in which lines of code appear in the program, so I would like the order itself programmable either at the simulation level or at the AI/obj level. For now, I've come down on the side of collecting all actions for a single tick and then executing them by type across all objects. This means that all obj's move orders will be executed before, say, their turn orders. The order of execution can be changed in main.json.
    1. The order of execution effects the outcome of a tick. Assuming an object's engine has a nonzero entry for turn rate and speed. Does the object turn first and then move? Or move, then turn? Does it fire and then move? Or move, the fire.
    2. Should actions for all object be executed in the same order within objects or even across objects? For example, should MAIA execute all TURN orders first before moving onto all MOVE orders? Or should the execution of actions be the same for all objects?
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

### Possible Default Virtual Worlds
1. Knockout
Maze where players knock each other back on collision, falling off the edge ends the game.
```json
"Map 2": {
    "name": "Knockback",
    "edge_obj_id": "cliff",
    "desc": "Maze where players knock each other back on collision, falling off the edge ends the game",
    "width": 10,
    "height": 10,
    "placed_objects": {},
    "placed_items": {
        "goal": [
            {
                "x": 1
            },
            {
                "x": 10
            },
            {
                "y": 1
            },
            {
                "y": 10
            }
        ]
    },
    "sides": {
        "Green": {
            "starting_locations": [
                [
                    3,
                    3
                ]
            ],
            "facing": 1,
            "color": "green"
        },
        "Blue": {
            "starting_locations": [
                [
                    3,
                    6
                ]
            ],
            "facing": 3,
            "color": "blue"
        },
        "Orange": {
            "starting_locations": [
                [
                    6,
                    3
                ]
            ],
            "facing": 1,
            "color": "orange"
        },
        "Yellow": {
            "starting_locations": [
                [
                    6,
                    6
                ]
            ],
            "facing": 3,
            "color": "yellow"
        }
    },
    "gameplay_mechanics": {
        "collision_action": "knockback",
        "knockback_distance": 2
    },
    "win_states": [
        "player_falls_off"
    ]
},
```
```json
"player_falls_off": [
    {
        "type": "OBJ_ITEMS_TOUCH",
        "items": ["cliff"],
        "objs": ["player"],
        "state": false,
        "msg":"Player falls off the map"
    }
]
```
Collision detect is not currently a feature in MAIA, and would need to be added for this to be a functional map.


# Problem List

### Order of Action Execution
1. There is a vital question (or set of questions) concerning the order that actions are executed for a given object. I am loathe to have it depend on the order in which lines of code appear in the program, so I would like the order itself programmable either at the simulation level or at the AI/obj level. For now, I've come down on the side of collecting all actions for a single tick and then executing them by type across all objects. This means that all obj's move orders will be executed before, say, their turn orders. The order of execution can be changed in main.json.
    1. The order of execution effects the outcome of a tick. Assuming an object's engine has a nonzero entry for turn rate and speed. Does the object turn first and then move? Or move, then turn? Does it fire and then move? Or move, the fire.
    2. Should actions for all object be executed in the same order within objects or even across objects? For example, should MAIA execute all TURN orders first before moving onto all MOVE orders? Or should the execution of actions be the same for all objects?

# PROJECT DESCRIPTION #
by zax              

## MAIA Breakdown

## The Map
MAIA's map consists of a 2D space that is broken into cells. Each cell represents a 1x1 space. All objects that are placed on the map occupy a single cell. However, within each cell, space is continuous. In other words, an object can move within the cell it currently occupies. When it moves out of the current cell, the map updates the cell in which it is located. The within cell x,y coordinates are in [0,1).

MAIA uses a hybrid map in order to simplify both movement and collision detection. Within-cell coordinates allow for an object to move sub-cell distances and to move in non-cardinal directions without having to fudge things so that diagonal movement is costlier. For example, if an object has an engine with speed 1, it could never move the 1.4 diagonal distance. Cells are used to simplify collision. If a projectile or explosion impacts a specific cell, the object in that cell is also impacted regardless of its location within the cell.

Collisions between moving objects are handled when an object tries to move into an occupied cell. The simulation prevents the movement and instead sets the within-cell coordinate to just inside the cell it tried to leave.

## The Components
Components are really the heart of the simulation. Each component is updated each tick during which two primary things happen: command processing and action issuing.

Components receive commands from AI scripts via the simulation. Components evaluate the command for legitimacy before implementing them. Some commands simply change the state of the component. Some cause the direct issuing of actions.

Actions are returned from component updates. They are passed back to the simulation. Actions represent requests by the component to change the world state. Some actions are issued without AI commands. If a component was sent to a particular state several ticks previously, that state may still cause the component to issue commands. Such as an engine with a non-zero speed will continue to issue MOVE commands until the speed is set to zero.

## The Objects
Objects are mostly just containers for components. They are the glue between simulation, AI and
components. They store data that involves all the components, such as x,y locations.

## Configuration
MAIA is configurable through JSON files. You can create new maps, objects, and components.
They are also used to set up teams.

* components.json
* maps.json
* objects.json

comprise the main library files by which you build scenarios. We will provide general template
docs for each of the above json files.

## Teams
All teams must be defined in the *teams.json* file under *settings*. Other than the *teams.json* definition, a team consists of a directory stored under *teams*. Each agent defined in the *teams json* entry must have a corresponding AI file with the same name as the one given in the *teams json* def. Example:

The following is a team definition taken from a sample *teams.json*.

```json
"TeamAlpha" : {
    "size" : 1,
    "name" : "TeamAlpha",
    "agent_defs" : [
        {
            "callsign": "Leader",
            "squad" : "A",
            "object" : "2",
            "AI_file" : "AI_file0.py"
        }
    ]
}
```

MAIA expects to find a directory in the *teams* directory matching the "name" field, TeamAlpha Likewise, for each agent_def, MAIA expects to find an AI file in that team directory with same name, AI_file0.py.

## AI
AI for objects is given by .py files stored under team directories. MAIA, using the teams.json file, loads the AI module for each agent of a participating team (See the file *ai.txt* for a precise reading of the AI class). MAIA creates an object of the AI class and uses the required routines to hook into user defined AI.

The simulation passes each AI object several views of the state of the world via a dictionary. It is up to the AI to parse the dictionary, interpret the data and send back commands.

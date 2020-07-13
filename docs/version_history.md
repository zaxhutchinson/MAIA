Version 0.08a
July 13, 2020
- Adds end of sim check. If only objects from a single team remain, sim ends.
- Adds in more documentation.

Version 0.07
July 12, 2020
- Some readme work
- Adds CnC components which primarily limit the number of commands an object can make.
- Adds a message queue to update the log
- Adds the start of several instruction files for users.
- First actual tests of the simulation in operation completed.

Version 0.06
July 11, 2020
- UI Updates
- Implements starting commands and actions.
- Adds first scanner comp and support code.
- Adds zmath
- Adds ai_helpers

Version 0.05
July 10, 2020
- Major rework. Converted from a continuous space to discrete grid. 
- Rewrote most of the storage and classes. 
- Moves toward a dictionary structure for all data.
- Moves sim building into Sim from App
- Fixes error with agent starting position

Version 0.04
July 8, 2020
- Adds starting_regions. This defines a box (left, right, top, bottom) for each
side in which they must pick a starting location.

Version 0.03
July 7, 2020
- Reworked Object and Shape moving data members around.
- Added in come preliminary collision detection
- Removed (temporarily) shapes other than Cylinder.
- Updated UI so that map sides and teams can be assigned via the UI.

Version 0.02
June 27, 2020
- Continued UI work: Added the ability to select teams and map.

Version 0.01
June 27, 2020
- Initial UI work
- Building objects from stored data
- Restructured data members into a dictionary with a basic way to require some
    variables and make others optional.

Init Version
June 27, 2020
- Basic structure of the objects, comps, map, and teams
- Loading of data from json files.
- No UI.
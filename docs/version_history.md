**Version 0.11**
July 20, 2020
- Adds todo.md.
- Adds very cluttery example AI. Just a test case for the various systems.
- First public version

**Version 0.10**
July 17, 2020
- Documentation work, specifically on views.
- AI helper functions and classes.

**Version 0.09**
July 14, 2020
- Changes UI names.
- Adds custom UI widgets to keep style consistent.
- Unifies the look of the AI.

**Version 0.08d**
July 14,2020
- Adds in the radio component ctype and a simple BROADCAST command. BROADCAST sends out a message to all objects on the map. Currently allowing the message to be almost anything. Might need changing.
- Adds an initial command validator. This will weed out malformed commands so the rest of the code does have be so damned paranoid about users sending back garbage. Will undoubtly need continual additions. Need to think about limiting sizes...possibly. Currently prints a mesage when the command is malformed. Need to move to a log.

**Version 0.08c**
July 13, 2020
- UI work on the Sim setup UI. Will eventually duplicate to the Sim itself. First stab at it.
- More cleaning of the docs.
- Adds initial exception handling. God that needs more work.

**Version 0.08b**
July 13, 2020
- More docs.
- Fixes ammunition check on reload command.

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
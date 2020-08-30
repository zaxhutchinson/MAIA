**Version 0.16**
August 30, 2020
- Adds a new component type (ctype) called 'Arm'. An arm can take and drop an item in the object's current cell. Arms can only hold 1 item at a time. Items will not be picked up if they are too heavy, bulky or if the arm is already holding an object.
- Changes held items remain graphically visible and retain, internally, their location; however, they are removed from the map cell. This prevents other objects from detecting them. TODO: Held items need to appear in a scanned object's view.
- Changes items so that their cell location is updated when the holding object moves.

**Version 0.15**
August 23, 2020
- Items are now visible in radar views. Items cannot block scans like objects.
- Renamed 'objname' data point to 'name'.

**Version 0.14**
August 22, 2020
- Reworked the destruction of objs. Destroyed objs can change color and are removed from the internal map list, but still show up on the map. However, they do not impede movement or lines of fire. Other objects cannot see them.
- Points have been added to objects. If points_count is true, then any damage done to objects of that type will award the damage amount as points to the damaging object. Damage as points cuts off when the total damage done to an object reaches the health amount.
- The order in which commands are carried out each tick is randomized.

**Version 0.13**
July 25, 2020
- Restructures tile and object tkinter drawing code to be more efficient. Large maps (200x200) have very little, if any, lag in redrawing now.
- Fixes major bug where sim tries to execute the commands of destroyed objects.
- Adds debug log. Debug log, when on, tracks user errors, e.g. ill-formed commands. This is different from the Error log, which tracks states into which MAIA should not find itself. They have been separated to provide a cleaner way for users to debug AI code.
- Destroyed objects now remain on the map. runAI and other methods are not called for destroyed objects. They become, in essence, a heap of indestructible rubble that prevents movement. So it is possible to block paths by destroying objects. Another data point was added to make a graphical change to destroyed objects by changing the color. Still needs more testing.
- Formally adds items. They are currently non-functional. They do not impede movement, but they do appear on the map. Functionality will require adding a new component type capable of picking up and storing items.

**Version 0.12**
July 23, 2020
- Adds ViewManager which creates a single place to template views. This will help creating views when there are more than one action capable of creating the same type of view.
- Adds the view.md file to document view templates.
- Renames the 'scanner' component to 'radar'. Makes slightly more sense. Can use the name 'scanner' to mean things that scan a 2d area, rather than just raycasts.
- Begins the process of adding the Item concept to MAIA. Items will have a location on the map, but not limit movement, like objects. They will not have components or AI. Necessary (perhaps) to introduce capture the flag mechanics, soccer, etc.

**Version 0.11a**
July 20, 2020
- Adds the agent facing entry to the maps.json to give agents a logical default facing. Setting the facing to "None" results in a random selection [0,360).

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
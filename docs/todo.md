# TODO
This file describes the list of bugs and features which need work.

* FIRE/SCAN path differences: The cell path of a scan ray can differ from the path of a fired projectile if the targeted cell are different distances. This can result in a scan saying a target is at X angle, but when the object fires on that hex, the hex is not included in the path of cells. Current fix: have AI recalculate angle based on target's x,y coords. Possible fix is to calculate direction after an object is encountered by the ray...rather than just return the ray's initial direction.
* Standarize the contents of the data dictionaries. Move the main reference into separate files for easy perusal.
    * WORK: Views are now standardized in the ViewManager
* Need to develop a solid log strategy. Sim will probably have several log levels. The verbose mode will write to a file. A terse mode will write the play-by-play to the in-UI log. AI will be responsible for logging information about its inner workings.
* Items: Need to create a component with commands to handle items.
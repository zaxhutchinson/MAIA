# Views and AI Helpers

This document describes the *views* returned from the simulation to user-defined AI scripts. It also speaks about the *ai_helpers.py* file.

## Views
A *view* is a dictionary sent to the *runAI* method of the *AI* class via its *data* parameter. The data parameter contains multiple views inside a single dictionary. A view is recursively defined.

### General View
The *general* view is always included in the data dictionary. It contains information about the world that would be common to any object inhabiting an environment, i.e. time. No commands need to be issued to receive this information each turn.

Contents

* tick: global time value.

### Self View
The *self* view contains current information about the object that the AI controls. No commands need to be issued in order to receive this information each turn.

Top-level Contents:

* health: the total health of the object. This is a static number
* damage: the total damage suffered by the object. This is subtracted from health. When the calculation reaches 0, the object is destroyed.
* facing: the world direction the object is facing.
* x: current x grid coordinate
* y: current y grid coordinate
* cell_x: current within grid-cell x coordinate [0-1)
* cell_y: current within grid-cell y coordinate [0-1)
* objname: name of the object given in the objects.json file.
* comps: a view of the current components

Comps View Contents
Different for each component. Keyed by component slot. Component information is (for the most part) identical to what is defined in the components.json file. However, when/if component health is implemented, that value will be found here. These views are necessary because components, more than the object itself, contain the state of the object (ammunition, engine speed, etc.).

### Comp View
This is not the same as the *comps* subview under the *self* view. The comp view contains information that was produced during the last tick(s) by the components themselves. For example, if a scan is issued, the results of the scan are inside the *comp* view keyed first by tick
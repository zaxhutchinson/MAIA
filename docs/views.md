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
This is not the same as the *comps* subview under the *self* view. The comp view contains information that was produced during the last tick(s) by the components themselves. For example, if a radar is issued, the results of the radar are inside the *comp* view keyed first by tick.

Values listed for each key are a mix of types: string, float, int, None. The value given is the default created by the ViewManager class. The comment gives the data type of the value when there is non-default data stored under a given key.

### projectile
```python
{
    'vtype': 'projectile',
    'compname': None # STRING: name of the component that caused this view to be created.
    'hit_x': None # INT: x-grid cell coordinate of the hit object. Default: None if no object was hit.
    'hit_y': None #INT: y-grid cell coordinate of the hit object. Default: None if no object was hit.
    'objname': None #STRING: objname of the object hit. Default: None if no object was hit.
}
```

### radar
```python
{
    'vtype': 'radar'
    'tick': None # INT: Stores the global tick as counted from the beginning of the simulation.
    'ctype': None # STRING: Stores the ctype (or component type) of the object creating this view.
    'compname': None # STRING: Stores the compname of the object creating this view.
    'slot_id': None # INT: Stores the slot index of the component that created this view.
    'pings': [] # ARRAY: Stores a list the objects pinged. (see ping details below).
}
```

#### ping details of the radar view
All pings will contained filled in values for the following keys.
```python
{
    'x': # INT:  The grid cell x-coordinate of the pinged object.
    'y': # INT: The grid cell y-coordinate of the pinged object.
    'objname': # STRING: The object name of the object pinged.
    'direction': # FLOAT: The direction [0-360) in degrees along which the object was detected.
    'cell_x': # FLOAT: The within cell x-coordiate.
    'cell_y': # FLAOT: The within cell y-coordiate.
}
```

### broadcast
```python
{
    'vtype': 'broadcast'
    'tick': None # INT: Stores the global tick as counted from the beginning of the simulation.
    'message': "" # STRING: The broadcasted message.
}
```
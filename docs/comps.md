# Component Descriptions

This file will describe each component type, or ctype. Each ctype carries with it its own data. This fill will be extended as additional ctypes are created or old ones are modified. This file gives a basic json example for each and then describes each data point within the dictionary.

Each component defined in the *comp.json* file is a template. When instances of the component are added to a new simulation this data is copied and more data is added by the sim.

## Common Data Points
The following data points are included in all components

* key: [STRING] Can be any string. Should match the id (not sure the code currently requires it, but it will eventually).
* id: [STRING] Same as the key. It is used to identify this particular component template.
* name: [STRING] A human-readable name. Not used for anything except descriptions and logs.
* ctype: [STRING] Very important. This determines how the sim expects this comp to function and what data is required. Giving the wrong ctype to a component with non-matching data will cause MAIA to crash.

## CnC
Command-n-Control

```json
"0": {
    "id":0,
    "name":"Basic Command Module",
    "ctype":"CnC",
    "max_cmds_per_tick":1
},
```
* max_cmd_per_tick: [INT]
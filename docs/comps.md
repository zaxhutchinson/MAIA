# Component Descriptions

This file will describe each component type, or ctype. Each ctype carries with it its own data. This fill will be extended as additional ctypes are created or old ones are modified. This file gives a basic json example for each and then describes each data point within the dictionary.

Each component defined in the *comp.json* file is a template. When instances of the component are added to a new simulation this data is copied and more data is added by the sim.

Dictionary keys are followed by the data type of the value and then a description of the value.

## Common Data Points
The following data points are included in all components

* key: [STRING] Can be any string. Should match the id (not sure the code currently requires it, but it will eventually).
* id: [STRING] Same as the key. It is used to identify this particular component template.
* name: [STRING] A human-readable name. Not used for anything except descriptions and logs.
* ctype: [STRING] Very important. This determines how the sim expects this comp to function and what data is required. Giving the wrong ctype to a component with non-matching data will cause MAIA to crash.

## CnC [Command-n-Control]. 
A CnC component models the command and control unit of the object (the brains).

```json
"0": {
    "id":"0",
    "name":"Basic Command Module",
    "ctype":"CnC",
    "max_cmds_per_tick":1
},
```
* max_cmd_per_tick [INT]: Limits the number of commands an AI can execute in a given tick. Currently, each component can accept 1 command per tick; therefore, the object AI could give a command to every component each turn. Reducing this below the number of components means an AI might have to choose what to do first.

## Engine
An engine has two jobs: 1) move the object around and 2) turn the object. Engines use continuous operations. Continuous ops in MAIA means that values do not reset between ticks. If you set a speed, it will remain set until you reset it.

```json
"2000" : {
    "id":"2000",
    "name":"Small Engine",
    "ctype":"Engine",
    "min_speed":-1.0,
    "max_speed":1.0,
    "cur_speed":0.0,
    "max_turnrate":90.0,
    "cur_turnrate":0.0
},
```
* min_speed [INT/FLOAT]: Maximum reverse speed of the engine. This was included to allow for objects that move at different speeds forward and backward.
* max_speed [INT/FLOAT]: Maximum forward speed of the engine.
* cur_speed [INT/FLOAT]: The current speed setting. Allows setting a starting speed. By default it should be 0.
* max_turnrate [INT/FLOAT]: This is the turn rate given in degrees. In the example above, the value is 90.0. This means that in a single tick, the engine can turn the object left or right by 90.0. So the useable values are -max_turnrate to max_turnrate. Negative values = left turn. Positive = right.

## Radar
By default objects and components receive no world state except what they know about themselves. Radars return external information. A radar consists of a series of raycasts at certain intervals. These simple radars transmit, by default, in the direction of the object. A ray will return object views for all objects it encounters. To be more precise, if a ray would encounter two objects, but the first blocks visibility of the second, only the first is returned.

```json
"3000": {
    "id":"3000",
    "name": "Simple 120/20/10 Radar",
    "ctype": "Radar",
    "active": false,
    "range":20,
    "level":1,
    "visarc":120,
    "offset_angle":0,
    "resolution":10
}
```
* active [BOOLEAN]: Currently unused. Might be removed in the future.
* range [INT/FLOAT]: The distance from the object the radar will return object information.
* level [INT]: The radar penetration value. Radar rays will penetrate any object with a *density* strictly less than their *level*, allowing radars to see behind objects.
* visarc [INT/FLOAT]: This is half the arc degrees transmitted by the radar. In the above example, the radar's *visarc* is 120. This means is transmits 120 degrees to the left and right of the object's facing.
* offset_angle [INT/FLOAT]: This swings the radar to point N degrees away from the facing of the object. For example, an *offset_angle* of 180 degrees would mean the radar points to the rear of the object.
* resolution [INT]: The interval at which transmit rays are emitted to cover the visible arc. For example, if the *visarc* were 10 and the *resolution* 10 as well, a radar command would produce three transmission rays at -10, 0, and 10.

## FixedGun
A fixed gun cannot move left and right. It points always in the direction of the vehicle.

```json
"1000": {
    "id":"1000",
    "name":"Main Cannon",
    "ctype":"FixedGun",
    "reload_ticks":1,
    "reload_ticks_remaining":0,
    "reloading":false,
    "ammunition":100,
    "min_damage":100,
    "max_damage":100,
    "range":10
},
```
* reload_ticks [INT]: The number of ticks it takes to reload the weapon.
* reload_ticks_remaining [INT]: Used by the simulation. Should be set to 0. This keeps track of how many ticks are left before the gun is reloaded.
* reloading [BOOLEAN]: Keeps track of whether the gun is reloading or not. Should start false unless, for some reason, you want the object to start unloaded and in the process of loading.
* ammunition [INT]: The number of shells left. When this reaches 0, the weapon cannot be fired.
* min_damage [INT/FLOAT]: The minimum damage inflicted by this weapon. Damage calculation is a random die roll [min_damage,max_damage]. If you want a non-random value, set both min and max to the same value.
* max_damage [INT/FLOAT]: Max damage of the weapon.
* range [INT/FLOAT]: Maximum range the gun can fire.

## Radio
A very basic radio with transmission and reception capabilities. It can broadcast a message. Cannot send targeted messages to a specific object.

```json
"4000": {
    "id": "4000",
    "name": "Basic Radio",
    "ctype": "Radio",
    "range": 100
    
}
```
* max_range [INT/FLOAT]: The maximum range setting of the radio.
* cur_range [INT/FLOAT]: The current range setting. Beyond this range, messages will not be heard.
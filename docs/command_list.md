# List of Commands
by zax

All components with of a specific ctype respond to the following commands.
If a command directly initiates an action, that action is noted just for reference.
Some commands do cause actions indirectly, such as setting the speed of an engine to
a non-zero number will cause the object to move.

## FixedGun
* **FIRE:** Fires the gun in the direction that the object is facing. Has no facing of its own
    * 'command': 'FIRE' 
    * action: 'HIGHSPEED_PROJECTILE'
* **RELOAD:** Begins the reloading process.
    * 'command': 'RELOAD'
    * action: None

## Engine
* **SET_SPEED:** Sets the speed of the engine. Speed must be within ['min_speed','max_speed'].
    * 'command': 'SET_SPEED'
    * 'speed': [FLOAT]
    * action: None
    
* **SET_TURNRATE:** Sets the turnrate of the engine. Turnrate must be withing['min_turnrate','max_turnrate']
    * 'command':'SET_TURNRATE'
    * 'turnrate': [FLOAT]
    * action: None

## Scanner
* **SCAN:** Initiates a one-time scan of the environment.
    * 'command':'SCAN'
    * action: 'SCAN'

## Radio
* **BROADCAST** Sends out a map-wide broadcast out to the range of the radio.
    * 'command':'BROADCAST'
    * action: 'BROADCAST'

* **SET_RANGE** Set the range of the radio up to the max_range.
    * 'command':'SET_RANGE'
    * 'range':[FLOAT]
    * action: None

        

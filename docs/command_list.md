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

## Radar
* **TRANSMIT_RADAR:** Initiates a one-time transmission.
    * 'command':'TRANSMIT_RADAR'
    * action: 'TRANSMIT_RADAR'

## Radio
* **BROADCAST** Sends out a map-wide broadcast out to the range of the radio.
    * 'command':'BROADCAST'
    * 'message':[INT,FLOAT,STR,LIST,TUPLE,DICT]
    * action: 'BROADCAST'

* **SET_RANGE** Set the range of the radio up to the max_range.
    * 'command':'SET_RANGE'
    * 'range':[FLOAT]
    * action: None

## Arm
* **TAKE_ITEM** Requests that the arm pick up an item.
    * 'command':'TAKE_ITEM'
    * 'location':'cell' or None
    * 'item_name':[STR] The name of the item to take.
    * 'item_index':[INT] The index of the item in the view list.
    * 'item_uuid':[STR] The assigned uuid of the item.

NOTES: If *location* is None, the arm will try to take from the current cell. Commands should only specify one item aspect (name, index or uuid). If more than 1 is provided, they are examined in the order (uuid, name, and index) taking the first match. If all are None, the arm tries to take the first item in the cell (default: *item_index*=0). In other words, unless the a cell contains a lot of items, a call to 'TAKE_ITEM' with all other data points set to None will cause the arm to pick up the only item in a cell.

* **DROP_ITEM** Requests that the arm drop the item it is holding.
    * 'command':'DROP_ITEM'
    * 'location': 'cell' or None

NOTES: Just like *TAKE_ITEM*, location determines were the item will be dropped. Currently, the only place to take or drop an item is the map cell. Eventually, I plan on adding storage compartments, so objects can store items.
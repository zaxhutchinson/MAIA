# Item Template Description

Items represent things on the map which are not controlled by AI. They have a location, but they do not block movement and cannot be destroyed. Their primary purpose is to provide a mechanism for tasks.

## Data
The data of items is the same across all items (currently). Items are in essence on-map flags. They have no self-serving purpose.

```json
"0": {
        "id":"0",
        "name":"flag",
        "weight":1,
        "bulk":1,
        "text":"B",
        "fill":"blue"
    }
```

* id [STR]: The id of the item.
* name [STR]: Generic name of the item.
* weight [INT/FLOAT]: Weight of the item.
* bulk [INT/FLOAT]: Bulk of the item (or the physical size).
* text [STR]: The char displayed on the map.
* fill [STR]: The color of the 'text' on the map. Should be a color name recognized by tkinter.
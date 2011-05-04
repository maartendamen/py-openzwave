#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
          1         2         3         4         5         6         7         8
 12345678901234567890123456789012345678901234567890123456789012345678901234567890
+--------------------------------------------------------------------------------+
| HomeSeer Z-Troller on /dev/keyspan-2                         Installer Library | 1
| Home ID 0x003d8522                                         Version Z-Wave 2.78 | 2
| 7 Registered Nodes (2 Sleeping)                                                | 3
|                                                                                | 4
| ID  Name          Location      Type                    State    Batt   Signal | 5
| 1   Controller                  Remote Controller       OK                     | 6    |
| 2   Sconce 1      Living Room   Multilevel Switch       [||||  ]        [||||] | 7    |
|>3   TV            Living Room   Binary Power Switch     on              [||| ] | 8    |
| 4   Liv Rm Motion Living Room   Motion Sensor           sleeping [||||] [||||] | 9    |
| 5   Sliding Door  Family Room   Door/Window Sensor      ALARM    [||| ] [||  ] | 10   +- Scrollable box, lists nodes
| 6   Sconce 2      Living Room   Multilevel Switch       [||||  ]        [||||] | 11   |
| 7   Bedroom Lamp  Master Bed    Multilevel Scene Switch on                     | 12   |
|                                                                                | 13   |
|                                                                                | 14   |
| Name:         TV                      | Command Classes                        | 15
| Location:     Living Room             | COMMAND_CLASS_BASIC                    | 16   |
| Manufacturer: Aeon Labs               | COMMAND_CLASS_HAIL                     | 17   |
| Product:      Smart Energy Switch     | COMMAND_CLASS_ASSOCIATION              | 18   |
| Neighbors:    2,4,5,6,7               | COMMAND_CLASS_VERSION                  | 19   |
| Version:      3                       | COMMAND_CLASS_SWITCH_ALL               | 20   |
| State:        On                      | COMMAND_CLASS_MANUFACTURER_SPECIFIC    | 21   +- Scrollable box, toggles:
| Signal:       3dbA (good)             | COMMAND_CLASS_CONFIGURATION            | 22   |  1) command classes
|                                       | COMMAND_CLASS_SENSOR_MULTILEVEL        | 23   |  2) values
|                                       | COMMAND_CLASS_METER                    | 24   |  3) groups
|        Add Del Edit Refresh + - oN oFf Values Groups Classes Setup Quit        | 25   |  4) config params
+---------------------------------------+----------------------------------------+

[a]add          - associate new node
[c]classes      - view command classes
[d]delete       - remove association
[e]edit         (COMMAND_CLASS_CONFIGURATION or has editable values)
[f]off          (command_class_switch_binary,command_class_switch_multilevel,COMMAND_CLASS_SWITCH_TOGGLE_BINARY,COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL)
[g]groups       (COMMAND_CLASS_ASSOCIATION)
[n]on           (command_class_switch_binary,command_class_switch_multilevel,COMMAND_CLASS_SWITCH_TOGGLE_BINARY,COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL)
[r]refresh      - refresh specified node
[s]setup
[+]increase     (COMMAND_CLASS_SWITCH_MULTILEVEL)
[-]decrease     (COMMAND_CLASS_SWITCH_MULTILEVEL)


'''
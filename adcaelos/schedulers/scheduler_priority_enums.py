#scheduler_priority_enums.py

from enum import Flag

class Scheduler_Priority_Enums(Flag):
    CONTROL         = 1
    NAVIGATION      = 2
    GUIDANCE        = 3
    SENSORS         = 4
    TRUTH           = 5
    LOWEST          = 6
    
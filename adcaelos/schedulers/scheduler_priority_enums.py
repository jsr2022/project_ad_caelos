#scheduler_priority_enums.py

from enum import IntEnum

class Scheduler_Priority_Enums(IntEnum):
    HIGHEST         = 1
    CONTROL         = 2
    NAVIGATION      = 3
    GUIDANCE        = 4
    SENSORS         = 5
    TRUTH           = 6
    LOWEST          = 7
    
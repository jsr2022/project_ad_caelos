#scheduler_priority_enums.py

from enum import IntEnum

class Scheduler_Priority_Enums(IntEnum):
    CONTROL         = 1
    NAVIGATION      = 2
    GUIDANCE        = 3
    SENSORS         = 4
    TRUTH           = 5
    LOWEST          = 6
    
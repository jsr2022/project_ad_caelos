#scheduler_enums.py
#Import Statements:
from enum import Flag, auto

class Scheduler_Enums(Flag):
    ACTIVE = auto()
    INACTIVE = auto()
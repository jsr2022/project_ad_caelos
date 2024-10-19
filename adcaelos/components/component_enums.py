#component_enums.py
#Import Statements:
from enum import Flag, auto

class Component_Enums(Flag):
    BASE_COMPONENT           = auto()
    TRUTH_COMPONENT          = auto()
    LOGIC_COMPONENT          = auto()
    CONTAINER_COMPONENT      = auto()
    OBJECT                   = auto()
    VEHICLE                  = auto()
    SUB_COMPONENT            = auto()
    TIME_VARYING_COMPONENT   = auto()
#component_enums.py
#Import Statements:
from enum import Flag, auto

class Component_Enums(Flag):
    BASE_COMPONENT = auto()
    DT_COMPONENT   = auto()
    OBJECT         = auto()
    VEHICLE        = auto()
    SUB_COMPONENT  = auto()
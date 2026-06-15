#scheduler_enums.py
#Import Statements:
from enum import Flag, auto

class Scheduler_Enums(Flag): # pylint: disable=invalid-name
    """
    _Scheduler_Enums contains the 'on' or 'off' enum to include the object in the heap_

    Parameters
    ----------
    Flag : _enum_
        _ACTIVE - means the object is included in the heap_
        _INACTIVE - means the object is not included in the heap_
    """
    ACTIVE = auto()
    INACTIVE = auto()
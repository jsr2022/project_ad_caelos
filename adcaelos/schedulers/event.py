# Import Python Default Library Packages
from dataclasses import dataclass, field
from datetime import datetime

from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

@dataclass(order=True)
class Event:
    time: float
    priority: Scheduler_Priority_Enums
    component: object = field(compare=False)
    action: str = field(compare=False)
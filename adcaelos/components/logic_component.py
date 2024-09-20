#logic_component.py
import numpy as np
from adcaelos.components.base_component import Base_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.scheduler.scheduler_enums import Scheduler_Enums

class Logic_Component(Base_Component):

    def __init__(self, name: str = "Logic_Component", UUID: int = None, executionOrder: int = -1) -> None:
        super().__init__(Component_Enums.LOGIC_COMPONENT, name, UUID) 
        self.executionOrder = executionOrder
        self.operationalStatus = Scheduler_Enums.INACTIVE
    
    def setOperationalStatus(self, operationStatus: Scheduler_Enums) -> None:
        self.operationalStatus = Scheduler_Enums.operationalStatus
    
    def getOperationalStatus(self) -> Scheduler_Enums:
        return self.operationalStatus
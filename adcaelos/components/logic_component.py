#logic_component.py
import numpy as np
from adcaelos.components.component_enums import Component_Enums
from adcaelos.components.base_component import Base_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.schedulers.scheduler_enums import Scheduler_Enums

class Logic_Component(Base_Component):

    def __init__(self, truthComp: Truth_Component, name: str = "Logic_Component", UUID: int = None, executionOrder: int = -1) -> None:
        super().__init__(Component_Enums.LOGIC_COMPONENT, name, UUID) 
        self.executionOrder = executionOrder
        self.operationalStatus = Scheduler_Enums.INACTIVE
        self.truthComp_s = truthComp
    
    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + f"\nExecution Order: {self.getExecutionOrder()}.\nOperational Status: {self.getOperationalStatus()}.\nConnected Truth Component:"
        msgStr = msgStr + self.truthComp_s.__str__()
        return msgStr

    def logicCenter(self) -> None:
        """Where Autonomy + GNC lives"""
        pass

    def setOperationalStatus(self, operationStatus: Scheduler_Enums) -> None:
        self.operationalStatus = Scheduler_Enums.operationalStatus
    
    def getOperationalStatus(self) -> Scheduler_Enums:
        return self.operationalStatus
    
    def setExecutionOrder(self, executionOrder) -> None:
        self.executionOrder = executionOrder

    def getExecutionOrder(self) -> int:
        return self.executionOrder
    
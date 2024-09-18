#dt_component.py
import numpy as np
from adcaelos.components.base_component import Base_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.scheduler.scheduler_enums import Scheduler_Enums

class Dt_Component(Base_Component):

    def __init__(self, name: str = "Dt_Component", UUID: int = None, executionOrder: int = -1, frequency: int = 100, integratorType: Integrator_Enums = Integrator_Enums.RK4) -> None:
        super().__init__(Component_Enums.DT_COMPONENT, name, UUID) 
        self.executionOrder = executionOrder
        self.operationalStatus = Scheduler_Enums.INACTIVE
        self.__frequency = frequency
        self.__integratorType = integratorType

    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + "\nADDSTUFFHERE"
        return msgStr
    
    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        pass
    
    def setCurrState(self, currState: np.array) -> None:
        #ADD CHECK ARRAY DIMENSIONS
        self.currState = currState

    def getCurrState(self) -> np.array:
        return self.currState
    
    def setCurrCntrl(self, currCntrl: np.array) -> None:
        #ADD CHECK ARRAY DIMENSIONS
        self.currCntrl = currCntrl

    def getCurrCntrl(self) -> np.array:
        return self.currCntrl
    
    def setOperationalStatus(self, operationStatus: Scheduler_Enums) -> None:
        self.operationalStatus = Scheduler_Enums.operationalStatus
    
    def getOperationalStatus(self) -> Scheduler_Enums:
        return self.operationalStatus
    
    def initialize(self, initialCond: np.array) -> None:
        #ADD CHECK ARRAY DIMENSIONS
        self.getCurrState(initialCond)
        self.setOperationalStatus(Scheduler_Enums.ACTIVE)
    
    def getFrequency(self) -> int:
        return self.__frequency

    def getIntegratorType(self) -> Integrator_Enums:
        return self.__integratorType
    


        
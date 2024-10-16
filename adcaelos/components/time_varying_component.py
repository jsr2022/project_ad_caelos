#time_varying_component.py

import numpy as np
from adcaelos.components.base_component import Base_Component
from adcaelos.components.component_enums import Component_Enums

class Time_Varying_Component(Base_Component):

    def __init__(self, nextTime: float = -1, frequency: int = 100, Component_Enum = Component_Enums.TIME_VARYING_COMPONENT, name: str = "Time_Varying_Component", UUID: int = None) -> None:
        super().__init__(Component_Enum, name, UUID)
        self.nextTime = nextTime
        self.__frequency = frequency
        self.__period = 1/frequency
    
    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + f"\nNext Time: {self.getNextTime()} [s].\nFrequency: {self.getFrequency()} [Hz].\nPeriod: {self.getPeriod()} [s]."
        return msgStr
    
    def setNextTime(self) -> None:
        currTime = self.getNextTime()
        self.nextTime = currTime + self.getPeriod()
    
    def getNextTime(self) -> float:
        return self.nextTime
        
    def getFrequency(self) -> int:
        return self.__frequency
    
    def getPeriod(self) -> float:
        return self.__period
#time_varying_component.py

#from python base package(s)
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.components.base_component import Base_Component
from adcaelos.components.connect_container_component import Connect_Container_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

class Time_Varying_Component(Base_Component, Connect_Container_Component, ABC):

    def __init__(self, frequency: int = 100, nextTime: float = 0, scheduler_priority_enum=Scheduler_Priority_Enums.LOWEST, Component_Enum=Component_Enums.TIME_VARYING_COMPONENT, name: str = "Time_Varying_Component", UUID: int = None) -> None:
        # Correctly initialize Base_Component with the proper arguments
        Base_Component.__init__(self, comptype=Component_Enum, name=name, UUID=UUID)
        Connect_Container_Component.__init__(self)
        self.nextTime = nextTime
        self.__scheduler_priority_enum = scheduler_priority_enum
        self.__frequency = frequency
        self.__period = float(1 / frequency)
    
    def __str__(self) -> str:
        msgStr = Base_Component.__str__(self)
        msgStr = msgStr + Connect_Container_Component.__str__(self)
        msgStr = msgStr + f"\nNext Time: {self.getNextTime()} [s].\nFrequency: {self.getFrequency()} [Hz].\nPeriod: {self.getPeriod()} [s]."
        return msgStr
     
    @abstractmethod
    def act(self) -> None:
        """
        _This class will implement whatever action is undertaken (for truth components it is running an integrator)
        """
        
    def setNextTime(self, next_time: float = np.nan) -> None:
        if isinstance(next_time, np.nan):
            currTime = self.getNextTime()
            self.nextTime = currTime + self.getPeriod()
        else:
            self.nextTime = next_time # allows for opportunity to do non-fixed step integration
    
    def getNextTime(self) -> float:
        return self.nextTime
        
    def getFrequency(self) -> int:
        return self.__frequency
    
    def getPeriod(self) -> float:
        return self.__period
    
    def setSchedulerPriorityEnum(self, new_scheduler_priority_enum: Scheduler_Priority_Enums) -> None:
        self.__scheduler_priority_enum = new_scheduler_priority_enum

    def getSchedulerPriorityEnum(self) -> Scheduler_Priority_Enums:
        return self.__scheduler_priority_enum
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

    def __init__(self, frequency: int = 100, nextTime: float = 0, scheduler_priority_enum = Scheduler_Priority_Enums.LOWEST, Component_Enum = Component_Enums.TIME_VARYING_COMPONENT, name: str = "Time_Varying_Component", UUID: int = None) -> None:
                      #frequency,            nextTime,            Scheduler_Priority_Enums.TRUTH,                                                      Component_Enum,                                          name,                                 UUID
        Base_Component.__init__(self, Component_Enum, name, UUID)
        self.nextTime = nextTime
        self.scheduler_priority_enum = scheduler_priority_enum
        self.__frequency = frequency
        self.__period = float(1/frequency)
    
    def __str__(self) -> str:
        msgStr = Base_Component.__str__(self)
        msgStr = msgStr + Connect_Container_Component.__str__(self)
        msgStr = msgStr + f"\nNext Time: {self.getNextTime()} [s].\nFrequency: {self.getFrequency()} [Hz].\nPeriod: {self.getPeriod()} [s]."
        return msgStr

    #@abstractmethod
    def subsystemMethod(self):
        """This function must be overridden in a subclass"""
        pass

    def setNextTime(self) -> None:
        currTime = self.getNextTime()
        self.nextTime = currTime + self.getPeriod()
    
    def getNextTime(self) -> float:
        return self.nextTime
        
    def getFrequency(self) -> int:
        return self.__frequency
    
    def getPeriod(self) -> float:
        return self.__period
    
    def setSchedulerPriorityEnum(self, new_scheduler_priority_enum: Scheduler_Priority_Enums) -> None:
        self.scheduler_priority_enum = new_scheduler_priority_enum

    def getSchedulerPriorityEnum(self) -> Scheduler_Priority_Enums:
        return self.scheduler_priority_enum
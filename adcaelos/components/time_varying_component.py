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

    def __init__(self, frequency: int = 100, next_time: float = 0, scheduler_priority_enum=Scheduler_Priority_Enums.LOWEST, Component_Enum=Component_Enums.TIME_VARYING_COMPONENT, name: str = "Time_Varying_Component", UUID: int = None) -> None:
        # Correctly initialize Base_Component with the proper arguments
        Base_Component.__init__(self, component_type=Component_Enum, name=name, UUID=UUID)
        Connect_Container_Component.__init__(self)
        self.__next_time = float(next_time)
        self.__scheduler_priority_enum = scheduler_priority_enum
        self.__frequency = frequency
        self.__period = float(1.0 / frequency)
        # Integer-step counter: next_time = __start_counter_time + __step_count / __frequency
        self.__start_counter_time = self.__next_time
        self.__step_count = 0
        
    def __str__(self) -> str:
        msgStr = Base_Component.__str__(self)
        msgStr = msgStr + "\nThis Component is a member of the following container:"\
                        + Connect_Container_Component.__str__(self)

        msgStr = msgStr + f"\nNext Time: {self.get_time()} [s].\nFrequency: {self.get_frequency()} [Hz].\nPeriod: {self.get_period()} [s]."
        return msgStr
    
    @abstractmethod
    def act(self) -> None:
        """
        _This class will implement whatever action is undertaken (for truth components it is running an integrator)_
        """
        
    def set_next_time(self, next_time: float = None, next_frequency: int = None) -> None:
        if next_time is None:
            self.__step_count += 1
            self.__next_time = self.__start_counter_time + self.__step_count / self.__frequency
        elif next_time is not None and next_frequency is not None:
            # Non-fixed step override: re-anchor the counter so subsequent
            # default calls continue from this explicit time without drift.
            self.__start_counter_time = float(next_time)
            self.__step_count = 0
            self.set_frequency(next_frequency)
            self.__next_time = self.__start_counter_time
        else:
            error_message = f"Invalid arguments for set_next_time: next_time={next_time}, next_frequency={next_frequency}. Must provide either no arguments or both next_time and next_frequency."
            raise ValueError(error_message)

    def get_time(self) -> float:
        return self.__next_time
    
    def get_frequency(self) -> int:
        return self.__frequency
    
    def get_period(self) -> float:
        return self.__period
    
    def setSchedulerPriorityEnum(self, new_scheduler_priority_enum: Scheduler_Priority_Enums) -> None:
        self.__scheduler_priority_enum = new_scheduler_priority_enum

    def getSchedulerPriorityEnum(self) -> Scheduler_Priority_Enums:
        return self.__scheduler_priority_enum

    def set_frequency(self, new_frequency: int) -> None:
        """Change frequency mid-simulation. Re-anchors counter so subsequent
        steps remain drift-free."""
        if new_frequency <= 0:
            error_message = f"Frequency must be positive. Got {new_frequency}."
            raise ValueError(error_message)
        # Preserve current time as new anchor
        self.__start_counter_time = self.__next_time
        self.__step_count = 0
        self.__frequency = new_frequency
        self.__period = 1.0 / new_frequency
    
    def getStepCount(self) -> int:
        """_Return current integer step count (for debugging)._"""
        return self.__step_count
    
    def getStartCounterTime(self) -> float:
        """_Return the anchor time from which the step count is calculated (for debugging)._"""
        return self.__start_counter_time

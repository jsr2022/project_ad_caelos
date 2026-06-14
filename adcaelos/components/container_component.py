#container_component.py

from typing import List

from adcaelos.components.base_component import Base_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.components.logic_component import Logic_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.schedulers.scheduler_enums import Scheduler_Enums

class Container_Component(Base_Component):
    def __init__(self, a_Logic_Component: Logic_Component, a_Truth_Component: Truth_Component, Time_Varying_Components: list[Time_Varying_Component]=[], operationalStatus=Scheduler_Enums.ACTIVE, Component_Enum=Component_Enums.CONTAINER_COMPONENT, name: str = "Container_Component", UUID: int = None) -> None:
        super().__init__(Component_Enum, name, UUID)
        # This connects the components to the container
        self.LC = a_Logic_Component
        self.TC = a_Truth_Component
        self.TVCs = Time_Varying_Components
        # This connects the container to the components
        self.LC.setContainerComponent(self)
        self.TC.setContainerComponent(self)
        for TVC in self.TVCs:
            TVC.setContainerComponent(self)

        self.operationalStatus = operationalStatus



    def __str__(self) -> str:
        message_string_TVC = ""
        for TVC in self.TVCs:
            # message_string_TVC = message_string_TVC + f"\n{TVC.getType()} UUID: {TVC.get_UUID()} Name: {TVC.get_name()}"
            message_string_TVC = message_string_TVC + f"\n{TVC.__str__()}"
        message_string = super().__str__()
        message_string = message_string + f"\nOperational Status: {self.operationalStatus}"
        message_string = message_string + f"\n{self.LC.__str__()}"
        message_string = message_string + f"\n{self.TC.__str__()}"
        message_string = message_string + "\n---------------Time Varying Components---------------"\
                        + message_string_TVC

        # message_string = message_string + f"\n{self.LC.getType()} UUID: {self.LC.get_UUID()} Name: {self.LC.get_name()}"\
        #                 + f"\n{self.TC.getType()} UUID: {self.TC.get_UUID()} Name: {self.TC.get_name()}"\
        #                 + "\n---------------Time Varying Components---------------"\
        #                 + message_string_TVC
        
        return message_string
    
    def getLC(self) -> Logic_Component:
        return self.LC
    
    def getTC(self) -> Truth_Component:
        return self.TC
    
    def getTVC(self) -> list[Time_Varying_Component]:
        return self.TVCs
    
    def setOperationalStatus(self, newOperationalStatus: Scheduler_Enums) -> None:
        self.operationalStatus = newOperationalStatus
    
    def getOperationalStatus(self) -> Scheduler_Enums:
        return self.operationalStatus

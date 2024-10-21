#container_component.py

from adcaelos.components.base_component import Base_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.components.logic_component import Logic_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.schedulers.scheduler_enums import Scheduler_Enums

class Container_Component(Base_Component):

    def __init__(self,Logic_Component: Logic_Component, Truth_Component: Truth_Component, Time_Varying_Components: Time_Varying_Component = [], Component_Enum = Component_Enums.CONTAINER_COMPONENT, name: str = "Container_Component", UUID: int = None) -> None:
        super().__init__(Component_Enum, name, UUID)
        # This connects the components to the container
        self.LC = Logic_Component
        self.TC = Truth_Component
        self.TVCs = Time_Varying_Components
        # This connects the container to the components
        self.LC.setContainerComponent(self)
        self.TC.setContainerComponent(self)
        for TVC in self.TVCs:
            TVC.setContainerComponent(self)

        self.operationalStatus = Scheduler_Enums.INACTIVE



    def __str__(self) -> str:
        msgStr_TVC = ""
        for TVC in self.TVCs:
            msgStr_TVC = msgStr_TVC + f"\n{TVC.getType()} UUID: {TVC.getUUID()} Name: {TVC.getName()}"
        msgStr = super().__str__()
        msgStr = msgStr + f"\nOperational Status: {self.operationalStatus}"
        msgStr = msgStr + f"\n{self.LC.getType()} UUID: {self.LC.getUUID()} Name: {self.LC.getName()}"\
                        + f"\n{self.TC.getType()} UUID: {self.TC.getUUID()} Name: {self.TC.getName()}"\
                        + "\n---------------Time Varying Logic Components---------------"\
                        + msgStr_TVC
        return msgStr
    
    def getLC(self) -> Logic_Component:
        return self.LC
    
    def getTC(self) -> Truth_Component:
        return self.TC
    
    def getTVC(self) -> Time_Varying_Component:
        return self.TVC
    
    def setOperationalStatus(self, operationStatus: Scheduler_Enums) -> None:
        self.operationalStatus = Scheduler_Enums.operationalStatus
    
    def getOperationalStatus(self) -> Scheduler_Enums:
        return self.operationalStatus
                        
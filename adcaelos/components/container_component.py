#container_component.py

from base_component import Base_Component
from component_enums import Component_Enums
from logic_component import Logic_Component
from truth_component import Truth_Component
from time_varying_component import Time_Varying_Component

class Container_Component(Base_Component):

    def __init__(self,Logic_Component: Logic_Component, Truth_Component: Truth_Component, Time_Varying_Component: Time_Varying_Component = [], Component_Enum = Component_Enums.CONTAINER_COMPONENT, name: str = "Container_Component", UUID: int = None) -> None:
        self.LC = Logic_Component
        self.TC = Truth_Component
        self.TVC = Time_Varying_Component

    def __str__(self) -> str:
        msgStr_TVC = ""
        for TVC in self.TVC:
            msgStr_TVC = msgStr_TVC + f"\n{TVC.getType()} UUID: {TVC.getUUID()} Name: {TVC.getName()}"
        msgStr = super().__str__()
        msgStr = msgStr + f"\n{self.LC.getType()} UUID: {self.LC.getUUID()} Name: {self.LC.getName()}"\
                        + f"\n{self.TC.getType()} UUID: {self.TC.getUUID()} Name: {self.TC.getName()}"\
                        + msgStr_TVC
        return msgStr
    
    def getLC(self) -> Logic_Component:
        return self.LC
    
    def getTC(self) -> Truth_Component:
        return self.TC
    
    def getTVC(self) -> Time_Varying_Component:
        return self.TVC
                        
#logic_component.py
import numpy as np

from adcaelos.components.base_component import Base_Component
from adcaelos.components.connect_container_component import Connect_Container_Component
from adcaelos.components.component_enums import Component_Enums

class Logic_Component(Base_Component, Connect_Container_Component):

    def __init__(self, name: str = "Logic_Component", UUID: int = None) -> None:
        super().__init__(Component_Enums.LOGIC_COMPONENT, name, UUID) 
        
    def __str__(self) -> str:
        msgStr = Base_Component.__str__(self)
        msgStr = msgStr + Connect_Container_Component.__str__(self)
        return msgStr

    def logicCenter(self) -> None:
        """Where Autonomy + GNC lives"""
        pass

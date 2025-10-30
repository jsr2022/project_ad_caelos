#logic_component.py

#from python base package(s)
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.components.base_component import Base_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.components.connect_container_component import Connect_Container_Component

class Logic_Component(Base_Component, Connect_Container_Component, ABC):

    def __init__(self, name: str = "Logic_Component", UUID: int = None) -> None:
        Base_Component.__init__(Component_Enums.LOGIC_COMPONENT, name, UUID)
        Connect_Container_Component.__init__(self)
        
    def __str__(self) -> str:
        msgStr = Base_Component.__str__(self)
        msgStr += Connect_Container_Component.__str__(self)
        return msgStr
    
    #@abstractmethod
    def logicCenter(self) -> None:
        """Where Autonomy + GNC lives: Implemented at Sub Class Level"""
        pass

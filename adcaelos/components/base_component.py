#base_component.py
#Imports:
import numpy as np
import uuid
# from sys import exit
from adcaelos.components.component_enums import Component_Enums
class Base_Component:

    def __init__(self, component_type: Component_Enums = Component_Enums.BASE_COMPONENT, name: str = "Base_Component", UUID: int = None) -> None:
        self.__type = component_type
        self.__name = name
        if UUID is None:
            self.__UUID = uuid.uuid4().int % (2**32) #32 bit integer
        else:
            self.__UUID = UUID

    def __str__(self) -> str:
        return f"This is a component class of type {self.getType()}.\nIt has the Name: {self.get_name()}.\nIts UUID is {self.get_UUID()}."

    def get_UUID(self) -> int:
        return self.__UUID

    def get_name(self) -> str:
        return self.__name
    
    def getType(self) -> Component_Enums:
        return self.__type
        



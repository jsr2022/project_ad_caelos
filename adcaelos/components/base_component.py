#base_component.py
#Imports:
import numpy as np
import uuid
# from sys import exit
from adcaelos.components.component_enums import Component_Enums
class Base_Component:

    def __init__(self, comptype: Component_Enums = Component_Enums.BASE_COMPONENT, name: str = "Base_Component", UUID: int = None) -> None:
        self.__type = comptype
        self.__name = name
        if UUID is None:
            self.__UUID = uuid.uuid4().int % (2**32) #32 bit integer
        else:
            self.__UUID = UUID

    def __str__(self) -> str:
        return f"This is a component class of type {self.getType()}.\nIt has the Name: {self.getName()}.\nIts UUID is {self.getUUID()}."

    def getUUID(self) -> int:
        return self.__UUID

    def getName(self) -> str:
        return self.__name
    
    def getType(self) -> Component_Enums:
        return self.__type
        



#connect_container_component.py
#from adcaelos.components.container_component import Container_Component
#Note: Performing the import above creates a loop in the imports. By removing it, the loop disappears
#Note: This warrants further investigation...

class Connect_Container_Component():
    
    def __init__(self) -> None:
        self.__container_component = None

    def __str__(self) -> str:
        return f"\nContainer Component UUID: {self.__container_component.getUUID()}. Container Component Name: {self.__container_component.getName()}"
    
    def setContainerComponent(self, container_component) -> None:
        self.__container_component = container_component

    def getContainerComponent(self): #-> Container_Component:
        return self.__container_component
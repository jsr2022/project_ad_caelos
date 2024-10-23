#connect_container_component.py
#from adcaelos.components.container_component import Container_Component
#Note: Performing the import above creates a loop in the imports. By removing it, the loop disappears
#Note: This warrants further investigation...

class Connect_Container_Component():
    
    def __init__(self) -> None:
        self.__containerComponent = None

    def __str__(self) -> str:
        return f"\nContainer Component UUID: {self.__containerComponent.getUUID()}. Container Component Name: {self.__containerComponent.getName()}"
    
    def setContainerComponent(self, containerComponent) -> None:
        self.__containerComponent = containerComponent

    def getContainerComponent(self): #-> Container_Component:
        return self.__containerComponent
#connect_container_component.py

class Connect_Container_Component:
    def __init__(self) -> None:
        self.__containerComponent = None

    def __str__(self) -> str:
        if self.__containerComponent:
            return f"\nContainer Component UUID: {self.__containerComponent.getUUID()}. Container Component Name: {self.__containerComponent.getName()}"
        return "\nContainer Component: None"

    def setContainerComponent(self, containerComponent) -> None:
        self.__containerComponent = containerComponent

    def getContainerComponent(self):
        return self.__containerComponent
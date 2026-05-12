#connect_container_component.py

class Connect_Container_Component:
    """
    This class connects all of the various components together for a vehicle so they know what truth or logical pieces they directly interact with
    """
    def __init__(self) -> None:
        self.__containerComponent = None

    def __str__(self) -> str:
        if self.__containerComponent:
            return f"\nContainer Component Name: {self.__containerComponent.get_name()} Container Component UUID: {self.__containerComponent.get_UUID()}."
        return "\nContainer Component: None"

    def setContainerComponent(self, containerComponent) -> None:
        self.__containerComponent = containerComponent

    def getContainerComponent(self):
        return self.__containerComponent
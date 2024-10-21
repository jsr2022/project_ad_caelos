#truth_component.py
from sys import exit
import numpy as np
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.connect_container_component import Connect_Container_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

class Truth_Component(Time_Varying_Component, Connect_Container_Component):

    def __init__(self, statePos2Names: dict, stateNames2Pos: dict, integratorType: Integrator_Enums = Integrator_Enums.RK4, nextTime: float = -1, frequency: int = 100, Component_Enum = Component_Enums.TRUTH_COMPONENT, name: str = "Truth_Component", UUID: int = None) -> None:
        super().__init__(nextTime, frequency, Scheduler_Priority_Enums.TRUTH, Component_Enum, name, UUID) 
        self.__statePos2Names = statePos2Names #dictionary of keys (state indices in state vector) to values (state names) 
        self.__stateNames2Pos = stateNames2Pos #dictionary of keys (state names) to values (state indices in state vector) 
        self.__integratorType = integratorType

    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + f"\nIntegrator Type: {self.getIntegratorType()}"
        #ADD PRINTING OUT STATE NUMBER TO STATE NAME
        return msgStr

    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        #ADD CHECK ARRAY DIMENSIONS
        pass
    
    def setCurrState(self, currState: np.array) -> None:
        #ADD CHECK ARRAY DIMENSIONS
        self.currState = currState

    def getCurrState(self) -> np.array:
        return self.currState
    
    def setCurrCntrl(self, currCntrl: np.array) -> None:
        #ADD CHECK ARRAY DIMENSIONS
        self.currCntrl = currCntrl

    def getCurrCntrl(self) -> np.array:
        return self.currCntrl
        
    def getIntegratorType(self) -> Integrator_Enums:
        return self.__integratorType
    
    def getStatePos2Names(self, indices = None):
        if indices is None:
            return np.array(list(self.__statePos2Names.values()))
        elif isinstance(indices, int):
            if indices not in self.__statePos2Names:
                raise KeyError(f"Key {key} not found in dictionary")
            return np.array(self.__statePos2Names[indices])
        elif isinstance(indices, np.ndarray): 
            stateNames = []
            for key in indices:
                if key not in self.__statePos2Names:
                    raise KeyError(f"Key {key} not found in dictionary")
                stateNames.append(self.__statePos2Names[key])
            return np.array(stateNames) #I am storing the string arrays in np arrays maybe a bad idea...
        else:
            print("Error: Improper Key Type Not In Dictionary") #add indices type, also add to logger
            exit(1)

    def getStateNames2Pos(self, indices = None):
        if indices is None:
            return np.array(list(self.__stateNames2Pos.values()))
        elif isinstance(indices, str): #I am storing the string arrays in array of strings
            statePos = []
            for key in indices:
                if key not in self.__stateNames2Pos:
                    raise KeyError(f"Key {key} not found in dictionary")
                statePos.append(self.__stateNames2Pos[key])
            return np.array(statePos)
        else:
            print("Error: Improper Key Type Not In Dictionary") #add indices type, also add to logger
            exit(1)  
    
    # def getUpdate(self) -> bool:
    #     if np.mod(self.getCurrTime(), 1/self.getFrequency()) == 0:
    #         return True
    #     else:
    #         return False

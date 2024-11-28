#truth_component.py

#from python base package(s)
from sys import exit
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.utilities import sim_utils
from adcaelos.components.time_varying_component import Time_Varying_Component

from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

class Truth_Component(Time_Varying_Component, ABC):

    def __init__(self, stateNames: list, integratorType: Integrator_Enums = Integrator_Enums.RK4, frequency: int = 100, nextTime: float = 0, Component_Enum = Component_Enums.TRUTH_COMPONENT, name: str = "Truth_Component", UUID: int = None) -> None:
        Time_Varying_Component.__init__(self, frequency, nextTime, Scheduler_Priority_Enums.TRUTH, Component_Enum, name, UUID) 
        statePos2Names = sim_utils.checkUniqueStateNames(stateNames) #will call
        stateNames2Pos = sim_utils.convertDictionaryIndex2State(statePos2Names)
        self.__statePos2Names = statePos2Names #dictionary of keys (state indices in state vector) to values (state names) 
        self.__stateNames2Pos = stateNames2Pos #dictionary of keys (state names) to values (state indices in state vector) 
        self.__integratorType = integratorType
        self.__numStates = len(self.__statePos2Names)
        self.__numCntrl = -1

    def __str__(self) -> str:
        msgStr = Time_Varying_Component.__str__(self)
        #msgStr = msgStr + Connect_Container_Component.__str__(self)
        msgStr = msgStr + f"\nIntegrator Type: {self.getIntegratorType()}"
        msgStr = msgStr + sim_utils.strStateNames(self.__statePos2Names)
        return msgStr

    @abstractmethod
    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        """Must Be Implemented at the subclass level"""
        pass
    
    def checkState(self, currState: np.array) -> None:
        if currState.size != self.__numStates:
            errorMsg = f"Error: Number of States Initialized: [{self.__numStates}]\n"
            errorMsg += f"Error: Number of States Declared:  [{currState.size}]"
            print(errorMsg) #add indices type, also add to logger
            exit(1)

    def checkCntrl(self, currCntrl: np.array) -> None:
        if self.__numCntrl == -1:
            self.__numCntrl = currCntrl.size #initialize on first pass 
            return
        if currCntrl.size != self.__numCntrl:
            errorMsg = f"Error: Number of Cntrls Initialized: [{self.__numCntrl}]\n"
            errorMsg += f"Error: Number of Cntrls Declared:  [{currCntrl.size}]"
            print(errorMsg) #add indices type, also add to logger
            exit(1)

    def setCurrState(self, currState: np.array) -> None:
        self.checkState(currState)
        self.currState = currState

    def getCurrState(self) -> np.array:
        return self.currState
    
    def setCurrCntrl(self, currCntrl: np.array) -> None:
        self.checkCntrl(currCntrl)
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
        elif isinstance(indices, np.array): 
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
    
    def printStates(self) -> str:
        pass
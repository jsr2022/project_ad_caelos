#truth_component.py

#from python base package(s)
from sys import exit as sys_exit
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.utilities.sim_utils import Sim_Utils
from adcaelos.components.time_varying_component import Time_Varying_Component

from adcaelos.components.component_enums import Component_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

# from adcaelos integrator classes
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.integrators.integrator_factory import IntegratorFactory

class Truth_Component(Time_Varying_Component, ABC):
    #NEED TO MAKE CHANGES
    #1) Separate states into states that get integrated, just get updated at each time step, 
    def __init__(self, stateNames: list, initial_state: np.array = None, initial_control: np.array = None, integratorType: Integrator_Enums = Integrator_Enums.RK4, frequency: int = 100, nextTime: float = 0, Component_Enum = Component_Enums.TRUTH_COMPONENT, name: str = "Truth_Component", UUID: int = None) -> None:
        Time_Varying_Component.__init__(self, frequency, nextTime, Scheduler_Priority_Enums.TRUTH, Component_Enum, name, UUID) 
        statePos2Names = Sim_Utils.checkUniqueStateNames(stateNames) #will call
        stateNames2Pos = Sim_Utils.convertDictionaryIndex2State(statePos2Names)

        #check to make sure number of states with names agrees with number of initial states
        if initial_state.size != len(statePos2Names):
            errorMsg = f"Number of initial state conditions: {initial_state.size}\
                        is different than the number of states with names: {len(statePos2Names)}"
            print(errorMsg)
            sys_exit(1)

        self.__statePos2Names = statePos2Names #dictionary of keys (state indices in state vector) to values (state names) 
        self.__stateNames2Pos = stateNames2Pos #dictionary of keys (state names) to values (state indices in state vector) 
        self.__integratorType = integratorType
        self.__numStates = initial_state.size
        self.__numCntrl = initial_control.size
        self.__currState = initial_state
        self.__currCntrl = initial_control
        # Create/get the integrator instance for this component
        self.integrator = IntegratorFactory.create(self.__integratorType)

    def __str__(self) -> str:
        msgStr = Time_Varying_Component.__str__(self)
        msgStr = msgStr + f"\nIntegrator Type: {self.getIntegratorType()}"
        msgStr = msgStr + Sim_Utils.strStateNames(self.__statePos2Names)\
                        + f"\nCurrent State:\n{self.getCurrState()}"\
                        + f"\nCurrent Control:\n{self.getCurrCntrl()}"
        return msgStr

    @abstractmethod
    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        """Returns the time derivative of the state vector (stateDot)
        requires: the current state, control, and time.
        This will be integrated by the RKX integrator
        Must Be Implemented at the subclass level"""
        

    @abstractmethod
    def calculateOtherStates(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        """
        This calculates any states that are not integrated but still need to be updated at each time step
        Must Be Implemented at the subclass level"""
    
    def checkState(self, currState: np.array) -> None:
        if currState.size != self.__numStates:
            errorMsg = f"Error: Number of States Initialized: [{self.__numStates}]\n"
            errorMsg += f"Error: Number of States Declared:  [{currState.size}]"
            print(errorMsg) #add indices type, also add to logger
            sys_exit(1)

    def checkCntrl(self, currCntrl: np.array) -> None:
        if self.__numCntrl == -1:
            self.__numCntrl = currCntrl.size #initialize on first pass 
            return
        if currCntrl.size != self.__numCntrl:
            errorMsg = f"Error: Number of Cntrls Initialized: [{self.__numCntrl}]\n"
            errorMsg += f"Error: Number of Cntrls Declared:  [{currCntrl.size}]"
            print(errorMsg) #add indices type, also add to logger
            sys_exit(1)

    def setCurrState(self, currState: np.array) -> None:
        self.checkState(currState)
        self.__currState = currState

    def getCurrState(self) -> np.array:
        if self.__currState is None:
            raise RuntimeError(f"Truth_Component '{self.getName()}' currState accessed before being set. Provide initial_state or call setCurrState().")
        return self.__currState
    
    def setCurrCntrl(self, currCntrl: np.array) -> None:
        self.checkCntrl(currCntrl)
        self.__currCntrl = currCntrl

    def getCurrCntrl(self) -> np.array:
        if self.__currCntrl is None:
            raise RuntimeError(f"Truth_Component '{self.getName()}' currCntrl accessed before being set. Provide initial_control or call setCurrCntrl().")
        return self.__currCntrl
        
    def getIntegratorType(self) -> Integrator_Enums:
        return self.__integratorType
    
    def getStatePos2Names(self, indices = None):
        if indices is None:
            return np.array(list(self.__statePos2Names.values()))
        elif isinstance(indices, int):
            if indices not in self.__statePos2Names:
                raise KeyError(f"indices {indices} not found in dictionary")
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
            sys_exit(1)

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
            sys_exit(1) 
    
    def act(self) -> None:
        """
        Integrates the truth state using the configured integrator.
        Called by the scheduler during event execution.
        """
        # Run the integrator to compute next state
        next_state = self.integrator.getNextState(
            fieldObject=self,
            currTime=self.getNextTime(),
            dt=self.getPeriod()
        )
        
        # Update the internal state
        self.setCurrState(next_state)
        
        # Calculate any non-integrated (derived) states
        self.calculateOtherStates(next_state, self.getCurrCntrl(), self.getNextTime())
        self.setNextTime()

    def getNumStates(self) -> int:
        return self.__numStates
    
    def getNumCntrl(self) -> int:
        return self.__numCntrl
    
    def print_states(self) -> str:
        pass
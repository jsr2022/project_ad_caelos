#truth_component.py # pylint: disable=missing-module-docstring

#from python base package(s)
from sys import exit as system_exit
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.utilities.sim_utils import Sim_Utils
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.data_storage import Data_Storage
#from adcaelos enums
from adcaelos.components.component_enums import Component_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

# from adcaelos integrator classes
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.integrators.integrator_factory import IntegratorFactory


class Truth_Component(Time_Varying_Component, ABC):
    #NEED TO MAKE CHANGES
    #1) Separate states into states that get integrated, just get updated at each time step, 
    def __init__(self,
                initial_state: np.array,
                state_names: str | list[str] = None,
                initial_control: np.array = None,
                control_names: str | list[str] = None,
                initial_other_states: np.array = None,
                other_states_names: str | list[str] = None,
                integrator_type: Integrator_Enums = Integrator_Enums.RK4,
                frequency: int = 100,
                next_time: float = 0,
                num_stored_steps: int = 100,
                Component_Enum = Component_Enums.TRUTH_COMPONENT,
                name: str = "Truth_Component",
                UUID: int = None) -> None:
        Time_Varying_Component.__init__(self,
                                        frequency,
                                        next_time,
                                        Scheduler_Priority_Enums.TRUTH,
                                        Component_Enum,
                                        name,
                                        UUID)
        
        self.__integrator_type = integrator_type
        self.__num_states = initial_state.size
        self.__current_state = initial_state
        # Default Behavior is no other states and no control
        self.__valid_other_states = False
        self.__valid_control = False
        self.__num_control = -1
        self.__current_control = 0
        self.__num_other_states = -1
        self.__other_states = 0

        # Create/get the integrator instance for this component
        self.integrator = IntegratorFactory.create(self.__integrator_type)

        #Checking State Names
        state_names = Sim_Utils.check_state_names(self.__num_states, state_names)
        #Creating Data Storage For Truth State Data
        self.state_data = Data_Storage(variable_names=state_names, initial_values=initial_state, next_time=next_time, num_stored_steps=num_stored_steps, name="truth_state_data")
        
        #If I have a Control, Check Control Names and Create Data Storage for Control Data
        if initial_control is not None:
            self.__valid_control = True
            self.__num_control = initial_control.size
            self.__current_control = initial_control
            control_names = Sim_Utils.check_state_names(self.__num_control, control_names)
            self.control_data = Data_Storage(variable_names=control_names, initial_values=initial_control, next_time=next_time, num_stored_steps=num_stored_steps, name="control_data")

        #If I have other states, check other state names and create data storage for other states
        if initial_other_states is not None:
            self.__valid_other_states = True
            self.__num_other_states = initial_other_states.size
            self.__other_states = initial_other_states
            other_states_names = Sim_Utils.check_state_names(self.__num_other_states, other_states_names)
            self.other_state_data = Data_Storage(variable_names=other_states_names, initial_values=initial_other_states, next_time=next_time, num_stored_steps=num_stored_steps, name="truth_other_state_data")


    def __str__(self) -> str:
        msg_str = Time_Varying_Component.__str__(self)
        msg_str = msg_str + f"\nIntegrator Type: {self.getIntegratorType()}"
        msg_str = msg_str + Sim_Utils.state_names_string(self.state_data.get_variable_names_2_position())\
                        + f"\nCurrent State:\n{self.getCurrState()}"
        if self.__valid_control:
            msg_str = msg_str + f"\nCurrent Control:\n{self.getCurrCntrl()}"
        if self.__valid_other_states:
            msg_str = msg_str + f"\nOther States:\n{self.get_other_states()}"

        return msg_str

    @abstractmethod
    def statesDot(self, current_state: np.array, current_control: np.array, current_time: float) -> np.array:
        """Returns the time derivative of the state vector (stateDot)
        requires: the current state, control, and time.
        This will be integrated by the RKX integrator
        Must Be Implemented at the subclass level"""
        

    @abstractmethod
    def calculateOtherStates(self, current_state: np.array, current_control: np.array, current_time: float) -> np.array:
        """
        This calculates any states that are not integrated but still need to be updated at each time step
        Must Be Implemented at the subclass level"""
    
    def checkState(self, current_state: np.array) -> None:
        if current_state.size != self.__num_states:
            error_message = f"Error: Number of States Initialized: [{self.__num_states}]\n"
            error_message += f"Error: Number of States Declared:  [{current_state.size}]"
            print(error_message) #add indices type, also add to logger
            system_exit(1)

    def checkCntrl(self, current_control: np.array) -> None:
        if current_control.size != self.__num_control:
            error_message = f"Error: Number of Controls Initialized: [{self.__num_control}]\n"
            error_message += f"Error: Number of Controls Declared:  [{current_control.size}]"
            print(error_message) # TODO add indices type, also add to logger
            system_exit(1)

    def checkOtherStates(self, other_states: np.array) -> None:
        if other_states.size != self.__num_other_states:
            error_message = f"Error: Number of Other States Initialized: [{self.__num_other_states}]\n"
            error_message += f"Error: Number of Other States Declared:  [{other_states.size}]"
            print(error_message) # TODO add indices type, also add to logger
            system_exit(1)

    def setCurrState(self, current_state: np.array) -> None:
        self.checkState(current_state)
        self.__current_state = current_state

    def getCurrState(self) -> np.array:
        return self.__current_state
    
    def setCurrCntrl(self, current_control: np.array) -> None:
        self.checkCntrl(current_control)
        self.__current_control = current_control

    def getCurrCntrl(self) -> np.array:
        if not self.__valid_control:
            raise RuntimeError(f"Truth_Component '{self.get_name()}' control has not been enabled")
        return self.__current_control
    
    def set_other_states(self, other_states: np.array) -> None:
        self.__other_states = other_states

    def get_other_states(self) -> np.array:
        if not self.__valid_other_states:
            raise RuntimeError(f"Truth_Component '{self.get_name()}' other_states has not been enabled")
        return self.__other_states

    def getIntegratorType(self) -> Integrator_Enums:
        return self.__integrator_type
    
    def act(self) -> None:
        """
        Integrates the truth state using the configured integrator.
        Called by the scheduler during event execution.
        """
        # Run the integrator to compute next state
        state = self.integrator.getNextState(
            fieldObject=self,
            current_time=self.get_time(),
            dt=self.get_period()
        )
        
        # Update the internal state
        self.setCurrState(state)
        
        # Calculate any non-integrated (derived) states
        if self.__valid_other_states:
            other_states = self.calculateOtherStates(state, self.getCurrCntrl(), self.get_time())
            self.set_other_states(other_states)

        self.store_states()
        #Set time for next action
        self.set_next_time()


    def store_states(self) -> None:
        """Stores current state control, and if enabled, other states in the respective data storage components.
        Called at the end of the act method to store data after state has been updated and other states have been calculated."""
        #TODO Review Method to see if this is still the best practice
        self.state_data.store_data(self.get_time(), self.getCurrState())
        if self.__valid_control:
            self.control_data.store_data(self.get_time(), self.getCurrCntrl())
    
        if self.__valid_other_states:
            self.other_state_data.store_data(self.get_time(), self.get_other_states())

    def getNumStates(self) -> int:
        return self.__num_states
    
    def getNumCntrl(self) -> int:
        return self.__num_control
    
    def getNumOtherStates(self) -> int:
        if not self.__valid_other_states:
            raise RuntimeError(f"Truth_Component '{self.get_name()}' other_states has not been enabled")
        return self.__num_other_states
    
    def print_states(self) -> str:
        #TODO implement method to print current state, control, and other states in a nice format
        pass
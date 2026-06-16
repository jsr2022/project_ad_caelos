#sim_utils.py

#from python base package(s)
from sys import exit as system_exit
import logging

#Import External Python Packages


class Sim_Utils:

    @staticmethod
    def get_logging_object() -> logging.Logger:
        """
        _Creates a logging object for use throughout the simulation._

        Returns
        -------
        logging.Logger
            _a logging object for use in the simulation_
        """
        logger = logging.getLogger("Adcaelos Simulation Logger")
        # logger.setLevel(logging.DEBUG)
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # ch.setFormatter(formatter)
        # logger.addHandler(ch)
        return logger
    


    @staticmethod
    def checkUniqueStateNames(state_names:list[str]) -> list[str]:
        """
        _Ensures that each state name is unique and errors if they are not unique_

        Parameters
        ----------
        state_names : list[str]
            _a list of state names_

        Returns
        -------
        list[str]
            _a list of unique state names that are all lower case_
        """
        state_names = [item.lower() for item in state_names]
        uniqueStateNames = list(set(state_names))
        if len(state_names) == len(uniqueStateNames):
            return uniqueStateNames
        else:
            print("Error: State Names are not Unique!")
            print(Sim_Utils.state_names_string(Sim_Utils.generateDictionaryIndex2State(state_names)))
            system_exit(1)
    
    @staticmethod
    def check_state_names(num_states:int, state_names:list[str] = None, abbreviation: str = None) -> dict:
        """
        _Checks to see if the user has provided state names and ensure that they are unique, number matches number of states, 
        and creates a dictionary mapping state indices to state names. If not, creates generic state names in the format s1, s2, etc. 
        based on the number of states._
        
        
        Parameters
        ----------
        num_states : int
            _the number of states for which to create names if state_names is None_
        state_names : list[str], optional
            _a list of state names, by default None_

        Returns
        -------
        dict
            _a dictionary mapping state indices (integers) to state names (strings)_
        """
        if state_names is None:
            state_names = Sim_Utils.create_state_names(num_states)
            state_names = Sim_Utils.checkUniqueStateNames(state_names)

        elif isinstance(state_names, str):
            state_names = [state_names]
            state_names = Sim_Utils.checkUniqueStateNames(state_names)

        elif len(state_names) != num_states:
            error_message = f"Number of state names provided: {len(state_names)} is different than the number of states: {num_states}"
            Sim_Utils.get_logging_object().error(error_message)
            system_exit(1)
        else:
            state_names = Sim_Utils.checkUniqueStateNames(state_names)
        
        return state_names

    @staticmethod
    def create_state_names(num_states: int, abbreviation: str = None) -> list[str]:
        """
        _Creates generic state names in the format s1, s2, etc. based on the number of states._

        Parameters
        ----------
        num_states : int
            _the number of states for which to create names_

        Returns
        -------
        list[str]
            _a list of generic state names_
        """
        if abbreviation is None:
            state_names = [f"s{i+1}" for i in range(num_states)]
        else:
            state_names = [f"{abbreviation}_{i+1}" for i in range(num_states)]
        return state_names


    @staticmethod
    def generateDictionaryIndex2State(state_names:list) -> dict:
        """_Generates a dictionary mapping state indices to state names.
        The key is the number and the value is the state name. 
        Keys are indexed at one as time is always the first 'hidden' state._"""
        statePos2Names = dict(list(enumerate(state_names, start=1)))
        return statePos2Names
    
    @staticmethod
    def convertDictionaryIndex2State(statePos2Names:dict) -> dict:
        """_Converts a dictionary mapping state indices to 
        state names to a dictionary mapping state names to state indices.
        The key is the state name and the value is the number. 
        values are indexed at one as time is always the first 'hidden' state._"""
        state_names_2_pos = {v: k for k, v in statePos2Names.items()}
        return state_names_2_pos

    @staticmethod
    def state_names_string(state_names:dict) -> str:
        """
        _creates a pretty type face describing each state and its name to be used in print commands_

        Parameters
        ----------
        state_names : dict
            _a dictionary mapping state indices (integers) to state names (strings)_

        Returns
        -------
        str
            _a formatted printing out each index and its state name on a separate line_
        """
        try: 
            aKey = list(state_names)[0]
        except IndexError:
            print("Need at least one key-value pair entered in the dictionary")
            print(f"State Names: {state_names}")
            system_exit(1)

        if not isinstance(aKey, int):
            state_names = Sim_Utils.convertDictionaryIndex2State(state_names)

        max_key_length = max(len(str(key)) for key in state_names)
        output_lines = []
        for key, value in state_names.items():
            output_lines.append("\nState Number: {:<{width}} State Name: {}".format(str(key), value, width=max_key_length))
        output = "".join(output_lines)
        return output
#sim_utils.py

#from python base package(s)
from sys import exit as sys_exit

#Import External Python Packages
import numpy as np

class Sim_Utils:
    @staticmethod
    def checkUniqueStateNames(stateNames:list) -> list[str]:
        stateNames = [item.lower() for item in stateNames]
        uniqueStateNames = list(set(stateNames))
        if len(stateNames) == len(uniqueStateNames):
            return uniqueStateNames
        else:
            print("Error: State Names are not Unique!")
            print(Sim_Utils.strStateNames(Sim_Utils.generateDictionaryIndex2State(stateNames)))
            sys_exit(1)
            

    @staticmethod
    def generateDictionaryIndex2State(stateNames:list) -> dict:
        """_Generates a dictionary mapping state indices to state names.
        The key is the number and the value is the state name. 
        Keys are indexed at one as time is always the first 'hidden' state._"""
        statePos2Names = dict(list(enumerate(stateNames, start=1)))
        return statePos2Names
    
    @staticmethod
    def convertDictionaryIndex2State(statePos2Names:dict) -> dict:
        """_Converts a dictionary mapping state indices to 
        state names to a dictionary mapping state names to state indices.
        The key is the state name and the value is the number. 
        Keys are indexed at one as time is always the first 'hidden' state._"""
        stateNames2Pos = {v: k for k, v in statePos2Names.items()}
        return stateNames2Pos

    @staticmethod
    def strStateNames(stateNames:dict) -> str:
        try: 
            aKey = list(stateNames)[0]
        except IndexError:
            print("Need at least one key-value pair entered in the dictionary")
            print(f"stateNames: {stateNames}")
            sys_exit(1)

        if not isinstance(aKey, int):
            stateNames = Sim_Utils.convertDictionaryIndex2State(stateNames)

        max_key_length = max(len(str(key)) for key in stateNames)
        output_lines = []
        for key, value in stateNames.items():
            output_lines.append("\nState Number: {:<{width}} State Name: {}".format(str(key), value, width=max_key_length))
        output = "".join(output_lines)
        return output
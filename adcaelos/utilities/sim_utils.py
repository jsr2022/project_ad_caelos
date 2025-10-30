#sim_utils.py

#from python base package(s)
from sys import exit

#Import External Python Packages
import numpy as np

class Sim_Utils:
    @staticmethod
    def checkUniqueStateNames(stateNames:list) -> None:
        stateNames = [item.lower() for item in stateNames]
        uniqueStateNames = set(stateNames)
        if len(stateNames) == len(uniqueStateNames):
            return Sim_Utils.generateDictionaryIndex2State(stateNames)
        else:
            print("Error: State Names are not Unique!")
            print(Sim_Utils.strStateNames(Sim_Utils.generateDictionaryIndex2State(stateNames)))
            exit(1)
            

    @staticmethod
    def generateDictionaryIndex2State(stateNames:list) -> dict:
        statePos2Names = dict(list(enumerate(stateNames)))
        return statePos2Names
    
    @staticmethod
    def convertDictionaryIndex2State(statePos2Names:dict) -> dict:
        stateNames2Pos = {v: k for k, v in statePos2Names.items()}
        return stateNames2Pos

    @staticmethod
    def strStateNames(stateNames:dict) -> str:
        try: 
            aKey = list(stateNames)[0]
        except IndexError:
            print("Need at least one key-value pair entered in the dictionary")
            print(f"stateNames: {stateNames}")
            exit(1)

        if not isinstance(aKey, int):
            stateNames = Sim_Utils.convertDictionaryIndex2State(stateNames)

        max_key_length = max(len(str(key)) for key in stateNames)
        output_lines = []
        for key, value in stateNames.items():
            output_lines.append("\nState Number: {:<{width}} State Name: {}".format(str(key), value, width=max_key_length))
        output = "".join(output_lines)
        return output
    
    ##-------------UNIT-CONVERSIONS-------------
    @staticmethod
    def in2cm() -> float:
        """Inch to Centimeter"""
        return 2.54
    
    @staticmethod
    def cm2in() -> float:
        """Centimeter to Inch"""
        return 1/Sim_Utils.in2cm()

    @staticmethod
    def ft2m() -> float:
        """Feet to Meter"""
        return 0.3048
    
    @staticmethod
    def m2ft() -> float:
        """Meter to Feet"""
        return 1/Sim_Utils.ft2m()
    
    @staticmethod
    def kg2lb() -> float:
        """Kilogram to Pound Mass"""
        return 2.214 #CHECK ME
    
    @staticmethod
    def lb2kg() -> float:
        """Pound Mass to Kilogram"""
        return 1/Sim_Utils.kg2lb()

    @staticmethod
    def nm2km() -> float:
        """Nautical Mile to Kilometer"""
        return 1.852
    
    @staticmethod
    def mi2km() -> float:
        """Mile to Kilometer"""
        return 5280*Sim_Utils.ft2m()/1000
    
    @staticmethod
    def km2mi() -> float:
        """Kilometer to Mile"""
        return 1/Sim_Utils.mi2km()
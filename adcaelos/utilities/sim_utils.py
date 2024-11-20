#sim_utils.py

#from python base package(s)
from sys import exit

#Import External Python Packages
import numpy as np

def checkUniqueStateNames(stateNames:list) -> None:
    stateNames = [item.lower() for item in stateNames]
    uniqueStateNames = set(stateNames)
    if len(stateNames) == len(uniqueStateNames):
        return generateDictionaryIndex2State(stateNames)
    else:
        print("Error: State Names are not Unique!")
        print(strStateNames(generateDictionaryIndex2State(stateNames)))
        exit(1)
        return dict()

def generateDictionaryIndex2State(stateNames:list) -> dict:
    statePos2Names = dict(list(enumerate(stateNames)))
    return statePos2Names
    
def convertDictionaryIndex2State(statePos2Names:dict) -> dict:
    stateNames2Pos = {v: k for k, v in statePos2Names.items()}
    return stateNames2Pos

def strStateNames(stateNames:dict) -> str:
    aKey = list(stateNames)[0]
    if type(aKey) is not int:
        stateNames = convertDictionaryIndex2State(stateNames)

    max_key_length = max(len(str(key)) for key in stateNames)
    output_lines = []
    for key, value in stateNames.items():
        output_lines.append("\nState Number: {:<{width}} State Name: {}".format(str(key), value, width=max_key_length))
    output = "".join(output_lines)
    return output
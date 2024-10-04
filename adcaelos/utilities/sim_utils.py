#sim_utils.py

def convertDictionaryIndex2State(statePos2Names:dict) -> dict:
    stateNames2Pos = {v: k for k, v in statePos2Names.items()}
    return stateNames2Pos
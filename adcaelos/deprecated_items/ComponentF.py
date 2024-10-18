import numpy as np

class Component:
    
    def __init__(self, UUID: int, numCntrl: int, initialCond: np.array) -> None:
        self.UUID      = UUID
        self.currState = initialCond
        self.numCntrl  = numCntrl
        self.currCntrl  = np.zeros(self.numCntrl)
        

    def getStatesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        """Returns the Vector Field of the System.
        Type: np.array """
        rho = 28
        beta = 8/3
        sigma = 10
        dx_dt = sigma*(currState[1] - currState[0])
        dy_dt = currState[0]*(rho - currState[2]) - currState[1]
        dz_dt = currState[0]*currState[1] - beta*currState[2]
        statesDot = np.array([dx_dt, dy_dt, dz_dt])
        return statesDot
    
    def setCurrState(self, currState):
        self.currState = currState

    def getCurrState(self) -> np.array:
        return self.currState
    
    def setCurrCntrl(self, currCntrl):
        self.currCntrl = currCntrl

    def getCurrCntrl(self) -> np.array:
        return self.currCntrl

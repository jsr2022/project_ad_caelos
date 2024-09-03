import numpy as np

class Component:
    
    def __init__(self, UUID: int, hasControl: bool = False):
        self.UUID = UUID

    def getStatesDot(self, currState: np.array, currTime: float) -> np.array:
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
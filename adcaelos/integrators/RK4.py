#RK4.py

import numpy as np
from integrators.IntegratorMetaInterface import IntegratorMetaInterface
from component.Component import Component
class RK4(IntegratorMetaInterface):
    
    type = "RK4"

    def __init__(self) -> None:
        pass


def nextState(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    """Returns the Next State in the Time Series.
    Type: np.array"""
    pass

def f2(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    #todo add RK4 f2 steps
    pass

def f3(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    #todo add RK4 f3 steps
    pass

def f4(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    #todo add RK4 f4 steps
    pass

def getIntegratorName() -> str:
    return type










#RK4.py

import numpy as np
from integrators.IntegratorMetaInterface import IntegratorMetaInterface
from component.Component import Component
class RK4(IntegratorMetaInterface):
    
    type = "RK4"

    def __init__(self) -> None:
        self.name = "Runge Kutta 4 Integrator"


def getNextState(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    """Returns the Next State in the Time Series.
    Type: np.array"""
    ff1 = fieldObject.getStatesDot(currState, currState)
    ff2 = self.f2(fieldObject, currState, currTime, dt)
    ff3 = self.f3(fieldObject, currState, currTime, dt)
    ff4 = self.f4(fieldObject, currState, currTime, dt)
    nextState = currState + dt/6*(ff1 + 2*ff2 + 2*ff3 + ff4)
    return nextState
    

def f2(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    """Returns f2 Runge Kutta Approximation
    Type: np.array"""
    ff2 = fieldObject.getStatesDot(currState + dt/2*fieldObject.getStatesDot(currState, currTime), currTime + dt/2)
    return ff2

def f3(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    """Returns f3 Runge Kutta Approximation
    Type: np.array"""
    ff3 = fieldObject.getStatesDot(currState + dt/2*self.f2(fieldObject, currState, currTime, dt), currTime + dt/2)
    return ff3
    
def f4(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
    """Returns f4 Runge Kutta Approximation
    Type: np.array"""
    ff4 = fieldObject.getStatesDot(currState + dt*self.f3(fieldObject, currState, currTime, dt), currTime + dt)
    return ff4

def getIntegratorName() -> str:
    return type










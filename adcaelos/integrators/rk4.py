# rk4.py # pylint: disable=missing-module-docstring
# Default Imports
from typing import TYPE_CHECKING

# Third Party Imports
import numpy as np

# Adcaelos Imports
from adcaelos.integrators.integrator_meta_interface import Integrator_Meta_Interface

if TYPE_CHECKING:
    from adcaelos.components.truth_component import Truth_Component



class RK4(Integrator_Meta_Interface):
    """
    _Runge-Kutta 4th Level Integration Class_

    Parameters
    ----------
    Integrator_Meta_Interface : 
        _a default interface for all integrators in Adcaelos_

    Returns
    -------
    _type_
        _The type of integrator (RK4_
    """
    type = "RK4"

    def __init__(self) -> None:
        self.name = "Runge Kutta 4 Integrator"

    def getNextState(self, fieldObject: "Truth_Component", currTime: float, dt: float) -> np.array:
        """Returns the next state in the time series"""
        currState = fieldObject.getCurrState()
        currCntrl = fieldObject.getCurrCntrl()
        ff1 = fieldObject.statesDot(currState, currCntrl, currTime)
        ff2 = self.f2(fieldObject, currTime, dt)
        ff3 = self.f3(fieldObject, currTime, dt)
        ff4 = self.f4(fieldObject, currTime, dt)
        nextState = currState + dt/6*(ff1 + 2*ff2 + 2*ff3 + ff4)
        return nextState
    
    def f2(self, fieldObject: "Truth_Component", currTime: float, dt: float) -> np.array:
        """Returns f2 Runge Kutta Approximation"""
        currState = fieldObject.getCurrState()
        currCntrl = fieldObject.getCurrCntrl()
        ff2 = fieldObject.statesDot(currState + dt/2*fieldObject.statesDot(currState, currCntrl, currTime), currCntrl, currTime + dt/2)
        return ff2

    def f3(self, fieldObject: "Truth_Component", currTime: float, dt: float) -> np.array:
        """Returns f3 Runge Kutta Approximation"""
        currState = fieldObject.getCurrState()
        currCntrl = fieldObject.getCurrCntrl()
        ff3 = fieldObject.statesDot(currState + dt/2*self.f2(fieldObject, currTime, dt), currCntrl, currTime + dt/2)
        return ff3
    
    def f4(self, fieldObject: "Truth_Component", currTime: float, dt: float) -> np.array:
        """Returns f4 Runge Kutta Approximation"""
        currState = fieldObject.getCurrState()
        currCntrl = fieldObject.getCurrCntrl()
        ff4 = fieldObject.statesDot(currState + dt*self.f3(fieldObject, currTime, dt), currCntrl, currTime + dt)
        return ff4

    @classmethod
    def getIntegratorName(cls) -> str:
        return cls.type








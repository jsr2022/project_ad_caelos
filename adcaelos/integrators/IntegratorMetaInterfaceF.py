#IntegratorMetaInterface.py

import abc
import numpy as np
from component.Component import Component


class IntegratorMetaInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        return (hasattr(subclass, 'getNextState') and
                callable(subclass.getNextState) and
                hasattr(subclass, 'getIntegratorName') and
                callable(subclass.getIntegratorName) or 
                NotImplemented)
    
    @abc.abstractmethod
    def getNextState(self, fieldObject: Component, currState: np.array, currTime: float, dt: float) -> np.array:
        """Returns the next state tied to the next time step
        Type: np.array"""
        raise NotImplementedError
    
    def getIntegratorName() -> str:
        """Returns the name of the integrator class
        Type: str """
        raise NotImplementedError
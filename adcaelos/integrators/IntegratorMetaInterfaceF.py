import abc
import numpy as np
from components.ComponentF import Component

class IntegratorMetaInterface(abc.ABC): #metaclass=abc.ABCMeta
    @abc.abstractmethod
    def getNextState(self, fieldObject: Component, currTime: float, dt: float) -> np.array:
        """Returns the next state tied to the next time step"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def getIntegratorName(self) -> str:
        """Returns the name of the integrator class"""
        raise NotImplementedError
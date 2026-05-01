import abc
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from adcaelos.components.truth_component import Truth_Component

class Integrator_Meta_Interface(abc.ABC): #metaclass=abc.ABCMeta
    @abc.abstractmethod
    def getNextState(self, fieldObject: "Truth_Component", currTime: float, dt: float) -> np.array:
        """Returns the next state tied to the next time step"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def getIntegratorName(self) -> str:
        """Returns the name of the integrator class"""
        raise NotImplementedError
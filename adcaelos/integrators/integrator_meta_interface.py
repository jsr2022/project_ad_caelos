# Generic Python Imports
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Package Imports
import numpy as np

# Adcaelos Imports
if TYPE_CHECKING:
    from adcaelos.components.truth_component import Truth_Component

class Integrator_Meta_Interface(ABC): #metaclass=abc.ABCMeta
    @abstractmethod
    def getNextState(self, fieldObject: "Truth_Component", currTime: float, dt: float) -> np.array:
        """Returns the next state tied to the next time step"""
        raise NotImplementedError
    
    @abstractmethod
    def getIntegratorName(self) -> str:
        """Returns the name of the integrator class"""
        raise NotImplementedError
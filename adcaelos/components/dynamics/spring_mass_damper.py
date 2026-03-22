# spring_mass_damper.py

# from python base package(s)
from sys import exit
from abc import ABC, abstractmethod

# from other package(s)
import numpy as np

# from adcaelos package(s)
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums

# utilities
from adcaelos.utilities.sim_utils import Sim_Utils
from adcaelos.atmosphere.atmosphere_models import Atmosphere_Models


class SpringMassDamper(Truth_Component):
    """
    Spring Mass Damper Class - Example Truth Component for a simple 1D spring mass damper system
    inputs: spring constant [kg*m/s^2] equivalently [N/m], damping constant [kg*m/s] equivalently [N*s/m], mass [kg]
    states: position [m], velocity [m/s]
    Args:
        Truth_Component (_type_): _description_
    """

    def __init__(self, stateNames: list, integratorType: Integrator_Enums = Integrator_Enums.RK4, frequency: int = 100, nextTime: float = 0, Component_Enum=Component_Enums.TRUTH_COMPONENT, name: str = "Spring_Mass_Damper", UUID: int = None,
                mass: float = 1.0, spring_constant: float = 1.0, damping_constant: float = 1.0) -> None:
        super().__init__(stateNames, integratorType, frequency, nextTime, Component_Enum, name, UUID)
        self.mass = mass
        self.spring_constant = spring_constant
        self.damping_constant = damping_constant

    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + "\n--Spring Mass Damper Dynamics--"
        msgStr = msgStr + f"\nMass: {self.mass} [kg]"
        msgStr = msgStr + f"\nSpring Constant: {self.spring_constant} [N/m]"
        msgStr = msgStr + f"\nDamping Constant: {self.damping_constant} [N*s/m]"
        return msgStr
    
    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        """
        Returns the time derivative of the state vector (stateDot)
        requires: the current state, control, and time.
        This will be integrated by the RKX integrator
        """
        super().checkState(currState) #I want to know immediately if there is an error
        super().checkCntrl(currCntrl)
        # Unpack states and controls
        position = currState[0]  # [m]
        velocity = currState[1]  # [m/s]
        
        position_dot = velocity
        velocity_dot = -self.damping_constant/self.mass * velocity - self.spring_constant/self.mass * position + currCntrl/self.mass  # [m/s^2], where currCntrl[0] is the external force applied to the mass [N]

        # Return state derivatives as a numpy array
        return np.array([position_dot, velocity_dot]).T  # [m/s, m/s^2]
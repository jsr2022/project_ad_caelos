# spring_mass_damper.py # pylint: disable=missing-module-docstring

# from python base package(s)
# from sys import exit as system_exit

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
    inputs: spring constant [kg*m/s^2] or [N/m], damping constant [kg*m/s] or [N*s/m], mass [kg]
    states: position [m], velocity [m/s]
    Args:
        Truth_Component (_type_): _description_
    """

    def __init__(self, stateNames: list, initial_state: np.array = np.zeros(2), initial_control: np.array = np.zeros(1), integrator_type: Integrator_Enums = Integrator_Enums.RK4, frequency: int = 100, next_time: float = 0, Component_Enum=Component_Enums.TRUTH_COMPONENT, name: str = "Spring_Mass_Damper", UUID: int = None,
                mass: float = 1.0, spring_constant: float = 1.0, damping_constant: float = 1.0) -> None:

        super().__init__(state_names=stateNames,
                        initial_state=initial_state,
                        control_names="external_force",
                        initial_control=initial_control,
                        integrator_type=integrator_type,
                        frequency=frequency,
                        next_time=next_time,
                        Component_Enum=Component_Enum,
                        name=name,
                        UUID=UUID)
        self.mass = mass
        self.spring_constant = spring_constant
        self.damping_constant = damping_constant

    def __str__(self) -> str:
        message_string = super().__str__()
        message_string = message_string + "\n--Spring Mass Damper Dynamics--"
        message_string = message_string + f"\nMass: {self.mass} [kg]"
        message_string = message_string + \
            f"\nSpring Constant: {self.spring_constant} [N/m]"
        message_string = message_string + \
            f"\nDamping Constant: {self.damping_constant} [N*s/m]"
        return message_string

    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        """
        Returns the time derivative of the state vector (stateDot)
        requires: the current state, control, and time.
        This will be integrated by the RKX integrator
        """
        super().checkState(currState)  # I want to know immediately if there is an error
        super().checkCntrl(currCntrl)
        # Unpack states and controls
        position = currState[0]  # [m]
        velocity = currState[1]  # [m/s]

        position_dot = velocity
        velocity_dot = -self.damping_constant/self.mass * velocity - self.spring_constant/self.mass * position + \
            currCntrl[0]/self.mass  # [m/s^2], where currCntrl[0] is the external force applied to the mass [N]

        # Return state derivatives as a numpy array
        return np.array([position_dot, velocity_dot])  # [m/s, m/s^2]

    def calculateOtherStates(self, currState: np.array, currCntrl: np.array, currTime: float) -> None:
        """
        This calculates any states that are not integrated but still need to be updated at each time step
        For this simple spring mass damper system, there are no additional states to calculate, so this function does nothing.
        """
        pass

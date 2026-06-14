# logic_component.py

# from python base package(s)
from abc import ABC, abstractmethod

# from other package(s)
import numpy as np

# from adcaelos package(s)
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums


class Logic_Component(Time_Varying_Component, ABC):
    """
    Abstract base class for control logic (guidance, navigation, control, etc.)

    Operates on Option B (buffered control):
    - Reads current/last truth state at each execution
    - Computes control inputs
    - Buffers control inputs for truth component to use
    - Next execution reads updated truth state reflecting previous control

    Can have multiple instances per vehicle at different frequencies.
    Example: FlightComputer oversees Control (50Hz), Navigation (20Hz), Guidance (5Hz)
    """

    def __init__(self, frequency: int = 50, next_time: float = 0,
                scheduler_priority_enum: Scheduler_Priority_Enums = Scheduler_Priority_Enums.CONTROL,
                name: str = "Logic_Component", UUID: int = None) -> None:
        """
        Initialize Logic Component

        Args:
            frequency: Execution frequency in Hz (default 50 Hz for control loop)
            next_time: Next scheduled execution time
            scheduler_priority_enum: Priority for scheduling conflicts
            name: Component name
            UUID: Unique identifier
        """
        Time_Varying_Component.__init__(
            self, frequency, next_time, scheduler_priority_enum,
            Component_Enums.LOGIC_COMPONENT, name, UUID
        )

    def __str__(self) -> str:
        message_string = Time_Varying_Component.__str__(self)
        return message_string

    def act(self) -> None:
        self.subsystemMethod()
        self.set_next_time()

    # @abstractmethod
    def logicCenter(self, currState: np.array) -> np.array:
        """
        Compute control law (autonomy, guidance, navigation, control)

        Called at this component's frequency. Must be implemented by subclasses.

        Args:
            currState: Current truth state from Truth_Component (numpy array)

        Returns:
            control: Control input vector (numpy array) to be applied by Truth_Component
                    This control will be used until the next call to logicCenter()
        """
        control_size = currState.size
        return np.zeros(1)

    def subsystemMethod(self) -> None:
        """
        Called by scheduler at this component's frequency (Option B buffered control)

        1. Reads current truth state from container
        2. Calls logicCenter() to compute control
        3. Buffers control for truth component to use in next integration step(s)
        """
        # Get truth component from container
        container = self.getContainerComponent()
        if container is None:
            raise RuntimeError(
                f"Logic_Component '{self.get_name()}' not connected to container")

        truth_component = container.getTC()
        if truth_component is None:
            raise RuntimeError(
                f"Logic_Component '{self.get_name()}' container has no Truth_Component")

        # Read current truth state
        currState = truth_component.getCurrState()

        # Compute control law
        control = self.logicCenter(currState)

        # Buffer control for truth component to use in next integration(s)
        truth_component.setCurrCntrl(control)

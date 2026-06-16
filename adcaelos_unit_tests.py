# adcaelos_unit_tests.py
"""
Unit tests for the ADCAELOS simulation framework.
This file provides a small regression test framework to verify core
behavior, especially time drift prevention in Time_Varying_Component.
"""
from __future__ import annotations

import sys
import unittest
import numpy as np

from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.base_component import Base_Component
from adcaelos.schedulers.scheduler import Scheduler
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums

# Additional imports
from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums
from adcaelos.components.logic_component import Logic_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.container_component import Container_Component


# Minimal concrete component for testing without abstract methods.
class DummyTVComponent(Time_Varying_Component):
    def __init__(self, frequency=100, next_time=0.0, name="DummyTV"):
        Base_Component.__init__(
            self, component_type=Component_Enums.TIME_VARYING_COMPONENT, name=name, UUID=None
        )
        self.next_time = float(next_time)
        self.__frequency = frequency
        self.__period = 1.0 / frequency
        self.__start_counter_time = self.next_time
        self.__step_count = 0
        self.__scheduler_priority_enum = Scheduler_Priority_Enums.LOWEST

    def act(self) -> None:
        pass

    def set_next_time(self, next_time=None, next_frequency=None) -> None:
        if next_time is None:
            self.__step_count += 1
            self.next_time = self.__start_counter_time + self.__step_count / self.__frequency
        elif next_time is not None and next_frequency is not None:
            self.__start_counter_time = float(next_time)
            self.__step_count = 0
            self.__frequency = next_frequency
            self.__period = 1.0 / next_frequency
            self.next_time = self.__start_counter_time
        else:
            raise ValueError(
                f"Invalid arguments for set_next_time: next_time={next_time}, "
                f"next_frequency={next_frequency}. Must provide either no arguments "
                "or both next_time and next_frequency."
            )

    def get_time(self) -> float:
        return self.next_time

    def get_frequency(self) -> int:
        return self.__frequency

    def get_period(self) -> float:
        return self.__period

    def getStepCount(self) -> int:
        return self.__step_count


class ConcreteTruth(Truth_Component):
    def statesDot(self, currState, currCntrl, currTime):
        return np.zeros_like(currState)
    def calculateOtherStates(self, currState, currCntrl, currTime):
        pass


class TestTimeDrift(unittest.TestCase):
    def test_no_drift_1m_steps_100hz(self):
        """
        Regression test: repeated set_next_time(None) should not accumulate drift.
        1,000,000 steps at 100 Hz should land exactly at 10,000.0 s (within 1e-9).
        """
        comp = DummyTVComponent(frequency=100, next_time=0.0)
        n = 1_000_000
        for _ in range(n):
            comp.set_next_time()
        final = comp.get_time()
        expected = 10_000.0
        self.assertLess(abs(final - expected), 1e-9,
                        f"Drift too large: {final} vs {expected} (diff={final-expected})")

    def test_reanchor_on_explicit_time(self):
        comp = DummyTVComponent(frequency=10, next_time=0.0)
        for _ in range(5):
            comp.set_next_time()
        self.assertAlmostEqual(comp.get_time(), 0.5)
        comp.set_next_time(100.0, 10)
        self.assertEqual(comp.get_time(), 100.0)
        self.assertEqual(comp.getStepCount(), 0)
        comp.set_next_time()
        self.assertAlmostEqual(comp.get_time(), 100.1)

    def test_set_frequency_reanchors(self):
        class ConcreteTV(Time_Varying_Component):
            def act(self) -> None:
                pass
        comp = ConcreteTV(frequency=10, next_time=0.0, name="Concrete",
                        Component_Enum=Component_Enums.TIME_VARYING_COMPONENT)
        for _ in range(5):
            comp.set_next_time()
        self.assertAlmostEqual(comp.get_time(), 0.5)
        comp.set_frequency(20)
        comp.set_next_time()
        self.assertAlmostEqual(comp.get_time(), 0.55)


class TestSchedulerTolerance(unittest.TestCase):
    def test_tolerance_used_when_set(self):
        # Basic smoke test: Scheduler can be constructed with tolerance and a container.
        log = Logic_Component(frequency=10, name="L")
        tru = ConcreteTruth(state_names=["x"], initial_state=np.array([0.0]),
                            initial_control=np.array([0.0]),
                            integrator_type=Integrator_Enums.RK4, frequency=10, name="T")
        container = Container_Component(a_Logic_Component=log, a_Truth_Component=tru,
                                        Time_Varying_Components=[], name="C")
        s = Scheduler(container_components=[container], global_sim_start_time=0.0,
                    global_sim_end_time=1.0, round2Decimals=6,
                    end_time_tolerance=0.1)
        self.assertIsNotNone(s.end_time_tolerance)


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False, argv=sys.argv[:1])

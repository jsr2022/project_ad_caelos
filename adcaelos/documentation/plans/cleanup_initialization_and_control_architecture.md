# Plan: Fix Scheduler & Implement Initial State/Control Architecture

## Summary
Fix critical bugs in the scheduler, establish clean initial state/control initialization on Truth_Component subclasses, and make the simulation runnable end-to-end with the SpringMassDamper example.

## Changes

### 1. Fix Scheduler Bugs (`adcaelos/schedulers/scheduler.py`)
- Replace `getTime()` with `getNextTime()` on lines 58, 59, 63 (method doesn't exist)
- Rename `getTemporarySimulationTerminationCondition()` to `is_simulation_configured()` — clarify that it checks whether sim is properly configured, not whether it should terminate
- The method should return `True` when `global_sim_end_time > 0` (properly configured), `False` otherwise
- Simplify `run_simulation()` loop condition to: `while self.is_simulation_configured() and self.all_events and self.global_sim_start_time < self.global_sim_end_time:`
- If `global_sim_end_time == -1`, the sim does NOT run (not configured)

### 2. Add Initial State/Control to Truth_Component Subclasses
Both `SpringMassDamper` and `Simple_Aircraft` should accept `initial_state` and `initial_control` in their `__init__`, then call `setCurrState()` and `setCurrCntrl()`:

**`adcaelos/components/dynamics/spring_mass_damper.py`:**
- Add `initial_state: np.array = None` and `initial_control: np.array = None` parameters to `__init__`
- After calling `super().__init__()`, if `initial_state` is provided, call `self.setCurrState(initial_state)`; otherwise default to `np.zeros(self.__numStates)` (accessed via parent)
- If `initial_control` is provided, call `self.setCurrCntrl(initial_control)`; otherwise default to `np.zeros(1)` (zero force)

**`adcaelos/components/dynamics/simple_aircraft.py`:**
- Same pattern: add `initial_state` and `initial_control` parameters with zero defaults
- Initialize `self.Speed = 0.0` in `__init__` (currently `getSpeed()` would fail since Speed is never set)

### 3. Fix SpringMassDamper `statesDot()` Return Shape
- Line 59: `return np.array([position_dot, velocity_dot]).T` — the `.T` transpose is wrong for a 1D array of size 2. Should be `return np.array([position_dot, velocity_dot])`

### 4. Update Logic_Component (`adcaelos/components/logic_component.py`)
- Add `act()` method override that calls `subsystemMethod()` then advances time via `setNextTime()` — currently `Logic_Component` does NOT implement `act()`, so scheduler's `component.act()` call silently does nothing (inherited abstract method has empty body)
- Uncomment `subsystemMethod()` body: call `logicCenter()` and `truth_component.setCurrCntrl(control)`
- For testing: `logicCenter()` returns zero control stub (zero numpy array matching control size)

### 5. Update Truth_Component `act()` to handle missing initial state/control gracefully
- If `currState` or `currCntrl` is accessed before being set, provide a clear error message
- Consider adding a property-based lazy initialization that raises on first access if not set

### 6. Update `testSimulation.py` to test the full flow
- Create a SpringMassDamper with initial_state and initial_control (test optional params)
- Create a Container_Component with the SpringMassDamper and a dummy Logic_Component
- Create a Scheduler with a valid end time (e.g., 2.0 seconds)
- Run simulation and print state values to verify integration works
- Verify Logic runs before Truth at same timestamps (priority ordering)

## Architecture Rationale
- Initial state/control on Truth_Component subclasses keeps the dynamics system self-contained
- The Logic_Component reads state and computes control at runtime, buffering it to Truth_Component
- The first integration step uses the initial control (zero or user-specified) until Logic runs and buffers its first computed control
- Priority ordering (CONTROL=1 runs before TRUTH=5) means Logic naturally computes control before Truth integrates at each timestep

## Risks
- The `Event` dataclass `compare=True` on `time` and `priority` means when times are equal, priority determines order. This is intentional and correct.
- The termination condition logic needs careful handling to avoid infinite loops or premature exits

# Design Discussion: State and Control Data Storage Location and Hierarchy in ADCAELOS

## Context
This document records the design decisions regarding the placement of state data and helper functions in the component hierarchy, specifically within the `Time_Varying_Component`, `Truth_Component`, and `Logic_Component` classes.

## Questions Considered
1. Should the ODE state data field (`currState`, `statePos2Names`, `stateNames2Pos`) be moved up to `Time_Varying_Component`?
2. Should the helper functions (`getStatePos2Names`, `getStateNames2Pos`) be moved up to `Time_Varying_Component`?
3. Should control data (`currCntrl`) be saved at the `Time_Varying_Component` level?
4. How does this impact logging strategy?

## Decisions and Reasoning

### 1. ODE State Data Placement
**Decision:** Keep ODE state data in `Truth_Component` only.

**Reasoning:**
- `Time_Varying_Component` is a scheduling abstraction (concerned with *when* to run).
- `Truth_Component` is a physics/ODE abstraction (owns integrable state vector and control inputs).
- `Logic_Component` has no ODE states; it computes command outputs.
- Moving ODE state to `Time_Varying_Component` would force non-physics components (e.g., future sensors, timers) to carry unnecessary state vector machinery.

### 2. Helper Functions Placement
**Decision:** Keep `getStatePos2Names` and `getStateNames2Pos` in `Truth_Component`.

**Reasoning:**
- These functions are tightly coupled to the ODE state-vector indexing scheme.
- They are specific to the truth component's need to map between state names and indices for integration and logging.
- They have no relevance to generic time-varying components or logic components.

### 3. Control Data Placement
**Decision:** Keep `currCntrl` in `Truth_Component` only.

**Reasoning:**
- `currCntrl` is an input to the ODE (`statesDot` method) and is consumed by the physics model.
- It is not a general property of "something that runs at a frequency."
- `Logic_Component` writes to `currCntrl` via the container, which is the correct direction of data flow (logic -> truth).
- Moving it upward would misrepresent the data dependencies.

### 4. Logging Strategy
**Decision:** Implement logging via the existing `store_data()` hook in `Time_Varying_Component`, overridden in subclasses.

**Reasoning:**
- The `store_data(logger)` method in `Time_Varying_Component` defines the *when* (called by scheduler after `act()`).
- Each component logs what it owns:
  - `Truth_Component.store_data()`: logs time, state names/values, and control values.
  - `Logic_Component.store_data()`: logs time and command outputs (introduce `_logged_outputs` dict).
- This provides a uniform logging interface without hoisting state machinery upward.
- Avoids data duplication and maintains clear abstraction boundaries.

## Additional Notes

### Bug Fix in `time_varying_component.py`
An existing defect in `set_next_time()` (line 52) must be fixed:
- The explicit-override branch incorrectly recomputes frequency from a time delta, risking division by zero.
- Corrected behavior: re-anchor the counter to the explicit time without altering frequency.
- Fixed code:
```python
def set_next_time(self, next_time: float = None) -> None:
    if next_time is None:
        self.__step_count += 1
        self.__next_time = self.__start_counter_time + self.__step_count / self.__frequency
    else:
        # Re-anchor to explicit time; frequency is unchanged
        self.__start_counter_time = float(next_time)
        self.__step_count = 0
        self.__next_time = self.__start_counter_time
```

## Summary of Data Placement
| Data/Method                | Class                  | Reason                                                                 |
|----------------------------|------------------------|------------------------------------------------------------------------|
| `currState`                | `Truth_Component`      | Integrable ODE state (physics concept)                                 |
| `statePos2Names`/`stateNames2Pos` | `Truth_Component`  | ODE-specific index mapping                                             |
| `currCntrl`                | `Truth_Component`      | ODE input, consumed by `statesDot`                                     |
| Command outputs            | `Logic_Component`      | Owned by logic component                                               |
| `store_data()` hook        | `Time_Varying_Component`| Scheduling concern - defines when logging fires                        |
| frequency/next_time/period  | `Time_Varying_Component`| Pure timing - correct as-is                                            |

This approach maintains clean semantic boundaries, avoids over-abstracting the base class, and provides a scalable path for logging and future component types.
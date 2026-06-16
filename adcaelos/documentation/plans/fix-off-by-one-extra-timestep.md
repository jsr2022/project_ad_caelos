# Fix: Off-by-One Extra Timestep at Simulation End

## Problem Analysis

### The Root Cause

`Time_Varying_Component.get_time()` returns the private field `__next_time`, which represents
**"the time at which this component is next scheduled to execute."** The scheduler's termination
guard in `run_simulation` reads `component.get_time()` *before* calling `act()`, so it sees the
component's current scheduled execution time.

With the `<=` guard, the event at exactly `t = end_time` passes the check
(`end_time <= end_time` → True), so `act()` runs. That call integrates forward by one `dt` past
`end_time`, storing a spurious extra data point.

### Concrete Trace (20s sim at 1 Hz, end_time=20.0)

| Event time (pre-act) | Guard (`<= 20.0`) | Integrates from→to | Data stored |
|---|---|---|---|
| 0.0  | ✓ pass | 0→1  | t=1.0 |
| 1.0  | ✓ pass | 1→2  | t=2.0 |
| ...  | ...    | ...  | ...   |
| 19.0 | ✓ pass | 19→20 | t=20.0 |
| 20.0 | ✓ pass (**BUG**) | 20→21 | t=21.0 ← extra |

Plus the IC stored at t=0.0 by `Data_Storage.__init__`, this produces 22 points instead of 21.

### Secondary Bug: `calculateOtherStates` receives the wrong time

In `truth_component.py:act()`, `calculateOtherStates` is currently called **before**
`set_next_time()`:

```python
# Current (wrong) ordering inside act():
state = self.integrator.getNextState(currTime=self.get_time(), dt=self.get_period())
#   → state is now at t=1, but self.get_time() still returns t=0
self.setCurrState(state)
other_states = self.calculateOtherStates(state, self.getCurrCntrl(), self.get_time())
#   ↑ BUG: passes time=0 (old) while state is at t=1 (new)
self.set_next_time()      # __next_time finally advances to t=1
self.store_states()       # stores correctly at t=1
```

Both current implementations of `calculateOtherStates` (`SpringMassDamper`,
`Simple_Aircraft`) are `pass`, so there is no runtime impact today. But the abstract method
contract is violated: any future implementation that uses `current_time` to look up, e.g.,
time-varying atmospheric conditions, will silently compute them at the *wrong* time against
the *new* state.

---

## Variable Step Size Consideration

The `< end_time` fix is **fully correct for all fixed-frequency components** (the entire current
codebase). For future variable-step integrators, the scheduler boundary alone is insufficient
for exact-endpoint termination regardless of whether `<` or `<=` is used:

| Step behavior | `<=` (current, broken) | `<` (proposed fix) |
|---|---|---|
| Fixed step, last step lands exactly on `end_time` | Runs one extra step past `end_time` ❌ | Skips event at `end_time`, data ends correctly at `end_time` ✓ |
| Variable step, last step overshoots `end_time` | Same overshoot ❌ | Same overshoot ❌ |
| Variable step, last step undershoots `end_time` | Endpoint not reached ❌ | Endpoint not reached ❌ |

To guarantee exact termination at `end_time` with variable step sizes, a **step-clamping
mechanism** is needed inside `act()` or the integrator: when `current_time + dt > end_time`,
clamp `dt = end_time - current_time`. This is a **separate future feature** and is out of scope
for this fix.

**Conclusion**: The `< end_time` change is the correct fix for the current bug. Do not rely on
the scheduler's termination boundary alone for exact-endpoint behavior when variable-step
integration is introduced.

---

## Implementation Plan

### File 1: `adcaelos/schedulers/scheduler.py`

#### 1a. Method rename: `_time_lte_end` → `_time_lt_end`
The name must match the new semantics (strict less-than, not less-than-or-equal).

#### 1b. Logic change in `_time_lt_end`: `<=` → `<`
```python
# BEFORE
def _time_lte_end(self, t: float) -> bool:
    """Return True if t is considered <= global_sim_end_time given tolerance."""
    if self.end_time_tolerance is None:
        return t <= self.global_sim_end_time
    return t <= self.global_sim_end_time + self.end_time_tolerance

# AFTER
def _time_lt_end(self, t: float) -> bool:
    """Return True if t is strictly before global_sim_end_time (with optional tolerance).

    Strict less-than is required because t is the component's *current* scheduled
    execution time, not the time the integration result will land at.  If t == end_time,
    act() would integrate one full dt beyond end_time, producing a spurious extra step.
    The event at end_time is intentionally skipped; the final data point (at end_time) is
    stored by the *previous* act() call which integrated from (end_time - dt) → end_time.
    """
    if self.end_time_tolerance is None:
        return t < self.global_sim_end_time
    return t < self.global_sim_end_time + self.end_time_tolerance
```

#### 1c. Update call site in `run_simulation`
Replace the call `self._time_lte_end(...)` with `self._time_lt_end(...)` and add an inline
comment:

```python
# component.get_time() is the component's *scheduled* execution time (pre-act).
# Strict < prevents the boundary event from running act() one step past end_time.
if self._time_lt_end(next_event.component.get_time()):
```

---

### File 2: `adcaelos/components/time_varying_component.py`

#### 2a. Docstring addition for `get_time()`
Add a clear docstring explaining the dual role of the return value:

```python
def get_time(self) -> float:
    """Return this component's current scheduled execution time.

    Before act() is called this equals the time the component will integrate *from*.
    After set_next_time() is called inside act() it equals:
      - the time the newly integrated state was computed *at*, AND
      - the time this component will be scheduled to execute *next*.
    Both interpretations are numerically identical; the field advances by exactly one
    period per call to set_next_time().
    """
    return self.__next_time
```

#### 2b. Docstring improvement for `set_next_time()`
Replace or augment the current (missing) docstring:

```python
def set_next_time(self, next_time: float = None, next_frequency: int = None) -> None:
    """Advance this component's scheduled time by one period.

    Called at the end of act() (after integration and state update) to record that
    the component has completed one step.  After this call:
      - get_time() returns the time the just-computed state represents
      - get_time() is also the time the scheduler will use for the next event

    Args:
        next_time / next_frequency: Both must be provided together to re-anchor the
            integer step counter at a new time with a new frequency (used for
            non-fixed-step overrides).  Providing only one raises ValueError.
    """
```

#### 2c. Inline comment on `__next_time` field initialization
Add a comment next to the field so the intent is obvious when reading `__init__`:

```python
# Tracks this component's scheduled execution time.
# Advances by exactly 1/frequency seconds on each set_next_time() call.
# Also equals the time label of the most recently stored state (after act() completes).
self.__next_time = float(next_time)
```

---

### File 3: `adcaelos/components/truth_component.py`

#### 3a. Reorder operations in `act()` — bug fix + clarity

Move `set_next_time()` to *before* `calculateOtherStates` so the time argument is correct.
Replace the misleading comment with a block comment that documents the intentional ordering:

```python
def act(self) -> None:
    """Integrate one time step and store results.

    Operation order is intentional:
      1. Integrate: compute new state at (current_time + dt)
      2. Update state: store the new state on the component
      3. Advance schedule: set_next_time() so get_time() now equals the new state's time
      4. Compute derived states: calculateOtherStates receives (new_state, new_time) ← correct
      5. Store: write state, control, and derived states at the new time
    """
    # 1 & 2: integrate from current time forward by one period
    state = self.integrator.getNextState(
        fieldObject=self,
        currTime=self.get_time(),
        dt=self.get_period()
    )
    self.setCurrState(state)

    # 3: advance schedule — get_time() now returns the time of the newly computed state
    self.set_next_time()

    # 4: compute any non-integrated derived states at (new_state, new_time)
    if self.__valid_other_states:
        other_states = self.calculateOtherStates(state, self.getCurrCntrl(), self.get_time())
        self.set_other_states(other_states)

    # 5: store state, control, and derived states — all labeled at the new time
    self.store_states()
```

#### 3b. Docstring update for `calculateOtherStates` abstract method
Clarify that `current_time` will equal the newly integrated state's time (i.e., *after*
`set_next_time()` has been called by `act()`):

```python
@abstractmethod
def calculateOtherStates(self, current_state: np.array, current_control: np.array,
                          current_time: float) -> np.array:
    """Compute derived (non-integrated) states at the newly integrated time step.

    Called by act() after set_next_time(), so current_time equals the time the
    integrator just advanced *to* (i.e., previous_time + dt).
    Must be implemented in every subclass.
    """
```

---

### File 4: `adcaelos/documentation/adcaelos_simulation_framework.md`

#### 4a. Section 6 — mark the off-by-one bug as RESOLVED

Add a new resolved entry in the **Scheduler Incomplete** bullet:

```markdown
- ~~**Off-by-one extra timestep**: `_time_lte_end` used `<=` so the event at exactly
  `end_time` was allowed to run `act()`, integrating one full step past the end and
  storing a spurious data point.~~ **[RESOLVED]**
    - **Fix**: Changed guard from `<=` to strict `<` and renamed helper to `_time_lt_end`.
      The event at `end_time` is now skipped; the final data point (at `end_time`) is
      correctly stored by the previous step which integrated from `(end_time − dt) → end_time`.
      Note: for variable step sizes, exact endpoint termination requires an additional
      step-clamping mechanism (future work).
```

#### 4b. Section 6 — mark the `calculateOtherStates` timing issue as RESOLVED

Add a new resolved entry under **Abstract Methods** or as its own bullet:

```markdown
- ~~**`calculateOtherStates` time argument mismatch**: `act()` called `calculateOtherStates`
  before `set_next_time()`, so `current_time` was the *previous* step's time while
  `current_state` was already the newly integrated state. Silent bug with no runtime impact
  today (both implementations are `pass`) but would corrupt any future implementation.~~
  **[RESOLVED]**
    - **Fix**: Reordered `act()` so `set_next_time()` runs before `calculateOtherStates`,
      ensuring `current_time` always matches the time the newly integrated state represents.
```

#### 4c. Section 6 — update the Scheduler Incomplete bullet

The "needs improved termination criteria" note should be updated to reflect the fix:

Change:
```markdown
- **Scheduler Incomplete**:
    - have current version working
    - needs improved termination criteria
```
To:
```markdown
- **Scheduler Incomplete**:
    - have current version working
    - ~~needs improved termination criteria (off-by-one extra step)~~ **[RESOLVED]** — see above
    - vehicle-specific termination criteria (where to implement?) — still open
```

---

## Summary of All Name / Comment Changes

| File | Type | Old | New | Reason |
|---|---|---|---|---|
| `scheduler.py` | Method rename | `_time_lte_end` | `_time_lt_end` | Name must match new `<` semantics |
| `scheduler.py` | Method docstring | *(existing one-liner)* | Full docstring explaining why strict `<` is used | Clarity |
| `scheduler.py` | Inline comment in `run_simulation` | *(none)* | Comment on `get_time()` guard explaining pre-act semantics | Clarity |
| `time_varying_component.py` | Method docstring | *(missing)* | Full docstring for `get_time()` explaining dual role | Clarity |
| `time_varying_component.py` | Method docstring | *(missing)* | Full docstring for `set_next_time()` explaining timing contract | Clarity |
| `time_varying_component.py` | Inline comment | *(missing)* | Comment on `self.__next_time` field init | Clarity |
| `truth_component.py` | Inline comment | `# we just calculated the data at this time step!` | Block docstring + numbered inline comments for each step | Clarity + correctness |
| `truth_component.py` | Operation order | `calculateOtherStates` before `set_next_time()` | `set_next_time()` before `calculateOtherStates` | **Bug fix** |
| `truth_component.py` | Abstract method docstring | *(existing)* | Clarify that `current_time` equals new state's time | Correctness |
| `adcaelos_simulation_framework.md` | Section 6 bug entry | *(missing)* | Add RESOLVED entry for off-by-one termination bug | Documentation |
| `adcaelos_simulation_framework.md` | Section 6 bug entry | *(missing)* | Add RESOLVED entry for `calculateOtherStates` time mismatch | Documentation |
| `adcaelos_simulation_framework.md` | Section 6 scheduler bullet | "needs improved termination criteria" | Mark as RESOLVED, keep vehicle-specific termination as open | Documentation |

---

## Testing

After the fix, verify with `testSimulation.py` (20s at 100 Hz):

- `smd.state_data.num_steps_stored` should equal **2001** (IC at t=0, plus 2000 steps: t=0.01…t=20.00)
- `smd.get_time()` after simulation should equal **20.01** (the next scheduled time; never executed — correct)
- No data point at t=20.01 should exist in `state_data`

The existing `adcaelos_unit_tests.py` tests do not assert step counts tied to simulation end
time, so no unit test changes are required.

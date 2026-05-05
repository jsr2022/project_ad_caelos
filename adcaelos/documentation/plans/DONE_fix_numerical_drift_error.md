## Runtime Numerical Error Fix
05/05/2026

1. **Non-fixed-step override: RE-ANCHOR.** `setNextTime(t)` resets
   `__start_time = t` and `__step_count = 0` so subsequent default calls
   resume a drift-free sequence anchored at the new time. (See §3.1 pseudocode
   — already reflects this choice.)
2. **Scheduler end-time tolerance: CONFIGURABLE.** Add an optional tolerance
   to the `Scheduler.__init__` signature, defaulting to off. When enabled,
   the end-time comparison uses `math.isclose` (or `nextTime <= end + tol`)
   rather than strict `<=`.
   - Add parameter `end_time_tolerance: float | None = None` to
     `Scheduler.__init__`.
   - When `None`, behaviour is today's strict `<=`.
   - When a float, comparisons in `run_simulation` use
     `nextTime <= global_sim_end_time + end_time_tolerance` (and optionally
     a `math.isclose(..., abs_tol=end_time_tolerance)` guard for the final
     step).
3. **Runtime frequency changes: SUPPORTED.** Add `setFrequency(new_freq: int)`
   on `Time_Varying_Component`:
   ```python
   def setFrequency(self, new_frequency: int) -> None:
       # Re-anchor so the integer-counter invariant is preserved under a
       # frequency change mid-simulation.
       self.__start_time = self.nextTime
       self.__step_count = 0
       self.__frequency = new_frequency
       self.__period = 1.0 / new_frequency
   ```
   This keeps the same drift-free property across frequency transitions.

## 6. Final Change Checklist

- [x] `time_varying_component.py`
  - Add `__start_counter_time: float`, `__step_count: int` fields.
  - Rewrite `setNextTime` to use integer-counter formula; switch sentinel to
    `None`; re-anchor on explicit override.
  - Add `setFrequency(new_frequency: int)` that re-anchors.
  - Add `getStepCount()` accessor for debugging.
- [x] `scheduler.py`
  - Add optional `end_time_tolerance` parameter to `__init__`.
  - Apply tolerance in `run_simulation` boundary check when configured.
  - Removed `np.round` from `update_event` (now unnecessary; value is drift-free).
  - Kept rounding guard in boundary check for backwards compatibility.
- [x] Add regression test (`adcaelos_unit_tests.py`) for 1M ticks @ 100 Hz →
  `|nextTime - 10000.0| < 1e-9` passes.
- [x] Re-run existing sim (`testSimulation.py`): observed clean time progression
  (20.00 boundary reached, subsequent steps correctly treated as over end time).
  No spurious drift-induced extra/missing steps.
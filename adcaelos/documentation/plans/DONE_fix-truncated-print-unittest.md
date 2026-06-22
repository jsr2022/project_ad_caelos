# Plan: Fix Partial "Unpacking Container Component: C" Print in Tests

## Problem Analysis

When running `python -m unittest adcaelos_unit_tests.py`, the test output is truncated to:

```
Unpacking Container Component: C
```

The root cause is in `adcaelos/schedulers/scheduler.py:58`. The `Scheduler.__init__` calls `self.unpack_container_components(container_components)`, which prints `Unpacking Container Component: {container.get_name()}` for every active container. Since this `print` runs at construction time (inside `__init__`), it executes during test setup **before** `unittest` has finished discovering/loading all tests. The test runner captures stdout, and output produced during test discovery/loading appears truncated or incomplete in the terminal.

## Root Cause Details

| File | Line | Issue |
|------|------|-------|
| `adcaelos/schedulers/scheduler.py` | 58 | `print(f"Unpacking Container Component: {container.get_name()}")` inside `unpack_container_components`, called from `__init__` |

`Scheduler` is instantiated in `TestSchedulerTolerance.test_tolerance_used_when_set` (`adcaelos_unit_tests.py:120`), but the print fires during that test's setup. However, because the `Scheduler` constructor also runs `unpack_container_components` which iterates and prints, and `unittest` may be mid-discovery, the output appears cut off at "C" (the container name passed in the test: `name="C"`).

## Fix Plan

### 1. Comment out the diagnostic print
**File:** `adcaelos/schedulers/scheduler.py:58`

Comment out the print statement to prevent stdout pollution during test discovery/construction.

```python
# print(f"Unpacking Container Component: {container.get_name()}")
```

### 2. Ensure no other side-effect prints in `__init__` paths
Review `unpack_container_components` and `__init__` for any other `print` statements that could interfere with test discovery. None were found beyond line 58, but verify `run_simulation` prints (lines 134-141) are only hit during explicit simulation runs, not construction.

### 3. Verify tests pass cleanly
After the change, run:
```bash
python -m unittest adcaelos_unit_tests.py -v
```
Expected: clean verbose output with no truncated prints, all tests passing.

## Tradeoffs / Considerations

- **Test impact**: The `TestSchedulerTolerance` test does not assert on stdout, so commenting out the print will not break any assertions.
- **Backward compatibility**: No API changes; only internal diagnostic output is suppressed.

## Implementation Steps

1. Edit `adcaelos/schedulers/scheduler.py:58`:
   - Comment out `print(f"Unpacking Container Component: {container.get_name()}")`.
2. Run `python -m unittest adcaelos_unit_tests.py -v` to verify clean output.

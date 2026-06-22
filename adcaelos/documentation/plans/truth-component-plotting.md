# Truth Component Plotting Script Plan

## Overview
Create a plotting module in `adcaelos/plotting/` that generates subplots stored data from Truth_Component(s) accessed via Container_Component(s). The module will create separate figures for states, control, and other_states, each with subplots per variable vs time.

## Data Flow
```
Container_Component(s) → getTC() → Truth_Component → state_data/control_data/other_state_data (Data_Storage) → get_all_stored_data() → dict with time + variables → matplotlib subplots
```

## File Structure
```
adcaelos/
└── plotting/
    ├── __init__.py
    └── truth_plotting.py    # Main plotting functions
```

## Core Functions

### 1. `extract_truth_components(container_components) -> list[Truth_Component]`
- Accepts single Container_Component or list of Container_Components
- Extracts TC via `container.getTC()` for each
- Returns list of Truth_Components

### 2. `get_stored_data(truth_component) -> dict`
- Returns dict with keys: 'states', 'control', 'other_states'
- Each value is a Data_Storage's `get_all_stored_data()` result
- Handles optional control/other_states gracefully

### 3. `plot_truth_data(truth_components, **kwargs) -> dict[figure_name: Figure]`
Main plotting function that:
- Creates 3 figures: "States vs Time", "Control vs Time", "Other States vs Time"
- Each figure has subplots (one per variable, shared x-axis = time)
- Returns dict of figure handles for further customization

### 4. `save_figures(figures, save_folder, dpi, figsize, file_format, timestamp) -> None`
- Handles saving with optional timestamp in folder name
- Creates folder if needed
- Supports png, pdf, svg formats

## Function Signature
```python
def plot_truth_components(
    container_components: Container_Component | list[Container_Component],
    # Save options
    save_plots: bool = False,
    save_folder: str = "plots",
    use_timestamp: bool = True,
    dpi: int = 300,
    figsize: tuple[float, float] = (10, 6),
    file_format: str = "png",
    # Styling (auto-generated unless overridden)
    labels: list[str] | None = None,
    colors: list[str] | None = None,
    linestyles: list[str] | None = None,
    # Legend
    show_legend: bool = True,
    legend_loc: str = "best",
    # Other
    show: bool = True,
) -> dict[str, plt.Figure]:
```

## Subplot Layout
- **Figure 1: "States vs Time"** - N subplots (N = num_states), shared x-axis
- **Figure 2: "Control vs Time"** - M subplots (M = num_control), shared x-axis (only if control exists)
- **Figure 3: "Other States vs Time"** - K subplots (K = num_other_states), shared x-axis (only if other_states exists)

## Data Extraction from Data_Storage
```python
data = truth_component.state_data.get_all_stored_data()
# data[0] = time array
# data[1], data[2], ... = state variables (keys map to state names via state_position_2_names)
```

## Multi-Component Handling
- Overlay all components on same subplots
- Auto-generate labels from `component.get_name()`
- Auto-assign colors via matplotlib's default cycle
- Allow user override via `labels`, `colors`, `linestyles` params
- Legend shows component names

## Implementation Details
1. **Import matplotlib** inside function (optional dependency)
2. **Time alignment**: All data stored at same timestamps per component
3. **Missing data**: Skip figure if no control/other_states data exists for any component
4. **Figure management**: Use `plt.subplots()` with `sharex=True`
5. **Cleanup**: Close figures if `show=False` and not saving

## Testing
- Run with testSimulation.py SpringMassDamper (has states + control, no other_states)
- Verify plots show correct variable names from Data_Storage
- Test single and multi-component scenarios

## Future Extensions (Not in Scope)
- Interactive plots (plotly)
- Animation/movie generation
- 3D trajectory plots
- Phase plane plots
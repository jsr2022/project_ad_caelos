import os
import datetime
from typing import Union, List, Dict, Optional, Tuple

from adcaelos.components.container_component import Container_Component
from adcaelos.components.truth_component import Truth_Component


def extract_truth_components(
    container_components: Union[Container_Component, List[Container_Component]]
) -> List[Truth_Component]:
    if isinstance(container_components, Container_Component):
        return [container_components.getTC()]
    return [cc.getTC() for cc in container_components]


def get_stored_data(truth_component: Truth_Component) -> dict:
    data = {}
    data['states'] = truth_component.state_data.get_all_stored_data()
    data['state_names'] = truth_component.state_data.get_state_position_2_names()
    
    if hasattr(truth_component, 'control_data') and truth_component.control_data is not None:
        data['control'] = truth_component.control_data.get_all_stored_data()
        data['control_names'] = truth_component.control_data.get_state_position_2_names()
    else:
        data['control'] = None
        data['control_names'] = None
        
    if hasattr(truth_component, 'other_state_data') and truth_component.other_state_data is not None:
        data['other_states'] = truth_component.other_state_data.get_all_stored_data()
        data['other_states_names'] = truth_component.other_state_data.get_state_position_2_names()
    else:
        data['other_states'] = None
        data['other_states_names'] = None
        
    return data


def plot_truth_data(
    truth_components: List[Truth_Component],
    labels: Optional[List[str]] = None,
    colors: Optional[List[str]] = None,
    linestyles: Optional[List[str]] = None,
    show_legend: bool = True,
    legend_loc: str = "best",
    figsize: Tuple[float, float] = (10, 6)
) -> Dict[str, object]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("matplotlib is required for plotting. Install it via 'pip install matplotlib'.")
    
    if not truth_components:
        return {}
        
    figures = {}
    all_data = [get_stored_data(tc) for tc in truth_components]
    
    has_control = any(d['control'] is not None for d in all_data)
    has_other_states = any(d['other_states'] is not None for d in all_data)
    
    if labels is None:
        labels = [tc.get_name() for tc in truth_components]
    
    if colors is None:
        colors = [f"C{i}" for i in range(len(truth_components))]
    if linestyles is None:
        linestyles = ["-"] * len(truth_components)
        
    state_data_list = [d['states'] for d in all_data]
    state_names_dict = all_data[0]['state_names']
    num_states = len(state_names_dict)
    
    if num_states == 0:
        return figures
        
    fig_states, axes_states = plt.subplots(num_states, 1, figsize=figsize, sharex=True)
    if num_states == 1:
        axes_states = [axes_states]
        
    for i, (pos, name) in enumerate(state_names_dict.items()):
        for j, data in enumerate(state_data_list):
            time_data = data[0]
            state_data = data[pos]
            axes_states[i].plot(time_data, state_data, label=labels[j], color=colors[j], linestyle=linestyles[j])
        axes_states[i].set_ylabel(name)
        if show_legend and i == 0:
            axes_states[i].legend(loc=legend_loc)
            
    axes_states[-1].set_xlabel("Time")
    fig_states.suptitle("States vs Time")
    figures["States vs Time"] = fig_states
    
    if has_control:
        control_names_dict = all_data[0]['control_names']
        num_control = len(control_names_dict)
        
        fig_control, axes_control = plt.subplots(num_control, 1, figsize=figsize, sharex=True)
        if num_control == 1:
            axes_control = [axes_control]
            
        for i, (pos, name) in enumerate(control_names_dict.items()):
            for j, d in enumerate(all_data):
                if d['control'] is None:
                    continue
                data = d['control']
                time_data = data[0]
                control_data = data[pos]
                axes_control[i].plot(time_data, control_data, label=labels[j], color=colors[j], linestyle=linestyles[j])
            axes_control[i].set_ylabel(name)
            if show_legend and i == 0:
                axes_control[i].legend(loc=legend_loc)
                
        axes_control[-1].set_xlabel("Time")
        fig_control.suptitle("Control vs Time")
        figures["Control vs Time"] = fig_control
        
    if has_other_states:
        other_names_dict = all_data[0]['other_states_names']
        num_other = len(other_names_dict)
        
        fig_other, axes_other = plt.subplots(num_other, 1, figsize=figsize, sharex=True)
        if num_other == 1:
            axes_other = [axes_other]
            
        for i, (pos, name) in enumerate(other_names_dict.items()):
            for j, d in enumerate(all_data):
                if d['other_states'] is None:
                    continue
                data = d['other_states']
                time_data = data[0]
                other_data = data[pos]
                axes_other[i].plot(time_data, other_data, label=labels[j], color=colors[j], linestyle=linestyles[j])
            axes_other[i].set_ylabel(name)
            if show_legend and i == 0:
                axes_other[i].legend(loc=legend_loc)
                
        axes_other[-1].set_xlabel("Time")
        fig_other.suptitle("Other States vs Time")
        figures["Other States vs Time"] = fig_other
        
    return figures


def save_figures(
    figures: Dict[str, object],
    save_folder: str = "plots",
    dpi: int = 300,
    figsize: Tuple[float, float] = (10, 6),
    file_format: str = "png",
    use_timestamp: bool = True
) -> None:
    valid_formats = {"png", "pdf", "svg"}
    if file_format not in valid_formats:
        raise ValueError(f"file_format must be one of {valid_formats}")
        
    if use_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_folder = f"{save_folder}_{timestamp}"
        
    abs_save_folder = os.path.abspath(save_folder)
    abs_cwd = os.path.abspath(os.getcwd())
    if not abs_save_folder.startswith(abs_cwd):
        raise ValueError("save_folder must be within the current working directory")
        
    os.makedirs(abs_save_folder, exist_ok=True)
    
    for name, fig in figures.items():
        safe_name = name.replace(" ", "_").replace("/", "_")
        filepath = os.path.join(abs_save_folder, f"{safe_name}.{file_format}")
        fig.savefig(filepath, dpi=dpi, bbox_inches="tight")


def plot_truth_components(
    container_components: Union[Container_Component, List[Container_Component]],
    save_plots: bool = False,
    save_folder: str = "plots",
    use_timestamp: bool = True,
    dpi: int = 300,
    figsize: Tuple[float, float] = (10, 6),
    file_format: str = "png",
    labels: Optional[List[str]] = None,
    colors: Optional[List[str]] = None,
    linestyles: Optional[List[str]] = None,
    show_legend: bool = True,
    legend_loc: str = "best",
    show: bool = True,
) -> Dict[str, object]:
    truth_components = extract_truth_components(container_components)
    figures = plot_truth_data(
        truth_components=truth_components,
        labels=labels,
        colors=colors,
        linestyles=linestyles,
        show_legend=show_legend,
        legend_loc=legend_loc,
        figsize=figsize
    )
    
    if save_plots:
        save_figures(
            figures=figures,
            save_folder=save_folder,
            dpi=dpi,
            figsize=figsize,
            file_format=file_format,
            use_timestamp=use_timestamp
        )
        
    if show:
        try:
            import matplotlib.pyplot as plt
            for fig in figures.values():
                fig.show()
        except ImportError:
            pass
    else:
        if not save_plots:
            try:
                import matplotlib.pyplot as plt
                for fig in figures.values():
                    plt.close(fig)
            except ImportError:
                pass
                
    return figures

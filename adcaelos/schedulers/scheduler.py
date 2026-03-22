#scheduler.py
#Import Python Default Library Packages
import heapq
from collections import defaultdict, deque
from datetime import datetime

#Import External Python Packages
import numpy as np

#Import Adcaelos Specific Packages
#Scheduler Subsystems:
from adcaelos.schedulers.scheduler_enums import Scheduler_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums
#Components and Corresponding Subsystems:
from adcaelos.components.component_enums import Component_Enums
from adcaelos.components.base_component import Base_Component
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.logic_component import Logic_Component
from adcaelos.components.container_component import Container_Component

class Scheduler():
    """
    Scheduler class for managing execution of components in a simulation.
    Handles:
    - Unpacking container components
    - Building dependency graph based on component connections
    - Topologically sorting components for execution order
    - Managing simulation time and execution of components at correct times
    """
    def __init__(self, container_components=None, global_sim_start_time = 0, global_sim_end_time = -1) -> None:
        
        if isinstance(global_sim_start_time, datetime):
            self.setup_sim_specific_datetime(global_sim_start_time)
        else:
            self.setup_sim_float_time(global_sim_start_time)

        self.unpack_container_components(container_components)
        

    def unpack_container_components(self, container_components) -> list:
        pass

    def initialize_dependencies(self, listAllComponents) -> None:
        pass

    def build_dependency_graph(self, listAllComponents) -> None:
        pass

    def compareComponents(self, c1, c2) -> bool:
        pass

    def topologicalSortDependencyGraph(self, dependencyGraph) -> dict:
        pass

    def setup_sim_specific_datetime(self, startTime: datetime) -> None:
        pass

    def setup_sim_float_time(self, start_time: float) -> None:
        self.global_sim_start_time = start_time

    def addToHeap(self, listAllComponents) -> list:
        pass

    def run_simulation(self, SimStuff) -> None:
        pass

    
#scheduler.py
#Import Python Default Library Packages
import heapq
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime

#Import External Python Packages
import numpy as np

#Import Adcaelos Specific Packages
#Scheduler Subsystems:
from adcaelos.schedulers.scheduler_enums import Scheduler_Enums
from adcaelos.schedulers.scheduler_priority_enums import Scheduler_Priority_Enums
from adcaelos.schedulers.event import Event

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
        self.global_sim_end_time = global_sim_end_time
        self.all_events = []
        self.unpack_container_components(container_components)
        

    def unpack_container_components(self, container_components) -> None:
        """
        Unpacks container components into their individual components and connections.
        Returns a list of all individual components and a list of all connections.
        """
        if not container_components:
            raise ValueError("Error: No Container Components Provided to Scheduler")

        for container in container_components:            
            print(f"Unpacking Container Component: {container.getName()}")
            
            tempTruthComponent = container.getTC()
            tempLogicComponent = container.getLC()
            tempEventTruth = Event(tempTruthComponent.getNextTime(), priority=tempTruthComponent.getSchedulerPriorityEnum() , component=tempTruthComponent, action=f"Container Truth Component: {tempTruthComponent.getName()} Event")
            tempEventLogic = Event(tempLogicComponent.getNextTime(), priority=tempLogicComponent.getSchedulerPriorityEnum() , component=tempLogicComponent, action=f"Container Logic Component: {tempLogicComponent.getName()} Event")
            self.addToHeap(tempEventTruth)
            self.addToHeap(tempEventLogic)
            for TVC in container.getTVC():
                tempEventTVC = Event(TVC.getNextTime(), priority=TVC.getSchedulerPriorityEnum() , component=TVC, action=f"Container Time Varying Component: {TVC.getName()} Event")
                self.addToHeap(tempEventTVC)

    # def initialize_dependencies(self, listAllComponents) -> None:
    #     pass

    # def build_dependency_graph(self, listAllComponents) -> None:
    #     pass

    # def compareComponents(self, c1, c2) -> bool:
    #     pass

    # def topologicalSortDependencyGraph(self, dependencyGraph) -> dict:
    #     pass

    def update_event(self, event: Event) -> None:
        """
        Performs the action requested on the current event
        """
        component = event.component
        if isinstance(component, Time_Varying_Component):
            new_event = Event(component.getNextTime(), priority=component.getSchedulerPriorityEnum(), component=component, action=f"Time Varying Component: {component.getName()} Event")
        else:
            raise ValueError("Error: Component is not a Time Varying Component. Cannot Create Next Event.")
        self.addToHeap(new_event)

    def setup_sim_specific_datetime(self, startTime: datetime) -> None:
        """
        _summary_

        Parameters
        ----------
        startTime : datetime
            _description_
        """
        self.global_sim_start_time = 0


    def setup_sim_float_time(self, start_time: float) -> None:
        self.global_sim_start_time = start_time

    def addToHeap(self, event: Event) -> None:
        heapq.heappush(self.all_events, event)

    def getTemporarySimulationTerminationCondition(self) -> bool:
        """
        _summary_

        Returns
        -------
        bool
            Checks Simulation Termination Conditions Other than Time. Currently only returns true.
        """
        return True
    

    def run_simulation(self, SimStuff) -> None:
        while ((self.all_events and self.getTemporarySimulationTerminationCondition()) and (self.global_sim_start_time <= self.global_sim_end_time)):
            next_event = heapq.heappop(self.all_events)

            print(f"Executing Event: {next_event.action} at time {next_event.time}")
            next_event.component.act()
            self.update_event(next_event)

            self.global_sim_start_time = next_event.time
            

    
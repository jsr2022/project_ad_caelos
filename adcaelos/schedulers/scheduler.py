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

    def __init__(self, containerComponents = [], globalSimStartTime = 0, globalSimEndTime = 0) -> None:
        self.containerComponents = containerComponents
        if type(globalSimStartTime) == datetime:
            self.setupSimSpecificDatetime(globalSimStartTime)
        elif type(globalSimStartTime) == float:
            self.setupSimFloatTime(globalSimStartTime)
        else:
            #OTHER OPTION
            self.setupSimFloatTime(globalSimStartTime)
        
    def unpackContainerComponents(self, containerComponents) -> list:
        pass

    def initializeDependencies(self, listAllComponents) -> None:
        pass

    def buildDependencyGraph(self, listAllComponents) -> None:
        pass

    def compareComponents(self, c1, c2) -> bool:
        pass

    def topologicalSortDependencyGraph(self, dependencyGraph) -> dict:
        pass

    def setupSimSpecificDatetime(startTime: datetime) -> None:
        pass

    def setupSimFloatTime(startTime: float) -> None:
        pass

    def addToHeap(self, listAllComponents) -> list:
        pass

    def runSimulation(self, SimStuff) -> None:
        pass

    
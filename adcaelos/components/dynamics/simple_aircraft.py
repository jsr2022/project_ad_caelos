#simple_aircraft.py

#from python base package(s)
from sys import exit
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.utilities import sim_utils
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums


class Simple_Aircraft(Truth_Component):

    def __init__(self, stateNames: list, integratorType: Integrator_Enums = Integrator_Enums.RK4, frequency: int = 100, nextTime: float = 0, Component_Enum = Component_Enums.TRUTH_COMPONENT, name: str = "Simple_Aircraft", UUID: int = None) -> None:
        super().__init__(stateNames, integratorType, frequency, nextTime, Component_Enum, name, UUID)
    
    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + f"\n--Simple Aircraft Dynamics--"
    
    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        super().checkState(currState) #I want to know immediately if there is an error
        super().checkCntrl(currCntrl)

    def getLongitundialStateSpace(self, currState):
        # Flight characteristics and basic setup
        gravity = 32.174049  # ft/s^2
        alt = 35000  # ft
        ft2m = 0.3048  # 1 ft = m
        rho_imp_rho_m = 515.3788184  # rho imperial to rho metric
        Mach = 0.9
        nz = 1  # g loading
        plotting = False  # don't need to plot data

        # Assuming USAF_1976_std_atm returns an array where:
        # - data[3]: speed of sound in metric (m/s)
        # - data[2]: density in metric (kg/m^3)
        def USAF_1976_std_atm(plotting, altitude_m):
            # Dummy implementation - replace with your actual atmospheric model
            # Returning: [_, _, density_metric, speed_of_sound_metric]
            return [0, 0, 1.225, 340.29]  # Replace with actual function

        data = USAF_1976_std_atm(plotting, alt * ft2m)

        # Set up speed, density, and dynamic pressure
        v_speed_sound = data[3] / ft2m  # Speed of sound in ft/s
        Vinf = Mach * v_speed_sound  # ft/s
        rhoinf = data[2] / rho_imp_rho_m  # slugs/ft^3
        qinf = 0.5 * rhoinf * Vinf**2  # slugs/ft * 1/s^2 = lbs

        # A-4D Longitudinal Values Condition 6
        alpha = 2.9
        Xu = -0.0353
        Xa = -47.04
        Xpu = 0
        Xq = 0
        Xt = 0
        U0 = Vinf * cos(radians(alpha))
        Xa_dot = 0
        Zu = -0.120
        Za = -586.7
        Mu = -0.0050
        Ma = -14.99
        Ma_dot = -0.389
        Mq = -0.876
        Xde = -6.05
        Zde = -42.90
        Zpu = 0
        Zq = 0
        Zt = 0
        Za_dot = 0
        Mde = -14.80
        Mpu = 0
        Mt = 0
        Mpa = 0

        # Populating the A, B, C, and D matrices
        A = np.zeros((5, 5))

        # A Matrix Row 1
        A[0, 0] = Xu + Xpu + (Xa_dot * (Zu + Zpu)) / (U0 - Za_dot)
        A[0, 1] = Xa + (Xa_dot * Za) / (U0 - Za_dot)
        A[0, 2] = -gravity
        A[0, 3] = Xq + Xa_dot * (U0 + Zq) / (U0 - Za_dot)
        A[0, 4] = 0

        # A Matrix Row 2
        A[1, 0] = (Zu + Zpu) / (U0 - Za_dot)
        A[1, 1] = Za / (U0 - Za_dot)
        A[1, 2] = 0
        A[1, 3] = (U0 + Zq) / (U0 - Za_dot)
        A[1, 4] = 0

        # A Matrix Row 3
        A[2, 0] = 0
        A[2, 1] = 0
        A[2, 2] = 0
        A[2, 3] = 1
        A[2, 4] = 0

        # A Matrix Row 4
        A[3, 0] = Mu + Mpu + (Ma_dot * (Zu + Zpu)) / (U0 - Za_dot)
        A[3, 1] = Ma + Mpa + (Ma_dot * Za) / (U0 - Za_dot)
        A[3, 2] = 0
        A[3, 3] = Mq + Ma_dot * (U0 + Zq) / (U0 - Za_dot)
        A[3, 4] = 0

        # A Matrix Row 5
        A[4, 0] = 0
        A[4, 1] = -U0
        A[4, 2] = U0
        A[4, 3] = 0
        A[4, 4] = 0

        # Populating B Matrix
        B = np.zeros((5, 2))
        B[0, 0] = Xde + (Xa_dot * Zde) / (U0 - Za_dot)
        B[0, 1] = Xt + (Xa_dot * Zt) / (U0 - Za_dot)
        B[1, 0] = Zde / (U0 - Za_dot)
        B[1, 1] = Zt / (U0 - Za_dot)
        B[2, 0] = 0
        B[2, 1] = 0
        B[3, 0] = Mde + (Ma_dot * Zde) / (U0 - Za_dot)
        B[3, 1] = Mt + (Ma_dot * Zt) / (U0 - Za_dot)
        B[4, 0] = 0
        B[4, 1] = 0

        # Populating C and D Matrices
        C = np.eye(5)
        D = np.zeros((5, 2))
        
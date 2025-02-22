#simple_aircraft.py

#from python base package(s)
from sys import exit
from abc import ABC, abstractmethod

#from other package(s)
import numpy as np

#from adcaelos package(s)
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.component_enums import Component_Enums
from adcaelos.integrators.integrator_enums import Integrator_Enums

#utilities
from adcaelos.utilities.sim_utils import Sim_Utils
from adcaelos.atmosphere.atmosphere_models import Atmosphere_Models

class Simple_Aircraft(Truth_Component):

    def __init__(self, stateNames: list, integratorType: Integrator_Enums = Integrator_Enums.RK4, frequency: int = 100, nextTime: float = 0, Component_Enum = Component_Enums.TRUTH_COMPONENT, name: str = "Simple_Aircraft", UUID: int = None) -> None:
        super().__init__(stateNames, integratorType, frequency, nextTime, Component_Enum, name, UUID)

    def __str__(self) -> str:
        msgStr = super().__str__()
        msgStr = msgStr + f"\n--Simple Aircraft Dynamics--"
    
    def statesDot(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        super().checkState(currState) #I want to know immediately if there is an error
        super().checkCntrl(currCntrl)

        longStates = currState[0:9]
        latDirStates = currState[10:19]

        
        #call set speed
        #call component states
        #add pieces together 
        return np.zeros((currState.size)) #Temporary
    
    def calculateOtherStates(self, currState: np.array, currCntrl: np.array, currTime: float) -> np.array:
        pass

    def getLongitudinalStatesDot(self, longStates, longCntrl) -> np.array:
        """Returns Longitudinal State Space for A4D-Skyhawk Linearized at 15000m @ M=0.9
        This function will go beyond that single flight condition (incorrect obviously 
        but good for testing). Note Matrix Components are in Imperial Units but converting to
        Metric Units on input and output
        States are 10 x 1:
        0) perturbation body x velocity (u) [m/s]
        1) perturbation angle of attack (alpha) [rad]
        2) perturbation pitch angle (theta) [rad]
        3) perturbation pitch rate (q) [rad/s]
        4) perturbation height (h) (positive is down) [m]
        5) combined body x velocity (uC = u0 + u) [m/s]
        6) combined angle of attack (alphaC = alpha0 + alpha) [rad]
        7) combined pitch angle (thetaC = theta0 + theta) [rad]
        8) combined pitch rate (qC = q0 + q) [rad/s]
        9) combined height (hC = h0 - h) [m]"""

        u       = longStates[0]
        alpha   = longStates[1]
        theta   = longStates[2]
        q       = longStates[3]
        h       = longStates[4] #negative is pointing up!
        uC      = longStates[5]
        alphaC  = longStates[6]
        thetaC  = longStates[7]
        qC      = longStates[8]
        hC      = longStates[9] # Need to make sure that when tracking this, perturbed altitude is -h in this case

        longStatesDot = np.zeros((longStates.size, 1))

        altitude = hC
        (a_speed_sound, rhoinf) = Atmosphere_Models.simple1976EarthAtmosphere(altitude)
        Vinf = self.getSpeed()
        mach = Vinf/a_speed_sound
        qinf = 0.5 * rhoinf * Vinf**2  

        #Imperial Measurements Here Below
        gravity = 32.174049  # ft/s^2
        rho_imp_rho_m = 515.3788184  # rho imperial to rho metric
        alt_ft = altitude*Sim_Utils.m2ft()
        Vinf_ft = Vinf*Sim_Utils.m2ft()
        qinf_slugs_ft3 = (qinf/rho_imp_rho_m)*(Sim_Utils.m2ft()**2)

        # A-4D Longitudinal Values Condition 6
        Xu = -0.0353
        Xa = -47.04
        Xpu = 0
        Xq = 0
        Xt = 0
        U0 = uC - u
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
        A[0, 2] = -gravity*np.cos(thetaC)
        A[0, 3] = Xq + Xa_dot * (U0 + Zq) / (U0 - Za_dot)
        A[0, 4] = 0

        # A Matrix Row 2
        A[1, 0] = (Zu + Zpu) / (U0 - Za_dot)
        A[1, 1] = Za / (U0 - Za_dot)
        A[1, 2] = -gravity*np.sin(thetaC)
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
        A[4, 0] = np.sin(thetaC)
        A[4, 1] = -U0*np.cos(thetaC)
        A[4, 2] = U0*np.cos(thetaC)
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

        #Performing Matrix Multiplication
        longStatesDot[0:4] = np.matmul(A, longStates[0:4]) + np.matmul(B, longCntrl)
        
        #Converting from Imperial back to SI units
        longStatesDot[0] = longStatesDot[0] * Sim_Utils.ft2m() #state units = m/s
        longStatesDot[1] = longStatesDot[1] # state units are rads (no change)
        longStatesDot[2] = longStatesDot[2] # state units are rads (no change)
        longStatesDot[3] = longStatesDot[3] # state units are rad/s (no change)
        longStatesDot[4] = longStatesDot[4] * Sim_Utils.ft2m() #state units are m

        #Extending to non perturbation states (derivatives on non perturbed parts are 0 so they match!)
        longStatesDot[5:9] = longStatesDot[0:4]
        longStatesDot[9] = -1*longStatesDot[9] #need to flip derivative for height as perturb height is positive down!

        return longStatesDot
    
    def getLateralDirectionalStatesDot(self, latDirStates, latDirCntrl, altitude, alphaC) -> np.array:
        """Returns Lateral Directional State Space for A4D-Skyhawk Linearized at 15000m @ M=0.6
        This function will go beyond that single flight condition (incorrect obviously 
        but good for testing). Note Matrix Components are in Imperial Units but converting to
        Metric Units on input and output
        States are 10 x 1:
        0) perturbation side slip angle (beta) [rad]
        1) perturbation euler roll angle (phi) [rad]
        2) perturbation roll rate (p) [rad/s]
        3) perturbation yaw rate (r) [rad/s]
        4) perturbation euler yaw angle (psi) [rad]
        5) combined side slip angle (betaC = beta0 + beta) [rad]
        6) combined euler roll angle (phiC = phi0 + phi) [rad]
        7) combined roll rate (pC = p0 + p) [rad/s]
        8) combined yaw rate (rC = r0 + r) [rad/s]
        9) combined euler yaw angle (psiC = psi0 + psi) [rad]"""
        
        latDirStatesDot = np.zeros((latDirStates.size, 1))
        # Flight characteristics and basic definition setups
        gravity = 32.174049  # ft/s^2
        rho_imp_rho_m = 515.3788184  # rho imperial to rho metric

        (a_speed_sound, rhoinf) = Atmosphere_Models.simple1976EarthAtmosphere(altitude)
        Vinf = self.getSpeed()
        mach = Vinf/a_speed_sound
        qinf = 0.5 * rhoinf * Vinf**2  

        #Imperial Measurements Here Below
        gravity = 32.174049  # ft/s^2
        rho_imp_rho_m = 515.3788184  # rho imperial to rho metric
        alt_ft = altitude*Sim_Utils.m2ft()
        Vinf_ft = Vinf*Sim_Utils.m2ft()
        qinf_slugs_ft3 = (qinf/rho_imp_rho_m)*(Sim_Utils.m2ft()**2)

        # Lateral-Directional Space A-4D 6th problem
        alpha = alphaC
        U0 = Vinf * np.cos((alpha))
        Yb = -144.6
        Yda = -2.409
        Ydr = 25.09
        Yp = 0
        Yr = 0
        Lb_pr = -34.90
        Lp_pr = -1.516
        Lr_pr = 0.872
        Lda_pr = 21.27
        Ldr_pr = 9.918
        Nb_pr = 18.73
        Np_pr = 0.038
        Nr_pr = -0.565
        Nda_pr = 0.508
        Ndr_pr = -8.383

        # Populating the A matrix
        A = np.zeros((5, 5))
        A[0, 0] = Yb / U0
        A[0, 1] = gravity / U0 #not fully accurate as we are assuming near level pitch...
        A[0, 2] = Yp / U0
        A[0, 3] = (Yr / U0) - 1
        A[0, 4] = 0

        A[1, 0] = 0
        A[1, 1] = 0
        A[1, 2] = 1
        A[1, 3] = 0
        A[1, 4] = 0

        A[2, 0] = Lb_pr
        A[2, 1] = 0
        A[2, 2] = Lp_pr
        A[2, 3] = Lr_pr
        A[2, 4] = 0

        A[3, 0] = Nb_pr
        A[3, 1] = 0
        A[3, 2] = Np_pr
        A[3, 3] = Nr_pr
        A[3, 4] = 1

        A[4, 0] = 0
        A[4, 1] = 0
        A[4, 2] = 0
        A[4, 3] = 0
        A[4, 4] = 0


        # Populating the B matrix
        B = np.zeros((5, 2))
        B[0, 0] = Yda / U0
        B[0, 1] = Ydr / U0
        B[1, 0] = 0
        B[1, 1] = 0
        B[2, 0] = Lda_pr
        B[2, 1] = Ldr_pr
        B[3, 0] = Nda_pr
        B[3, 1] = Ndr_pr
        B[4, 0] = 0
        B[4, 1] = 0

        # Populating the C and D matrices
        C = np.eye(4)  # Identity matrix
        D = np.zeros((4, 2))  # Zero matrix

        #Performing Matrix Multiplication
        latDirStatesDot[0:4] = np.matmul(A, latDirStates[0:4]) + np.matmul(B, latDirCntrl)
        
        #Converting from Imperial back to SI units
        latDirStatesDot[0] = latDirStatesDot[0] # state units are rads (no change)
        latDirStatesDot[1] = latDirStatesDot[1] # state units are rads (no change)
        latDirStatesDot[2] = latDirStatesDot[2] # state units are rad/s (no change)
        latDirStatesDot[3] = latDirStatesDot[3] # state units are rad/s (no change)
        latDirStatesDot[4] = latDirStatesDot[4] # state units are rads (no change)

        #Extending to non perturbation states (derivatives on non perturbed parts are 0 so they match!)
        latDirStatesDot[5:9] = latDirStatesDot[0:4]

        return latDirStatesDot

    def setSpeed(self,u, v, w) -> None:
        """Actual Full Vehicle Speed [m/s]"""
        Speed = np.sqrt(u**2 + v**2 + w**2)
        self.Speed = Speed
    
    def getSpeed(self) -> float:
        return self.Speed

        

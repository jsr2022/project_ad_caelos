import numpy as np
import sys as sys

def phiMat(phi):
    """
    Function Description: Phi Matrix of (1) Euler Angle Direction Cosine Matrix
    Units: Radians
    Input: int, double, float, [1 x 1]
    Output: np.array [3, 3]

    Usage example(s):
    phiMatrix = phiMat(phi) 
    phiMatrix = phiMat(np.pi/2)

    Source(s):
    "Modern Flight Dynamics" by Daniel K. Schmidt, pg. 9
    """
    # Input argument check
    if __name__ == "__main__":
    
        if np.shape(phi) != 1:
            print("Input structure is not 1 x 1")
            exit(0)

    phiMatrix = np.array([[1, 0, 0], [0, np.cos(phi), np.sin(phi)], [0, -1*np.sin(phi), np.cos(phi)]])

    return phiMatrix

def thetaMat(theta):
    """
    Function Description: Theta Matrix of (2) Euler Angle Direction Cosine Matrix
    Units: Radians
    Input: int, double, float, [1 x 1]
    Output: np.array [3, 3]

    Usage example(s):
    thetaMatrix = thetaMat(theta) 
    thetaMatrix = thetaMat(np.pi/2)

    Source(s):
    "Modern Flight Dynamics" by Daniel K. Schmidt, pg. 9
    """
    # Input argument check
    if __name__ == "__main__":
    
        if np.shape(theta) != 1:
            print("Input structure is not 1 x 1")
            exit(0)

    thetaMatrix = np.array([[np.cos(theta), 0, -1*np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]])

    return thetaMatrix

def psiMat(psi):
    """
    Function Description: Psi Matrix of (3) Euler Angle Direction Cosine Matrix
    Units: Radians
    Input: int, double, float, [1 x 1]
    Output: np.array [3, 3]

    Usage example(s):
    psiMatrix = psiMat(psi) 
    psiMatrix = psiMat(np.pi/2)

    Source(s):
    "Modern Flight Dynamics" by Daniel K. Schmidt, pg. 9
    """
    # Input argument check
    if __name__ == "__main__":
    
        if np.shape(psi) != 1:
            print("Input structure is not 1 x 1")
            exit(0)

    psiMatrix = np.array([[np.cos(psi), np.sin(psi), 0], [-1*np.sin(psi), np.cos(psi), 0], [0, 0, 1]])

    return psiMatrix
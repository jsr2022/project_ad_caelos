from adcaelos.utilities.rotations.euler import Euler
import numpy as np

# Executes script
if __name__ == "__main__":

    phi = np.deg2rad(30)
    theta = np.deg2rad(45)
    psi = np.deg2rad(60)
    phiMatrix   = Euler.phiMat(phi)
    thetaMatrix = Euler.thetaMat(theta)
    psiMatrix   = Euler.psiMat(psi)

    euler123Matrix = Euler.euler123(phi, theta, psi)
    
    print("phiMatrix")
    print(phiMatrix)
    print("thetaMatrix")
    print(thetaMatrix)
    print("psiMatrix")
    print(psiMatrix)
    print("Euler123 Matrix")
    print(euler123Matrix)

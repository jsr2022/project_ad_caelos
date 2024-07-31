import adcaelos.rotation.euler 
import numpy as np

# Executes script
if __name__ == "__main__":

    phi = np.deg2rad(30)
    theta = np.deg2rad(45)
    psi = np.deg2rad(60)
    phiMatrix   = adcaelos.rotation.euler.phiMat(phi)
    thetaMatrix = adcaelos.rotation.euler.thetaMat(theta)
    psiMatrix   = adcaelos.rotation.euler.psiMat(psi)

    euler123Matrix = adcaelos.rotation.euler.euler123(phi, theta, psi)
    
    print("phiMatrix")
    print(phiMatrix)
    print("thetaMatrix")
    print(thetaMatrix)
    print("psiMatrix")
    print(psiMatrix)
    print("Euler123 Matrix")
    print(euler123Matrix)

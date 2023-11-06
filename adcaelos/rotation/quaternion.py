from numpy import shape, zeros
from sys import exit

def quatconjugate(q_in):
    """
    Function Description: quatconjugate.py computes the conjugate of a quaternion, or array of quaternions, defined as a N x 4 numpy array

    Usage example: 
    q_in = np.array([[0, 1, 0, 0],[0, 0, 1, 0]])
    q_conj = quatconjugate(q_in)
    
    Source: "Quaternion kinematics for the error-state Kalman filter" by Joan Sola, pg. 8 (https://arxiv.org/pdf/1711.02508.pdf)

    Author: Michael Higgins
    Created: 2023-Nov-5
    """

    # Input argument check
    if __name__ == "__main__":
        
        if shape(q_in)[1] != 4:
            print("Input structure is not N x 4")
            exit(0)

        if shape(q_in.ndim)[1] != 2:
            print("Input structure is not two-dimensional")
            exit(0)

    size_q_in = shape(q_in)[0]

    q_conj = zeros((size_q_in,4))

    q_conj[:,0] = q_in[:,0]
    q_conj[:,1:3] = -q_in[:,1:3]

    return q_conj
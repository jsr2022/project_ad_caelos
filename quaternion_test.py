import adcaelos.rotation.quaternion
import numpy as np

# Executes script
if __name__ == "__main__":

    q_in = np.array([[0, 1, 0, 0],[0, 0, 1, 0]])
    q_conj = adcaelos.rotation.quaternion.quatconjugate(q_in)

    print(q_conj)
#testSimulation.py
import numpy as np
from adcaelos.components.container_component import Container_Component
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.logic_component import Logic_Component
from adcaelos.components.dynamics.spring_mass_damper import SpringMassDamper
from adcaelos.schedulers.scheduler import Scheduler
from adcaelos.integrators.integrator_enums import Integrator_Enums

print("=== Spring Mass Damper Simulation Test ===")

# Create SpringMassDamper with initial state and control
stateNames = ["position", "velocity"]
initial_state = np.array([1.0, 0.1])  # position=1m, velocity=0.1m/s
initial_control = np.array([0.0])     # zero external force

smd = SpringMassDamper(
    stateNames=stateNames,
    initial_state=initial_state,
    initial_control=initial_control,
    integrator_type=Integrator_Enums.RK4,
    frequency=100,
    next_time=0.0,
    name="Spring_Mass_Damper",
    mass=1.0,
    spring_constant=1.0,
    damping_constant=0.5
)
print("Created Truth Physics Spring Mass Damper")
# Print(f"Initial condition: {smd.getCurrState()})
# print(f"Initial control: {smd.getCurrCntrl()}")

# Create a dummy Logic_Component
logic = Logic_Component(frequency=50, name="Dummy_Logic")
print(f"Logic_Component created: {logic.get_name()}")

# Create Container_Component
container = Container_Component(
    a_Logic_Component=logic,
    a_Truth_Component=smd,
    Time_Varying_Components=[],
    name="SMD_Container"
)
print("==================THE CONTAINER==================")
print(container)

# Create Scheduler with valid end time (2.0 seconds)
scheduler = Scheduler(
    container_components=[container],
    global_sim_start_time=0.0,
    global_sim_end_time=20.0,
    round2Decimals=10
)
print(f"Scheduler created with end time: {scheduler.global_sim_end_time} [s]")

# Print state before simulation
print(f"\n--- State before simulation ---")
print(f"Time: {smd.get_time():.3f}s")
print(f"State: {smd.getCurrState()}")
print(f"Control: {smd.getCurrCntrl()}")

# Run simulation
print("\n--- Running simulation ---")
scheduler.run_simulation(None)

# Print state after simulation
print(f"\n--- State after simulation ---")
print(f"Time: {smd.get_time():.3f}s")
print(f"State: {smd.getCurrState()}")
print(f"Control: {smd.getCurrCntrl()}")

print("\n=== Simulation Complete ===")

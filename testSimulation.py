#testSimulation.py
from adcaelos.components.base_component import Base_Component
from adcaelos.components.container_component import Container_Component
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.logic_component import Logic_Component
from adcaelos.components.dynamics.simple_aircraft import Simple_Aircraft

from adcaelos.atmosphere.atmosphere_models import Atmosphere_Models
altitude_m = 15000
print(Atmosphere_Models.simple1976EarthAtmosphere(altitude_m))

print("Printing Test Components")
testBase_Component            = Base_Component()
testTime_Varying_Component1   = Time_Varying_Component(name="1st Time Varying Component")
testTime_Varying_Component2   = Time_Varying_Component(name="2nd Time Varying Component")
stateNames = ["x_pos", "y_pos", "x_vel", "y_vel"]
#testTruth_Component           = Truth_Component(stateNames)
testLogic_Component           = Logic_Component()
#testContainer_Component       = Container_Component(testLogic_Component, testTruth_Component, [testTime_Varying_Component1, testTime_Varying_Component2])

testSimple_Aircraft           = Simple_Aircraft(stateNames)
testContainer_Simple_Aircraft = Container_Component(testLogic_Component, testSimple_Aircraft, [testTime_Varying_Component1, testTime_Varying_Component2], name="Simple Aircraft Container")


print(testBase_Component)
print("")
print(testTime_Varying_Component1)
print("")
print(testTime_Varying_Component2)
print("")
#print(testTruth_Component)
print("")
print(testLogic_Component)
print("")
# print("CONTAINER ONE")
# print(testContainer_Component)
print("")
print("AIRCRAFT ONE")
print(testContainer_Simple_Aircraft)


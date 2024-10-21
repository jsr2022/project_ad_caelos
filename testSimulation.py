#testSimulation.py
from adcaelos.components.base_component import Base_Component
from adcaelos.components.container_component import Container_Component
from adcaelos.components.time_varying_component import Time_Varying_Component
from adcaelos.components.truth_component import Truth_Component
from adcaelos.components.logic_component import Logic_Component


testBase_Component          = Base_Component()
testTime_Varying_Component1 = Time_Varying_Component(name="1st Time Varying Component")
testTime_Varying_Component2 = Time_Varying_Component(name="2nd Time Varying Component")
aa = dict()
bb = dict()
testTruth_Component        = Truth_Component(aa, bb)
testLogic_Component        = Logic_Component()
testContainer_Component    = Container_Component(testLogic_Component, testTruth_Component, [testTime_Varying_Component1, testTime_Varying_Component2])

print(testBase_Component)
print("")
print(testTime_Varying_Component1)
print("")
print(testTime_Varying_Component2)
print("")
print(testTruth_Component)
print("")
print(testLogic_Component)
print("")
print(testContainer_Component)
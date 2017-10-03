from physicalInterface import SimPhysicalInterface
from environmentSimulator import EnvironmentSimulator

a = SimPhysicalInterface()
a.forward()

b = EnvironmentSimulator()
b.generate(4, 4)
print(b.text_map())

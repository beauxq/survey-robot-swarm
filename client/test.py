from physicalInterface import SimPhysicalInterface
from environmentSimulator import EnvironmentSimulator

a = SimPhysicalInterface()
print(a.env.text_map())
a.forward()
a.forward()
a.rotate_left()
a.forward()
a.forward()

"""
b = EnvironmentSimulator()
b.generate(4, 4)
print(b.text_map())
"""

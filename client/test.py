from physicalInterface import SimPhysicalInterface
from environmentSimulator import EnvironmentSimulator

a = SimPhysicalInterface()
print(a.env.text_map())
a.forward()
print("read_sensor:", a.read_sensor())
a.forward()
print("read_sensor:", a.read_sensor())
a.rotate_left()
a.forward()
print("read_sensor:", a.read_sensor())
a.forward()
print("read_sensor:", a.read_sensor())

"""
b = EnvironmentSimulator()
b.generate(4, 4)
print(b.text_map())
"""

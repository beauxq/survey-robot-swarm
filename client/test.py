from physicalInterface import SimPhysicalInterface
from environmentSimulator import EnvironmentSimulator


def test_sim_physical_interface():
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


def test_environment_simulator():
    b = EnvironmentSimulator()
    b.generate(4, 4)
    print(b.text_map())


def main():
    test_sim_physical_interface()

if __name__ == "__main__":
    main()

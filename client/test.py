from physicalInterface import SimPhysicalInterface
from environmentSimulator import EnvironmentSimulator
from dataRepository import DataRepository
from utils import Coordinate, COORDINATE_CHANGE, Knowledge


def test_sim_physical_interface():
    a = SimPhysicalInterface(10, 10)
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


def test_data_repository():
    width = 10
    height = 10
    a = SimPhysicalInterface(width, height)
    d = DataRepository(width, height)

    print(a.env.text_map())

    # visit current space
    d.set_objective(a.position, a.read_sensor())
    # check obstacles
    for direction in COORDINATE_CHANGE:
        looking_at = a.position + COORDINATE_CHANGE[direction]
        if not d.out_of_bounds(looking_at):
            d.set_obstacle(looking_at, Knowledge.YES if a.see_obstacles(direction) else Knowledge.NO)

    c = d.find_target(a.position, Coordinate(0, 0))
    print(c)

    p = d.find_path(a.position, c)
    print(p)

    print(d.text_map(a.position, a.facing))


def main():
    # test_sim_physical_interface()
    # test_environment_simulator()
    test_data_repository()


if __name__ == "__main__":
    main()

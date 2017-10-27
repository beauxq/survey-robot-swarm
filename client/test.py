from physicalInterface import SimPhysicalInterface, IPhysicalInterface
from environmentSimulator import EnvironmentSimulator
from dataRepository import DataRepository
from utils import Coordinate, COORDINATE_CHANGE, Knowledge

import random


def test_sim_physical_interface():
    a = SimPhysicalInterface(10, 10, random.randint(76, 76000))
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


def visit(physical_interface: IPhysicalInterface, d: DataRepository):
    # visit current space
    d.set_objective(physical_interface.position, physical_interface.read_sensor())
    # check obstacles
    for direction in COORDINATE_CHANGE:
        looking_at = physical_interface.position + COORDINATE_CHANGE[direction]
        if not d.out_of_bounds(looking_at):
            d.set_obstacle(looking_at, Knowledge.YES if physical_interface.see_obstacles(direction) else Knowledge.NO)


def test_data_repository():
    width = 10
    height = 10
    seed = random.randint(76, 76000)
    print("seed:", seed)
    a = SimPhysicalInterface(width, height, seed)
    d = DataRepository(width, height)

    print(a.env.text_map())

    visit(a, d)

    c = d.find_target(a.position, Coordinate(0, 0))
    while c != Coordinate(0, 0):
        print("target:", c)

        p = d.find_path(a.position, c)
        print("path:", p)
        if len(p) > 0:
            a.turn(p[0])
            a.forward()
            visit(a, d)

        print(d.text_map(a.position, a.facing))
        input()
        c = d.find_target(a.position, Coordinate(0, 0))


def main():
    # test_sim_physical_interface()
    # test_environment_simulator()
    test_data_repository()


if __name__ == "__main__":
    main()

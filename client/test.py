from time import sleep

from physicalInterface import SimPhysicalInterface, IPhysicalInterface
from environmentSimulator import EnvironmentSimulator
from dataRepository import DataRepository
from comm import Message, CommunicationManager
from utils import Coordinate, COORDINATE_CHANGE, Knowledge, get_jenks_breaks

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


def test_message():
    print(Message.coord_str(Coordinate(536, 0)))
    assert Message.coord_str(Coordinate(536, 0)) == "536 0 "
    print("passed Message.coord_str")

    Message.set_my_robot_id(1)

    m = Message()
    m.add_objective(Coordinate(3, 5), 2.0)
    print(m.get_data())
    assert m.get_data() == Message.BEGIN + "1 1 j3 5 2.0k" + Message.END
    print("passed add_objective")

    m._cursor = 10
    ov = m.extract_objective_value()
    print(ov)
    assert ov == 2.0
    print("passed extract_objective_value")

    m = Message()
    m.add_obstacle(Coordinate(0, 6), Knowledge.YES)
    print(m.get_data())
    assert m.get_data() == Message.BEGIN + "1 2 s0 6 yt" + Message.END
    print("passed add_obstacle")

    m._cursor = 6
    co = m.extract_coordinates()
    print(co)
    assert co == Coordinate(0, 6)
    print("passed extract coordinate")

    d = DataRepository(10, 10)
    m.add_objective(Coordinate(6, 0), 7.0)
    m.handle(d)
    obs = d.get_obstacle(Coordinate(0, 6))
    obj = d.get_objective(Coordinate(6, 0))
    print(obs, obj)
    assert obs == Knowledge.YES
    assert obj == 7.0
    print("passed handle")


def test_comm():
    d = DataRepository(10, 10)

    # change broadcast address for testing
    CommunicationManager.DEFAULT_BROADCAST = "127.255.255.255"

    c = CommunicationManager(d, 1, 1)

    c.start_listen_thread()

    c.send_message(Message())
    sleep(5)
    c.send_message(Message())


def test_jenks():
    a = [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3,
         7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 28]
    print(get_jenks_breaks(a, 2))


def main():
    # test_sim_physical_interface()
    # test_environment_simulator()
    # test_data_repository()
    # test_message()
    # test_comm()
    test_jenks()


if __name__ == "__main__":
    main()

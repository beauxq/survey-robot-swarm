from robot import Robot
from utils import Coordinate
from threading import Thread

import sys


class DataGatherThread(Thread):
    def __init__(self, robot: Robot):
        Thread.__init__(self)
        self.robot = robot
        self.result = None

    def run(self):
        self.result = self.robot.go()


DEMO_OPTIONS = {
    "0": {
        "width": 20,
        "height": 15,
        "home_x": 0,
        "home_y": 0,
        # 87 good for presentation
        "seed": 87,
        "robot_id": 1,
        "robot_count": 1
    },
    "1": {
        "width": 20,
        "height": 15,
        "home_x": 0,
        "home_y": 0,
        "seed": 87,
        "robot_id": 1,
        "robot_count": 2
    },
    "2": {
        "width": 20,
        "height": 15,
        "home_x": 19,
        "home_y": 14,
        "seed": 87,
        # 86 bl trp
        "robot_id": 2,
        "robot_count": 2
    }
}


def get_configuration() -> dict:
    with open("config.txt") as file:

        # defaults
        options = {
            "width": 10,
            "height": 10,
            "home_x": 0,
            "home_y": 0,
            "seed": 76,
            "robot_id": 1,
            "robot_count": 2
        }

        # read non-defaults from configuration file
        for line in file:
            words = line.split(" ")
            if len(words) == 3 and words[1] == "=":
                try:
                    options[words[0]] = int(words[2])
                except ValueError:
                    print("warning: discarding non-integer found for a configuration value -", line)

    return options


def create_robot_with_options(options: dict) -> Robot:
    return Robot(options["width"],
                 options["height"],
                 Coordinate(options["home_x"], options["home_y"]),
                 options["seed"],
                 options["robot_id"],
                 options["robot_count"])


def one_set(seed: int) -> tuple:
    """
    :param seed:
    :return: lower left alone time, upper right alone time, lower left together time, upper right together time
    """
    options2 = get_configuration()

    # 1 in lower left
    options2["home_x"] = 0
    options2["home_y"] = 0
    options2["seed"] = seed
    options2["robot_id"] = 1
    options2["robot_count"] = 1
    robot = create_robot_with_options(options2)
    robot.communication.broadcast = "127.255.255.255"
    result_ll = robot.go()

    # 1 in upper right
    options2["home_x"] = options2["width"] - 1
    options2["home_y"] = options2["height"] - 1
    robot = create_robot_with_options(options2)
    robot.communication.broadcast = "127.255.255.255"
    result_ur = robot.go()

    # 1 in each corner
    options2["robot_count"] = 2
    options1 = options2.copy()
    options2["robot_id"] = 2
    options1["home_x"] = 0
    options1["home_y"] = 0

    # create them (changing ports) and run them, collect data
    robot1 = create_robot_with_options(options1)
    robot1.communication.send_port = 7677
    robot1.communication.broadcast = "127.255.255.255"
    robot2 = create_robot_with_options(options2)
    robot2.communication.listen_port = 7677
    robot2.communication.broadcast = "127.255.255.255"

    thread1 = DataGatherThread(robot1)
    thread2 = DataGatherThread(robot2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    return result_ll, result_ur, thread1.result, thread2.result


def data_gather_sequence():
    lower_left_alone_results = []
    upper_right_alone_results = []
    lower_left_together_results = []
    upper_right_together_results = []

    for seed in range(10000):
        results = one_set(seed)
        lower_left_alone_results.append(results[0])
        upper_right_alone_results.append(results[1])
        lower_left_together_results.append(results[2])
        upper_right_together_results.append(results[3])

        print("lla", lower_left_alone_results)
        print("ura", upper_right_alone_results)
        print("llt", lower_left_together_results)
        print("urt", upper_right_together_results)


def run_a_robot(demo):
    """ not data gathering """
    options = get_configuration()
    if demo:
        options = DEMO_OPTIONS[sys.argv[1]]
    robot = create_robot_with_options(options)
    # for single computer demo
    if demo:
        if sys.argv[1] == "1":
            robot.communication.send_port = 7677
        else:  # should be "2"
            robot.communication.listen_port = 7677
        robot.communication.broadcast = "127.255.255.255"
    print("done time:", robot.go())


def main():
    # 2 robot on 1 computer demo
    demo = (len(sys.argv) > 1 and (sys.argv[1] == "1" or sys.argv[1] == "2"))
    if len(sys.argv) > 1 and sys.argv[1] == "d":
        # one_set(78)
        data_gather_sequence()
    else:
        run_a_robot(demo)


if __name__ == "__main__":
    main()

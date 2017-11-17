from robot import Robot
from utils import Coordinate

import sys


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


def one_set(seed: int):
    options2 = get_configuration()

    # 1 in lower left
    options2["home_x"] = 0
    options2["home_y"] = 0
    options2["seed"] = seed
    options2["robot_id"] = 1
    options2["robot_count"] = 1
    robot = create_robot_with_options(options2)
    result = robot.go()
    # TODO: store information

    # 1 in upper right
    options2["home_x"] = options2["width"] - 1
    options2["home_y"] = options2["height"] - 1
    robot = create_robot_with_options(options2)
    result = robot.go()
    # TODO: store information

    # 1 in each corner
    options2["robot_count"] = 2
    options1 = options2.copy()
    options2["robot_id"] = 2
    options1["home_x"] = 0
    options1["home_y"] = 0

    # TODO: create them (changing ports) and run them, collect data


def main():
    # 2 robot on 1 computer demo
    demo = (len(sys.argv) > 1)
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
        robot.communication.__class__.BROADCAST = "127.255.255.255"
    print("done time:", robot.go())


if __name__ == "__main__":
    main()

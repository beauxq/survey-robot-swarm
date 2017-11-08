from robot import Robot
from utils import Coordinate

import sys


DEMO_OPTIONS = {
    "1": {
        "width": 20,
        "height": 15,
        "home_x": 0,
        "home_y": 0,
        "seed": 82,
        # seed 79 debug message failure 1, 1 to 2
        "robot_id": 1,
        "robot_count": 2
    },
    "2": {
        "width": 20,
        "height": 15,
        "home_x": 19,
        "home_y": 14,
        "seed": 82,
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


def main():
    # 2 robot on 1 computer demo
    demo = (len(sys.argv) > 1)
    options = get_configuration()
    if demo:
        options = DEMO_OPTIONS[sys.argv[1]]

    robot = Robot(options["width"],
                  options["height"],
                  Coordinate(options["home_x"], options["home_y"]),
                  options["seed"],
                  options["robot_id"],
                  options["robot_count"])
    # for single computer demo
    if demo:
        if sys.argv[1] == "1":
            robot.communication.__class__.SEND_PORT = 7677
        else:  # should be "2"
            robot.communication.__class__.LISTEN_PORT = 7677
        robot.communication.__class__.BROADCAST = "127.255.255.255"
    robot.go()


if __name__ == "__main__":
    main()

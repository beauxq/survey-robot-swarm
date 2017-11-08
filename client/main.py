from robot import Robot
from utils import Coordinate


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
    options = get_configuration()

    robot = Robot(options["width"],
                  options["height"],
                  Coordinate(options["home_x"], options["home_y"]),
                  options["seed"],
                  options["robot_id"],
                  options["robot_count"])
    robot.go()


if __name__ == "__main__":
    main()

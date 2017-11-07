from robot import Robot
from utils import Coordinate

import sys


ARG_LIST = "width height home_x home_y seed robot_id"


def main():
    width = 10
    height = 10
    home_x = 0
    home_y = 0
    seed = 76
    robot_id = 1
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        home_x = int(sys.argv[3])
        home_y = int(sys.argv[4])
        seed = int(sys.argv[5])
        robot_id = int(sys.argv[6])
    except IndexError:
        print("need 6 arguments:", ARG_LIST)
        exit(1)
    except ValueError:
        print("all arguments should be integers:", ARG_LIST)
        exit(1)

    robot = Robot(width, height, Coordinate(home_x, home_y), seed, robot_id)
    robot.go()


if __name__ == "__main__":
    main()

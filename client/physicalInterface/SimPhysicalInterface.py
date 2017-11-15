from physicalInterface import IPhysicalInterface
from environmentSimulator import EnvironmentSimulator
from utils import Coordinate, COORDINATE_CHANGE, Direction

from time import sleep


class SimPhysicalInterface(IPhysicalInterface):
    TURN_TIME = .01
    FORWARD_TIME = .03
    OBJECTIVE_TIME = .001
    OBSTACLE_TIME = .00025  # seeing all obstacles can be same as 1 objective

    def __init__(self, width: int, height: int, seed: int):
        super().__init__()
        self.env = EnvironmentSimulator()
        self.env.generate(width, height, seed)
        self.position = Coordinate(0, 0)
        self.facing = Direction.EAST

    def forward(self) -> float:
        """ :returns time taken """
        target_coordinate = self.position + COORDINATE_CHANGE[self.facing]
        if self.env.get(target_coordinate).obstacle:
            print("WARNING: attempted to move into obstacle - failed")
            return 0

        sleep(SimPhysicalInterface.FORWARD_TIME)

        self.position = target_coordinate
        # print("moved forward to", str(self.position))

        return SimPhysicalInterface.FORWARD_TIME

    def rotate_left(self) -> float:
        """ :returns time taken """
        self.facing = Direction((self.facing + 1) % 4)
        # print("turned left, now facing", self.facing)

        sleep(SimPhysicalInterface.TURN_TIME)
        return SimPhysicalInterface.TURN_TIME

    def rotate_right(self) -> float:
        """ :returns time taken """
        self.facing = Direction((self.facing - 1) % 4)
        # print("turned right, now facing", self.facing)

        sleep(SimPhysicalInterface.TURN_TIME)
        return SimPhysicalInterface.TURN_TIME

    def turn(self, desired_direction: Direction) -> float:
        """ :returns time taken """
        time_to_return = 0
        # print("about to turn: " + str(desired_direction))
        if self.facing == desired_direction:
            pass  # don't evaluate elif expressions
        # not already facing the correct direction
        elif int(desired_direction) == (int(self.facing) + 1) % int(Direction.COUNT):
            time_to_return += self.rotate_left()
        elif (int(desired_direction) + 1) % int(Direction.COUNT) == int(self.facing):
            time_to_return += self.rotate_right()
        else:  # 180
            # TODO:might there be a reason to alternate 2 lefts and 2 rights?
            time_to_return += self.rotate_left()
            time_to_return += self.rotate_left()
        # print("just turned: " + str(self.facing))

        return time_to_return

    def read_sensor(self) -> (int, float):
        """ :returns sensor reading, time taken """
        sleep(SimPhysicalInterface.OBJECTIVE_TIME)
        return self.env.get(self.position).objective_value, SimPhysicalInterface.OBJECTIVE_TIME

    def see_obstacles(self, direction: Direction) -> (bool, float):
        """ :returns obstacle in given direction, time taken """
        sleep(SimPhysicalInterface.OBSTACLE_TIME)
        return self.env.get(self.position + COORDINATE_CHANGE[direction]).obstacle, SimPhysicalInterface.OBSTACLE_TIME

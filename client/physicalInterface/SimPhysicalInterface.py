from physicalInterface import IPhysicalInterface
from environmentSimulator import EnvironmentSimulator
from utils import Coordinate, COORDINATE_CHANGE, Direction


class SimPhysicalInterface(IPhysicalInterface):
    def __init__(self, width, height):
        super().__init__()
        self.env = EnvironmentSimulator()
        self.env.generate(width, height)
        self.position = Coordinate(0, 0)
        self.facing = Direction.EAST

    def forward(self):
        target_coordinate = self.position + COORDINATE_CHANGE[self.facing]
        if self.env.get(target_coordinate).obstacle:
            print("attempted to move into obstacle - failed")
            return

        self.position = target_coordinate
        print("moved forward to", str(self.position))

    def rotate_left(self):
        self.facing = Direction((self.facing + 1) % 4)
        print("turned left, now facing", self.facing)

    def rotate_right(self):
        self.facing = Direction((self.facing - 1) % 4)
        print("turned right, now facing", self.facing)

    def turn(self, desired_direction: Direction):
        print("about to turn: " + str(desired_direction))
        if self.facing == desired_direction:
            pass  # don't evaluate elif expressions
        # not already facing the correct direction
        elif int(desired_direction) == (int(self.facing) + 1) % int(Direction.COUNT):
            self.rotate_left()
        elif (int(desired_direction) + 1) % int(Direction.COUNT) == int(self.facing):
            self.rotate_right()
        else:  # 180
            # TODO:might there be a reason to alternate 2 lefts and 2 rights?
            self.rotate_left()
            self.rotate_left()
        print("just turned: " + str(self.facing))

    def read_sensor(self) -> int:
        return self.env.get(self.position).objective_value

    def see_obstacles(self, direction: Direction) -> bool:
        return self.env.get(self.position + COORDINATE_CHANGE[direction]).obstacle

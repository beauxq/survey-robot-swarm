from physicalInterface import IPhysicalInterface
from environmentSimulator import EnvironmentSimulator
from utils import Coordinate, COORDINATE_CHANGE, Direction

SIZE = 10


class SimPhysicalInterface(IPhysicalInterface):
    def __init__(self):
        super().__init__()
        self.env = EnvironmentSimulator()
        self.env.generate(SIZE, SIZE)
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

    def read_sensor(self) -> int:
        return self.env.get(self.position).objective_value

    def see_obstacles(self, n: Direction) -> bool:
        return False  # TODO: implement see_obstacles

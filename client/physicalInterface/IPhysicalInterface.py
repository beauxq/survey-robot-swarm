from utils import Direction, Coordinate


class IPhysicalInterface:
    def __init__(self):
        self.position = Coordinate()
        self.facing = Direction.EAST

    def rotate_left(self):
        raise NotImplementedError

    def rotate_right(self):
        raise NotImplementedError

    def turn(self, direction: Direction):
        raise NotImplementedError

    def forward(self):
        raise NotImplementedError

    def see_obstacles(self, n: Direction) -> bool:
        raise NotImplementedError

    def read_sensor(self) -> int:
        raise NotImplementedError

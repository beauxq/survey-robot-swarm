from utils import Direction


class IPhysicalInterface:
    def __init__(self):
        pass

    def rotate_left(self):
        raise NotImplementedError

    def rotate_right(self):
        raise NotImplementedError

    def forward(self):
        raise NotImplementedError

    def see_obstacles(self, n: Direction) -> bool:
        raise NotImplementedError

    def read_sensor(self) -> int:
        raise NotImplementedError

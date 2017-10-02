from physicalInterface.IPhysicalInterface import IPhysicalInterface
from utils import Direction


class SimPhysicalInterface(IPhysicalInterface):
    def __init__(self):
        super().__init__()
        self.a = 0

    def forward(self):
        self.a += 1
        print("moved forward")

    def rotate_left(self):
        self.a += 1
        print("turned left")

    def read_sensor(self) -> int:
        return self.a

    def see_obstacles(self, n: Direction) -> bool:
        return False

    def rotate_right(self):
        self.a += 1
        print("turned right")

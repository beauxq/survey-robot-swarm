from physicalInterface import IPhysicalInterface
from utils import Direction
from environmentSimulator import EnvironmentSimulator


class SimPhysicalInterface(IPhysicalInterface):
    def __init__(self):
        super().__init__()
        self.env = EnvironmentSimulator()
        self.env.generate()

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

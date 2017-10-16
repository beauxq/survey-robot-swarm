from environmentSimulator.GridSpace import GridSpace
from utils import Coordinate
import random


class EnvironmentSimulator:
    def __init__(self):
        self._grid = [[GridSpace()]]

    def generate(self, width, height, seed=None):
        random.seed(seed)
        self._grid = [[] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                self._grid[y].append(GridSpace(random.choice((True, False)), random.random()))

    def text_map(self) -> str:
        to_return = ""
        for row in self._grid:
            for space in row:
                if space.obstacle:
                    to_return += "X"
                else:
                    to_return += str(int(space.objective_value * 10))
                to_return += " "
            to_return += "\n"
        return to_return

    def get(self, x_or_coordinate, y=None):
        i0, i1 = Coordinate.to_indexes(len(self._grid), x_or_coordinate, y)
        return self._grid[i0][i1]

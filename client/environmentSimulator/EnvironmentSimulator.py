from environmentSimulator.GridSpace import GridSpace
import random


class EnvironmentSimulator:
    def __init__(self):
        pass
        self._grid = []

    def generate(self, width, height, seed=None):
        random.seed(seed)
        self._grid = [[] for y in range(height)]
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
        if y is None:
            # 1st argument is Coordinate
            x, y = x_or_coordinate.x, x_or_coordinate.y
        else:
            x = x_or_coordinate
        return self._grid[len(self._grid) - (y+1)][x]

from environmentSimulator.GridSpace import GridSpace
import random


class EnvironmentSimulator:
    def __init__(self):
        pass
        self.grid = []

    def generate(self, width, height, seed=None):
        random.seed(seed)
        self.grid = [[] for y in range(height)]
        for y in range(height):
            for x in range(width):
                self.grid[y].append(GridSpace(random.choice((True, False)), random.random()))

    def text_map(self) -> str:
        to_return = ""
        for row in self.grid:
            for space in row:
                if space.obstacle:
                    to_return += "X"
                else:
                    to_return += str(int(space.objective_value * 10))
                to_return += " "
            to_return += "\n"
        return to_return

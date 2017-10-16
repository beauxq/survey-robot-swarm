from utils import Knowledge


class GridSpace:
    def __init__(self):
        self.obstacle_here = Knowledge.UNKNOWN
        self.objective_value = Knowledge.UNKNOWN

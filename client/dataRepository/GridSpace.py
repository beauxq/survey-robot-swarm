from utils import Knowledge


class GridSpace:
    def __init__(self):
        self.obstacle_here = Knowledge.UNKNOWN
        self.objective_value = Knowledge.UNKNOWN
        self.occupied = False  # one of the robots is moving into or out of this space

    def text_map_repr(self) -> str:
        if self.obstacle_here == Knowledge.YES:
            return "X"
        if self.obstacle_here == Knowledge.UNKNOWN:
            return "?"
        # known no obstacle
        if self.occupied:
            return "R"
        if self.objective_value == Knowledge.UNKNOWN:
            return "."
        # objective known
        return "O"

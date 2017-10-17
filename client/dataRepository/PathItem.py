from utils import Coordinate


class PathItem:
    """
    used whenever a coordinate needs to be stored with a number
    compares on the cost number
    """
    def __init__(self, coordinate: Coordinate, cost: int):
        self.coordinate = coordinate
        self.cost = cost

    def __lt__(self, other) -> bool:
        return self.cost < other.cost

    def __eq__(self, other) -> bool:
        return self.cost == other.cost

    def __repr__(self) -> str:
        return "(" + str(self.coordinate) + ", " + str(self.cost) + ")"

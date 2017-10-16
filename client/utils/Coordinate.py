class Coordinate:
    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.x * 17 + self.y  # TODO: find a good way to eliminate magic number

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    @staticmethod
    def to_indexes(height, x_or_coordinate, y=None) -> tuple:
        """convert cartesian coordinate to 2-dimensional list indexes"""
        if y is None:
            # 1st argument is Coordinate
            x, y = x_or_coordinate.x, x_or_coordinate.y
        else:
            x = x_or_coordinate
        return height - (y+1), x

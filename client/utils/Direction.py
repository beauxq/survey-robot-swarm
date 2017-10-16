from enum import IntEnum


class Direction(IntEnum):

    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3
    COUNT = 4

    @staticmethod
    def opposite(given):
        """ :returns the opposite direction from what is given """
        return (given + 2) % Direction.COUNT

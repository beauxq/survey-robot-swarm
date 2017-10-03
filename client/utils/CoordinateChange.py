from utils.Direction import Direction
from utils.Coordinate import Coordinate

# To get the next coordinate in a given direction, add this coordinate
COORDINATE_CHANGE = {
    Direction.EAST: Coordinate(1, 0),
    Direction.WEST: Coordinate(-1, 0),
    Direction.NORTH: Coordinate(0, 1),
    Direction.SOUTH: Coordinate(0, -1)
}

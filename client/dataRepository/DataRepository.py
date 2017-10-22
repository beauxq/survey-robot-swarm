from collections import deque, defaultdict
from heapq import heappop, heappush
from threading import Lock
import math

from dataRepository.GridSpace import GridSpace
from dataRepository.PathItem import PathItem
from utils import Coordinate, Knowledge, COORDINATE_CHANGE, Direction, static_vars


class DataRepository:
    TRAVEL_WEIGHT = 3  # preference for travel weight over distance from home
    STOP_BFS_THRESHOLD = 10  # stop bfs if costs are this much greater than current best

    def __init__(self, width: int, height: int):
        self._mutex = Lock()
        self._data = [[GridSpace()]]

        self.reset(width, height)

    def reset(self, width: int, height: int):
        self._mutex.acquire()
        self._data = [[] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                self._data[y].append(GridSpace())
        self._mutex.release()

    def _get(self, coordinate: Coordinate) -> GridSpace:
        i0, i1 = Coordinate.to_indexes(len(self._data), coordinate)
        return self._data[i0][i1]

    def set_obstacle(self, coordinate: Coordinate, value: Knowledge=Knowledge.YES):
        self._mutex.acquire()
        self._get(coordinate).obstacle_here = value
        self._mutex.release()

    def get_obstacle(self, coordinate: Coordinate) -> Knowledge:
        self._mutex.acquire()
        to_return = self._get(coordinate).obstacle_here
        self._mutex.release()
        return to_return

    def set_objective(self, coordinate: Coordinate, value=Knowledge.YES):
        self._mutex.acquire()
        self._get(coordinate).objective_value = value
        self._mutex.release()

    def get_objective(self, coordinate: Coordinate):
        self._mutex.acquire()
        to_return = self._get(coordinate).objective_value
        self._mutex.release()
        return to_return

    def set_occupied(self, coordinate: Coordinate, value: bool=True):
        self._mutex.acquire()
        self._get(coordinate).occupied = value
        self._mutex.release()

    def get_occupied(self, coordinate: Coordinate) -> bool:
        self._mutex.acquire()
        to_return = self._get(coordinate).occupied
        self._mutex.release()
        return to_return

    def out_of_bounds(self, coordinate: Coordinate) -> bool:
        """:returns whether coordinate is outside the grid"""
        # short circuit evaluation - index 0 isn't checked if len(self._data) is 0
        return (coordinate.x < 0 or
                coordinate.y < 0 or
                coordinate.y > len(self._data) - 1 or
                coordinate.x > len(self._data[0]))

    def _can_travel(self, target: Coordinate) -> bool:
        if self.out_of_bounds(target):
            return False
        target_space = self._get(target)
        if target_space.obstacle_here in (Knowledge.UNKNOWN, Knowledge.YES) or target_space.occupied:
            return False
        return True

    def find_target(self, start: Coordinate, home: Coordinate) -> Coordinate:
        """decide where the robot at current_coordinate will try to go"""
        print("find target from: " + str(start) + "  home: " + str(home))
        best_target = PathItem(home, math.inf)  # return home if there's no where else to go
        # breadth-first search for nodes to put in the heap
        path_queue = deque([PathItem(start, start.distance_to(home))])
        bfs_visited = defaultdict(bool)

        self._mutex.acquire()

        while len(path_queue):
            print("going through path_queue, current length: " + str(len(path_queue)))
            current = path_queue.popleft()
            print("popped: " + str(current))
            # if we don't have a reading for this space yet, it is candidate for best target
            if self._get(current.coordinate).objective_value == Knowledge.UNKNOWN:
                print("found unknown objective at: " + str(current.coordinate))
                if current.cost < best_target.cost:
                    best_target = current
            bfs_visited[current.coordinate] = True
            # look at all neighbors
            for direction in COORDINATE_CHANGE:
                this_neighbor = current.coordinate + COORDINATE_CHANGE[direction]
                print("looking " + str(direction) + " at: " + str(this_neighbor))
                print("can travel: " + str(self._can_travel(this_neighbor)))
                if self._can_travel(this_neighbor) and not bfs_visited[this_neighbor]:
                    print("can travel and not already visited: " + str(this_neighbor))
                    # calculate cost
                    distance_to_home_change = this_neighbor.distance_to(home) - current.coordinate.distance_to(home)
                    cost = current.cost + DataRepository.TRAVEL_WEIGHT + distance_to_home_change
                    if cost - DataRepository.STOP_BFS_THRESHOLD < best_target.cost:
                        path_queue.append(PathItem(this_neighbor, cost))

        self._mutex.release()

        return best_target.coordinate

    def find_path(self, start: Coordinate, target: Coordinate) -> list:
        """:returns a list of directions from start to target"""
        visited_in_this_search = set()
        direction_to_arrive_at = {start: None}
        bfs_queue = [PathItem(start, 0)]
        current = heappop(bfs_queue)

        while current.coordinate != target:
            visited_in_this_search.add(current.coordinate)

            for direction in COORDINATE_CHANGE:
                coordinate_checking = current.coordinate + COORDINATE_CHANGE[direction]
                if (self._can_travel(coordinate_checking) and coordinate_checking not in visited_in_this_search):
                    heappush(bfs_queue, PathItem(coordinate_checking, current.cost + 1))
                    direction_to_arrive_at[coordinate_checking] = direction

            current = heappop(bfs_queue)

        # now at target, build list of directions
        to_return = []
        current_coordinate = target
        while direction_to_arrive_at[current_coordinate] is not None:
            to_return.append(direction_to_arrive_at[current_coordinate])
            current_coordinate += COORDINATE_CHANGE[Direction.opposite(direction_to_arrive_at[current_coordinate])]

        return to_return

    @static_vars(ROBOT_SYMBOLS={
        Direction.NORTH: "^",
        Direction.SOUTH: "v",
        Direction.WEST: "<",
        Direction.EAST: ">"
    })
    def text_map(self, my_position: Coordinate=None, my_direction: Direction=None) -> str:
        my_position_indexes = None if my_position is None else Coordinate.to_indexes(len(self._data), my_position)

        to_return = ""
        for i1 in range(len(self._data)):
            for i2 in range(len(self._data[i1])):
                space = self._data[i1][i2]
                representation = self.text_map.ROBOT_SYMBOLS[my_direction] + " " if \
                    my_position_indexes is not None and my_position_indexes == (i1, i2) else \
                    space.text_map_repr() + " "
                to_return += representation
            # row complete
            to_return += "\n"
        return to_return

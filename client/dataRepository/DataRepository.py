from collections import deque, defaultdict
from threading import Lock
import math

from dataRepository.GridSpace import GridSpace
from dataRepository.PathItem import PathItem
from utils import Coordinate, Knowledge, COORDINATE_CHANGE


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

    def _can_travel(self, target: Coordinate) -> bool:
        # short circuit evaluation - index 0 isn't checked if len(self._data) is 0
        if target.x < 0 or target.y < 0 or target.y > len(self._data) - 1 or target.x > len(self._data[0]):
            return False
        target_space = self._get(target)
        if target_space.obstacle_here in (Knowledge.UNKNOWN, Knowledge.YES) or target_space.occupied:
            return False
        return True

    def find_target(self, start: Coordinate, home: Coordinate) -> Coordinate:
        """decide where the robot at current_coordinate will try to go"""
        best_target = PathItem(home, math.inf)
        # breadth-first search for nodes to put in the heap
        path_queue = deque([PathItem(start, start.distance_to(home))])
        bfs_visited = defaultdict(bool)

        self._mutex.acquire()

        while len(path_queue):
            current = path_queue.popleft()
            # if we don't have a reading for this space yet, it is candidate for best target
            if self._get(current.coordinate).objective_value == Knowledge.UNKNOWN:
                if current.cost < best_target.cost:
                    best_target = current
            bfs_visited[current.coordinate] = True
            # look at all neighbors
            for direction in COORDINATE_CHANGE:
                this_neighbor = current.coordinate + COORDINATE_CHANGE[direction]
                if self._can_travel(this_neighbor) and not bfs_visited[this_neighbor]:
                    # calculate cost
                    distance_to_home_change = this_neighbor.distance_to(home) - current.coordinate.distance_to(home)
                    cost = current.cost + DataRepository.TRAVEL_WEIGHT + distance_to_home_change
                    if cost - DataRepository.STOP_BFS_THRESHOLD < best_target.cost:
                        path_queue.append(PathItem(this_neighbor, cost))

        self._mutex.release()

        return best_target.coordinate

from dataRepository.GridSpace import GridSpace
from utils import Coordinate, Knowledge
from threading import Lock


class DataRepository:
    def __init__(self, width, height):
        self._mutex = Lock()
        self._data = [[GridSpace()]]

        self.reset(width, height)

    def reset(self, width, height):
        self._mutex.acquire()
        self._data = [[] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                self._data[y].append(GridSpace())
        self._mutex.release()

    def _get(self, x_or_coordinate, y=None) -> GridSpace:
        i0, i1 = Coordinate.to_indexes(len(self._data), x_or_coordinate, y)
        return self._data[i0][i1]

    def set_obstacle(self, x, y=None, value=Knowledge.YES):
        if type(y) == Knowledge:
            value = y
            y = None
        self._mutex.acquire()
        self._get(x, y).obstacle_here = value
        self._mutex.release()

    def get_obstacle(self, x, y=None) -> Knowledge:
        self._mutex.acquire()
        to_return = self._get(x, y).obstacle_here
        self._mutex.release()
        return to_return

    def set_objective(self, x, y=None, value=None):
        if type(x) == Coordinate and value is None:
            value = y
            y = None
        if value is None:
            value = Knowledge.YES
        self._mutex.acquire()
        self._get(x, y).objective_value = value
        self._mutex.release()

    def get_objective(self, x, y=None):
        self._mutex.acquire()
        to_return = self._get(x, y).objective_value
        self._mutex.release()
        return to_return

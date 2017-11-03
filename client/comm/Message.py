from dataRepository import DataRepository
from utils import Coordinate, Knowledge

from bidict import bidict  # pip install bidict


class Message:
    # protocol
    # if we want to make any of these more than one character, handle will need to be changed
    BEGIN = "\t"
    OBJECTIVE = "j"
    OBJECTIVE_END = "k"
    OBSTACLE = "s"
    OBSTACLE_END = "t"
    KNOWLEDGE = bidict({
        Knowledge.YES: "y",
        Knowledge.NO: "n",
        Knowledge.UNKNOWN: "u"
    })
    SEPARATOR = " "  # after each coordinate number
    END = "~"

    # this type needs to be able to be casted to str and back
    # Message.OBJECTIVE_TYPE(str(x))
    # and must not have OBJECTIVE_END in any str representation
    OBJECTIVE_TYPE = float

    def __init__(self, incoming: str=None):
        self._data = Message.BEGIN
        if incoming is not None:
            self._data = incoming

    @staticmethod
    def coord_str(coordinate: Coordinate) -> str:
        return str(coordinate.x) + Message.SEPARATOR + str(coordinate.y) + Message.SEPARATOR

    def extract_coordinates(self, cursor: int) -> (Coordinate, int):
        """ inverse of coord_str starting from index cursor
            :returns Coordinate and new cursor value """
        separator_index = self._data.index(Message.SEPARATOR, cursor)
        x = int(self._data[cursor:separator_index])
        cursor = separator_index + 1
        separator_index = self._data.index(Message.SEPARATOR, cursor)
        y = int(self._data[cursor:separator_index])
        cursor = separator_index + 1

        return Coordinate(x, y), cursor

    def extract_objective_value(self, cursor: int) -> (OBJECTIVE_TYPE, int):
        end = self._data.index(Message.OBJECTIVE_END, cursor)
        value = Message.OBJECTIVE_TYPE(self._data[cursor:end])
        return value, end

    def add_objective(self, position: Coordinate, value):
        self._data += Message.OBJECTIVE + Message.coord_str(position) + str(value) + Message.OBJECTIVE_END

    def add_obstacle(self, position: Coordinate, knowledge: Knowledge):
        try:
            self._data += \
                Message.OBSTACLE + Message.coord_str(position) + Message.KNOWLEDGE[knowledge] + Message.OBSTACLE_END
        except KeyError:
            raise TypeError("knowledge parameter wasn't Knowledge type")

    def get_data(self) -> str:
        return self._data + Message.END

    def handle(self, data: DataRepository):
        cursor = 1
        while cursor < len(self._data):
            if self._data[cursor] == Message.OBSTACLE:
                cursor += 1
                coordinate, cursor = self.extract_coordinates(cursor)
                value = Message.KNOWLEDGE.inv[self._data[cursor]]
                cursor += 1

                # verify segment ending
                assert self._data[cursor] == Message.OBSTACLE_END
                cursor += 1

                data.set_obstacle(coordinate, value)

            elif self._data[cursor] == Message.OBJECTIVE:
                cursor += 1
                coordinate, cursor = self.extract_coordinates(cursor)
                value, cursor = self.extract_objective_value(cursor)

                # verify segment ending
                assert self._data[cursor] == Message.OBJECTIVE_END
                cursor += 1

                data.set_objective(coordinate, value)
            elif self._data[cursor] == Message.END:
                cursor += 1
            # TODO: robot movement
            else:
                raise ValueError("bad message - data string: " + self._data + "  cursor: " + str(cursor))

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

    _my_robot_id = 0
    _next_message_id = 1

    def __init__(self, incoming: str=None):
        self._data = Message.BEGIN
        if incoming is None:
            self._write_header()
        else:
            self._data = incoming

        self._cursor = 0

    def _write_header(self):
        if Message._my_robot_id == 0:
            raise ValueError("robot id needs to be set before creating new messages - Message.set_my_robot_id(n)")
        self._data = Message.BEGIN + str(Message._my_robot_id) + Message.SEPARATOR + \
                     str(Message._next_message_id) + Message.SEPARATOR
        Message._next_message_id += 1

    @staticmethod
    def set_my_robot_id(robot_id: int):
        Message._my_robot_id = robot_id

    @staticmethod
    def coord_str(coordinate: Coordinate) -> str:
        return str(coordinate.x) + Message.SEPARATOR + str(coordinate.y) + Message.SEPARATOR

    def extract_number(self) -> int:
        """ extracts integer from data
            :returns number extracted """
        separator_index = self._data.index(Message.SEPARATOR, self._cursor)
        number = int(self._data[self._cursor:separator_index])
        self._cursor = separator_index + 1

        return number

    def extract_coordinates(self) -> Coordinate:
        """ inverse of coord_str starting from index cursor
            :returns Coordinate """
        x = self.extract_number()
        y = self.extract_number()

        return Coordinate(x, y)

    def extract_objective_value(self) -> OBJECTIVE_TYPE:
        end = self._data.index(Message.OBJECTIVE_END, self._cursor)
        value = Message.OBJECTIVE_TYPE(self._data[self._cursor:end])
        self._cursor = end
        return value

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
        self._cursor = 1
        robot_id = self.extract_number()
        message_id = self.extract_number()
        print("robot id:", robot_id, "  message id:", message_id)

        while self._cursor < len(self._data):
            if self._data[self._cursor] == Message.OBSTACLE:
                self._cursor += 1
                coordinate = self.extract_coordinates()
                value = Message.KNOWLEDGE.inv[self._data[self._cursor]]
                self._cursor += 1

                # verify segment ending
                assert self._data[self._cursor] == Message.OBSTACLE_END
                self._cursor += 1

                data.set_obstacle(coordinate, value)

            elif self._data[self._cursor] == Message.OBJECTIVE:
                self._cursor += 1
                coordinate = self.extract_coordinates()
                value = self.extract_objective_value()

                # verify segment ending
                assert self._data[self._cursor] == Message.OBJECTIVE_END
                self._cursor += 1

                data.set_objective(coordinate, value)
            elif self._data[self._cursor] == Message.END:
                self._cursor += 1
            # TODO: robot movement
            else:
                raise ValueError("bad message - data string: " + self._data + "  cursor: " + str(self._cursor))

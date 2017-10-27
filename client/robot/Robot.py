from dataRepository import DataRepository
from physicalInterface import SimPhysicalInterface
from utils import COORDINATE_CHANGE, Knowledge, Coordinate

from threading import Thread


class Robot:
    def __init__(self, map_width: int, map_height: int, home: Coordinate, seed: int):
        self.data = DataRepository(map_width, map_height)
        self.interface = SimPhysicalInterface(map_width, map_height, seed)
        self.home = home

        self.interface.position = home

    def visit_current_space(self):
        # objective reading
        self.data.set_objective(self.interface.position, self.interface.read_sensor())
        # check obstacles
        for direction in COORDINATE_CHANGE:
            looking_at = self.interface.position + COORDINATE_CHANGE[direction]
            if not self.data.out_of_bounds(looking_at):
                self.data.set_obstacle(looking_at,
                                       Knowledge.YES if self.interface.see_obstacles(direction) else Knowledge.NO)

    def go(self):
        communication = Thread(target=self.communication_run(), args=(self,))
        communication.start()

        self.visit_current_space()  # home

        while True:
            target = self.data.find_target(self.interface.position, self.home)

            print("target:", target)

            path_to_target = self.data.find_path(self.interface.position, target)
            print("path:", path_to_target)
            if len(path_to_target) > 0:
                self.interface.turn(path_to_target[0])
                self.interface.forward()
                self.visit_current_space()

            print(self.data.text_map(self.interface.position, self.interface.facing))
            input()  # wait for enter key

    def communication_run(self):
        """this is the main control of the communication thread"""
        pass

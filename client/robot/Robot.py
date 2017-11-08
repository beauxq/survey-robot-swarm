from dataRepository import DataRepository
from physicalInterface import SimPhysicalInterface
from comm import CommunicationManager, Message
from utils import COORDINATE_CHANGE, Knowledge, Coordinate

from time import sleep


class Robot:
    def __init__(self, map_width: int, map_height: int, home: Coordinate, seed: int, robot_id: int, robot_count: int):
        self.data = DataRepository(map_width, map_height)
        self.interface = SimPhysicalInterface(map_width, map_height, seed)
        self.home = home
        self.communication = CommunicationManager(self.data, robot_id, robot_count)

        self.interface.position = home

    def visit_current_space(self):
        message = Message()

        # objective reading
        already_have = self.data.get_objective(self.interface.position) != Knowledge.UNKNOWN
        self.data.set_objective(self.interface.position, self.interface.read_sensor())
        if not already_have:
            message.add_objective(self.interface.position, self.data.get_objective(self.interface.position))

        # check obstacles
        for direction in COORDINATE_CHANGE:
            looking_at = self.interface.position + COORDINATE_CHANGE[direction]
            if not self.data.out_of_bounds(looking_at):
                previous = self.data.get_obstacle(looking_at)
                new = Knowledge.YES if self.interface.see_obstacles(direction) else Knowledge.NO
                if new != previous:
                    self.data.set_obstacle(looking_at, new)
                    message.add_obstacle(looking_at, new)

        self.communication.send_message(message)

    def go(self):
        self.communication.start_listen_thread()
        sleep(0.5)
        self.communication.start_outgoing_thread()
        sleep(0.5)

        self.visit_current_space()  # home

        while True:
            target = self.data.find_target(self.interface.position, self.home)

            print("target:", target)

            path_to_target = self.data.find_path(self.interface.position, target)
            print("path:", path_to_target)
            if len(path_to_target) > 0:
                # TODO: get permission from communication thread to make this move
                self.interface.turn(path_to_target[0])
                self.interface.forward()
                self.visit_current_space()

            print(self.data.text_map(self.interface.position, self.interface.facing))
            # input()  # wait for enter key - TODO: timing
            sleep(0.5)

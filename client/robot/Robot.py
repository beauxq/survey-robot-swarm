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

        self.wait_for_enter = True  # enter key between each robot movement
        self.display_text_map = True

    def visit_current_space(self) -> float:
        """ :returns time taken """
        total_time = 0

        message = Message(self.communication)

        # objective reading
        already_have = self.data.get_objective(self.interface.position) != Knowledge.UNKNOWN
        data, time_taken = self.interface.read_sensor()
        total_time += time_taken
        self.data.set_objective(self.interface.position, data)
        if not already_have:
            message.add_objective(self.interface.position, self.data.get_objective(self.interface.position))

        # check obstacles
        for direction in COORDINATE_CHANGE:
            looking_at = self.interface.position + COORDINATE_CHANGE[direction]
            if not self.data.out_of_bounds(looking_at):
                previous = self.data.get_obstacle(looking_at)
                obstacle_reading, time_taken = self.interface.see_obstacles(direction)
                total_time += time_taken
                new = Knowledge.YES if obstacle_reading else Knowledge.NO
                if new != previous:
                    self.data.set_obstacle(looking_at, new)
                    message.add_obstacle(looking_at, new)

        self.communication.send_message(message)
        return total_time

    def go(self) -> float:
        """ :returns total time taken """
        self.communication.start_listen_thread()
        sleep(0.5)
        self.communication.start_outgoing_thread()
        sleep(0.5)

        count_home_target = 0

        total_time = 0

        total_time += self.visit_current_space()  # home

        while count_home_target < 100:
            target = self.data.find_target(self.interface.position, self.home)
            # print("target:", target)
            if target == self.home:
                count_home_target += 1
            else:
                count_home_target = 0

            path_to_target = self.data.find_path(self.interface.position, target)
            # print("path:", path_to_target)
            if len(path_to_target) > 0:
                # TODO: get permission from communication thread to make this move
                total_time += self.interface.turn(path_to_target[0])
                total_time += self.interface.forward()
                total_time += self.visit_current_space()

            if self.display_text_map:
                print(self.data.text_map(self.interface.position, self.interface.facing))
                print("total time:", total_time)
                if not self.wait_for_enter:  # 2 program demo
                    sleep(0.5)  # instead of waiting for enter, we put a delay between each move
            if self.wait_for_enter:
                input()  # wait for enter key - TODO: timing

        # exit while loop when targeted home 100 times
        self.communication.stop_outgoing_thread()
        self.communication.stop_listen_thread()

        return total_time

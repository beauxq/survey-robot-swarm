from dataRepository import DataRepository
from comm import Message

from queue import Queue, Empty
import socket
from threading import Thread
import time


class CommunicationManager:
    HOST = ""  # all available interfaces
    PORT = 7676
    BROADCAST = "192.168.76.255"
    ADDRESS_PREFIX = "192.168.76."

    ACK_INTERVAL = 0.5  # second acknowledgements every this many seconds

    def __init__(self, data_repository: DataRepository, robot_id: int, robot_count: int):
        self._data = data_repository
        self._address = CommunicationManager.ADDRESS_PREFIX + str(robot_id)  # ip address for this robot

        self._unacknowledged_messages = Queue()  # TODO: parameter is max length, decide on a good one
        self._highest_acknowledge_from = dict()  # this key robot has received all my messages up to value
        self._highest_acknowledge_to = dict()  # received from key robot all messages up to this value
        # initialize acknowledgement dictionaries
        for i in range(1, robot_count+1):
            if i != robot_id:
                self._highest_acknowledge_from[i] = 0
                self._highest_acknowledge_to[i] = 0

        self._my_robot_id = robot_id

        # set that id for the Message class
        Message.set_my_robot_id(self._my_robot_id)

        self._listen_thread = Thread(target=self._receive_incoming_messages)
        self._send_thread = Thread(target=self._outgoing_thread)

    @staticmethod
    def extract_robot_id_from_address(address: str) -> int:
        """ the robot id is the last number of the ip address """
        index = address.rfind(".") + 1
        return int(address[index:])

    def _receive_incoming_messages(self):
        """ thread function
            open listening socket and handle messages """
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("starting listening socket")
            listen_socket.bind((CommunicationManager.HOST, CommunicationManager.PORT))
        except Exception as e:
            print("unable to start listening socket", e)
            return
        print("listening socket opened")

        while True:
            data, address = listen_socket.recvfrom(1024)
            from_robot_id = CommunicationManager.extract_robot_id_from_address(address[0])
            print("incoming connection from robot", from_robot_id)

            if from_robot_id != self._my_robot_id:  # ignore if it's from me
                string = bytes.decode(data)  # decode it to string
                message = Message(string)
                print("message:", message.get_data())

                # check to see if it's an acknowledgement
                robot_id, message_id = message.is_ack()
                if robot_id:
                    # check to see if it's an acknowledgement TO ME
                    if robot_id == self._my_robot_id:
                        self._highest_acknowledge_from[from_robot_id] = \
                            max(message_id, self._highest_acknowledge_from[from_robot_id])
                    # else ignore it (not for me)

                else:  # not an acknowledgement
                    try:
                        robot_id, message_id = message.extract_from_info()
                        if message_id == self._highest_acknowledge_to[robot_id] + 1:
                            message.handle(self._data)
                        # else  it's either already handled or one was skipped, so ignore it
                    except ValueError as e:
                        print("handle message failed:", e)
                        robot_id = 0
                        message_id = 0
                    if robot_id:
                        # outgoing thread will make acknowledgement and send it
                        self._highest_acknowledge_to[robot_id] = message_id

    def start_listen_thread(self):
        self._listen_thread.start()

    def start_outgoing_thread(self):
        self._send_thread.start()

    @staticmethod
    def _send_message(message: Message):
        """ outgoing thread calls this to send messages """
        data = message.get_data().encode("utf-8")
        print("sending", data)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        send_socket.connect((CommunicationManager.BROADCAST, CommunicationManager.PORT))
        send_socket.sendall(data)
        send_socket.shutdown(socket.SHUT_WR)
        send_socket.close()

    def send_message(self, message: Message):
        self._unacknowledged_messages.put(message)

    def _outgoing_thread(self):
        previous_message_id = 0  # used to put a delay between repeating sends of the same message
        timer = time.time()
        while True:

            if time.time() - CommunicationManager.ACK_INTERVAL > timer:
                # print("sending acknowledgements:", [v for v in self._highest_acknowledge_to.values()])
                # send all acknowledgements
                for robot_id, message_id in self._highest_acknowledge_to.items():
                    ack = Message(Message.acknowledge(robot_id, message_id))
                    CommunicationManager._send_message(ack)
                timer = time.time()

            # send messages from outgoing queue
            # print("about to pull a message from queue")
            try:
                message = self._unacknowledged_messages.get(timeout=CommunicationManager.ACK_INTERVAL)
                this_message_id = message.extract_from_info()[1]
                # print("pulled from queue", this_message_id)
                # check has this id been acknowledged by everyone?
                acknowledged = True
                for message_id in self._highest_acknowledge_from.values():
                    if message_id < this_message_id:
                        acknowledged = False
                if not acknowledged:
                    if this_message_id < previous_message_id:
                        time.sleep(CommunicationManager.ACK_INTERVAL)
                    previous_message_id = this_message_id
                    CommunicationManager._send_message(message)
                    self._unacknowledged_messages.put(message)
                # else this message has been acknowledged by everyone, so drop it
                else:  # debugging
                    # print(this_message_id, "acknowledged, so dropping")
                    pass
            except Empty:
                pass

from dataRepository import DataRepository
from comm import Message
from utils import Coordinate

from queue import Queue
import socket
from threading import Thread


class CommunicationManager:
    HOST = ""  # all available interfaces
    PORT = 7676
    BROADCAST = "192.168.76.255"

    def __init__(self, data_repository: DataRepository, address: str):
        self._data = data_repository
        self._address = address  # ip address for this robot

        # extract robot id from address
        index = address.rfind(".") + 1
        self._my_robot_id = int(address[index:])

        # set that id for the Message class
        Message.set_my_robot_id(self._my_robot_id)

        self._listen_thread = Thread(target=self._receive_incoming_messages)

    """
        self._incoming_messages = Queue()  # TODO: parameter is max length, decide on a good one

    def _handle_incoming_messages(self):
        "" worker thread ""
        while True:
            message = self._incoming_messages.get()
            message.handle(self._data)
    """

    def _receive_incoming_messages(self):
        """ open listening socket and handle messages """
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
            print("incoming connection from", address)

            if address[0] != self._address:  # ignore if it's from me
                string = bytes.decode(data)  # decode it to string
                print("message:", string)
                Message(string).handle(self._data)

    def start_listen_thread(self):
        self._listen_thread.start()

    @staticmethod
    def send_message(message: Message):
        data = message.get_data().encode("utf-8")
        print("sending", data)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_socket.connect((CommunicationManager.BROADCAST, CommunicationManager.PORT))
        send_socket.sendall(data)
        send_socket.shutdown(socket.SHUT_WR)
        send_socket.close()

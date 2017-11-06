from dataRepository import DataRepository
from comm import Message
from utils import Coordinate

from queue import Queue
import socket


class CommunicationManager:
    HOST = ""  # all available interfaces
    PORT = 7676
    BROADCAST = "192.168.76.255"

    def __init__(self, data_repository: DataRepository, address: str):
        self._data = data_repository
        self.address = address  # ip address for this robot

    """
        self._incoming_messages = Queue()  # TODO: parameter is max length, decide on a good one

    def _handle_incoming_messages(self):
        "" worker thread ""
        while True:
            message = self._incoming_messages.get()
            message.handle(self._data)
    """

    def _receive_incoming_messages(self):
        """ open listening socket and put messages in queue """
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("starting listening socket")
            listen_socket.bind((CommunicationManager.HOST, CommunicationManager.PORT))
        except Exception as e:
            print("unable to start listening socket", e)
            return
        print("listening socket opened")

        while True:
            listen_socket.listen()

            connection, address = listen_socket.accept()  # this line blocks the thread until a connection comes
            print("incoming connection from", address)

            if address != self.address:  # ignore if it's from me
                data = connection.recv(1024)  # receive data from client
                string = bytes.decode(data)  # decode it to string
                print("message:", string)
                Message(string).handle(self._data)

            connection.close()

    def send_message(self, message: Message):
        data = message.get_data().encode("utf-8")
        print("sending", data)
        send_socket = socket.socket()
        send_socket.connect((CommunicationManager.BROADCAST, CommunicationManager.PORT))
        send_socket.sendall(data)
        send_socket.shutdown(socket.SHUT_WR)
        send_socket.close()

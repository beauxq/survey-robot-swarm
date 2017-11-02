from dataRepository import DataRepository
from comm import Message
from utils import Coordinate

from queue import Queue


class CommunicationManager:
    def __init__(self, data_repository: DataRepository):
        self._data = data_repository
        self._incoming_messages = Queue()  # TODO: parameter is max length, decide on a good one

    def _handle_incoming_messages(self):
        """ worker thread """
        while True:
            message = self._incoming_messages.get()
            message.handle(self._data)

    def _receive_incoming_messages(self):
        """ open listening socket and put messages in queue """
        # TODO: open listening socket and put messages in queue
        pass

    def send_message(self, message: Message):
        pass

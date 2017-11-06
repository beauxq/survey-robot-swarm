import socket

from threading import Thread

# https://stackoverflow.com/questions/22878625/receiving-broadcast-packets-in-python


class Client:
    PORT = 7676
    HOST = ""  # all available interfaces

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("binding socket")
            self.socket.bind((Client.HOST, Client.PORT))
        except Exception as e:
            print("unable to bind socket", e)
            return
        print("socket bind complete")

    def _listen_thread(self):
        while True:  # False to disable server

            data = self.socket.recvfrom(1024)

            print("data:", data)

            """ this is the stuff that worked for unicast
            self.socket.listen()

            connection, address = self.socket.accept()  # this line blocks the thread until a connection comes
            print("incoming connection from", address)

            data = connection.recv(1024)  # receive data from client
            string = bytes.decode(data)  # decode it to string
            print("message:", string)
            # self._incoming_messages.put(Message(string))

            connection.close()
            """

    def go(self):
        listen_thread = Thread(target=self._listen_thread)
        listen_thread.start()

        my_input = input("input (~ to stop):")
        while my_input != "~":
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            send_socket.connect(("127.255.255.255", Client.PORT))
            sent = send_socket.sendall(my_input.encode("utf-8"))
            send_socket.shutdown(socket.SHUT_WR)
            send_socket.close()
            print("sent:", sent)
            my_input = input("input (~ to stop):")
        listen_thread.join()


def main():
    c = Client()
    c.go()


if __name__ == "__main__":
    main()

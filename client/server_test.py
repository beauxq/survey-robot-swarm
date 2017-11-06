# listen on (7676) and print to screen what is received

import socket

HOST = ""
PORT = 7676

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
print("listening")

while True:
    server_socket.listen()
    connection, address = server_socket.accept()
    print("got connection from", address)
    data = connection.recv(1024)  # receive data from client
    string = bytes.decode(data)  # decode it to string
    print("message:", string)
    # self._incoming_messages.put(Message(string))

    connection.close()

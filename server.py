#socket_echo_server_dgram.py
import socket
import sys
import pickle

class player:
    def __init__(self, name, socket, UDPport)
        self.score = 0
        self.pos = None
        self.isDrawing = False
        self.TCPsock = socket
        self.UDPport = UDPport
        self.name = name

class server:
    def __init__(self):
        self.UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self. TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = "localhost"
        self.UDPport = 10000
        self.TCPport = 11000

    def start(self):
        # bind UDP socket
        self.UDPsock.bind((self.server_address, self.UDPport))
        # bind TCP socket
        self.TCPsock.bind((self.server_address, self.TCPport))
        # accept connections on the TCP socket.
        self.TCPsock.accept(1)
        while True:
            client_TCPSocket, client_address = TCPsock.accept()
            # players name is the amount of players + 1, players UDP port is 
            # is the amount of players plus 10001
            player = player("player" + len(players_list) + 1, client_TCPSocket, 
                            len(players_list + 10001))
            self.players_list.append(player)
            # send the UDP port to the client
            player.socket.sendall((player.UDPport + "").encode())


# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print('starting up on {} port {}'.format(*server_address))
# sock.bind(server_address)
# while True:
#     data, address = sock.recvfrom(4096)
#     sock.sendto(data, ("127.0.0.1", 1444))

    
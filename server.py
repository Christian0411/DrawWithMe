#socket_echo_server_dgram.py
from socket import *
import sys
import pickle

class player:
    def __init__(self, name, socket, UDPport):
        self.score = 0
        self.pos = None
        self.isDrawing = False
        self.TCPsock = socket
        self.UDPport = UDPport
        self.name = name

class server:
    def __init__(self):
        self.UDPsock = socket(AF_INET, SOCK_DGRAM)
        self.TCPsock = socket(AF_INET, SOCK_STREAM)
        self.TCPsock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.server_address = "localhost"
        self.UDPport = 10000
        self.TCPport = 11000

        self.players_list = []

    def start(self):
        # bind UDP socket
        self.UDPsock.bind((self.server_address, self.UDPport))
        # bind TCP socket
        self.TCPsock.bind((self.server_address, self.TCPport))
        self.TCPsock.listen(1)
        
        while True:
            client_TCPSocket, client_address = self.TCPsock.accept()
            # players name is the amount of players + 1, players UDP port is 
            # is the amount of players plus 10001
            player1 = player("player" + str(len(self.players_list) + 1), client_TCPSocket, 
                            len(self.players_list) + 10001)
            self.players_list.append(player1)
            # send the UDP port to the client
            player1.TCPsock.sendall(pickle.dumps(("UDPport", player1.UDPport)))

if __name__ == "__main__":
    server = server()
    server.start()

# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print('starting up on {} port {}'.format(*server_address))
# sock.bind(server_address)
# while True:
#     data, address = sock.recvfrom(4096)
#     sock.sendto(data, ("127.0.0.1", 1444))

    
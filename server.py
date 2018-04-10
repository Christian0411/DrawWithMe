#socket_echo_server_dgram.py
from socket import *
import sys
import pickle
from threading import Thread
class player:
    def __init__(self, name, socket, UDPport, address):
        self.score = 0
        self.pos = None
        self.isDrawing = False
        self.TCPsock = socket
        self.UDPport = UDPport
        self.name = name
        self.address = address

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

        self.udp_thread = Thread(target= self.recv_udp, args=())
        self.udp_thread.start()
        
        while True:
            client_TCPSocket, client_address = self.TCPsock.accept()
            print("client accepted " + str(client_address))
            # players name is the amount of players + 1, players UDP port is 
            # is the amount of players plus 10001
            player1 = player("player" + str(len(self.players_list) + 1),
                             client_TCPSocket, len(self.players_list) + 10001, client_address[0])
            for p1 in self.players_list:
                p1.TCPsock.sendall(pickle.dumps(("newPlayer", player1.name + "      " + str(p1.score), player1.score)))
            self.players_list.append(player1)
            self.p_thread = Thread(target=self.handle_player, args=(player1,))
            self.p_thread.start()
            # send the UDP port to the client
            player1.TCPsock.sendall(pickle.dumps(("UDPport", player1.UDPport)))
            if len(self.players_list) >= 2:
                self.game_start()

    def game_start(self):
        self.players_list[0].TCPsock.sendall(pickle.dumps(("makeDrawer", True)))
    def handle_player(self, player):
        player.TCPsock.sendall(pickle.dumps(("updatePlayerList", [x.name + "     " + str(x.score)  for x in self.players_list])))
        while True:
            pass
    def recv_udp(self):
        print("Here")
        while True:
            data, address = self.UDPsock.recvfrom(4096)
            data = pickle.loads(data)
            for player in self.players_list:
                if player.UDPport != address[1]:
                    self.UDPsock.sendto(pickle.dumps(("Draw",data)), (player.address, player.UDPport))
                    self.UDPsock.sendto(pickle.dumps(("Draw",data)), (player.address, player.UDPport))
                    self.UDPsock.sendto(pickle.dumps(("Draw",data)), (player.address, player.UDPport))



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

    
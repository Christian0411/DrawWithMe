#socket_echo_server_dgram.py
import socket
import sys
import pickle
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    sock.sendto(data, ("127.0.0.1", 1444))

    
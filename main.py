'''
Citations:
    - Drawing Functionality: https://stackoverflow.com/questions/597369/how-to-create-ms-paint-clone-with-python-and-pygame
'''
import pygame, random
import socket
import pickle
from threading import Thread
class client: 
    def __init__(self):
        self.q = None
        self.UDPsock = None
        self.UDPdata = None

    def roundline(self, srf, color, start, end, radius=1):
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
            pygame.draw.circle(srf, color, (x, y), radius)

    def UDPrecv(self):
        while True:
            try:
                item = self.q.get()
                if item == 'stop':
                    break
            except:
                pass

            self.UDPdata, server = self.UDPsock.recvfrom(4096)
    def TCPrecv(self):
        while True:
            try:
                item = self.q.get()
                if item == 'stop':
                    break
            except:
                pass
            self.TCPdata, server = self.TCPsock.recvfrom(4096)


    def stop_recv_thread(self):
        self.q.put('stop')

    def main(self):
        draw_on = False
        last_pos = (0, 0)
        color = (random.randrange(256), random.randrange(256), random.randrange(256))
        radius = 5

        screen = pygame.display.set_mode((800,600))
        screen.fill((255, 255, 255))
        # Create a UDP socket
        self.UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Create TCP socket
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server_address = ('localhost', 10000)
        
        # start the tcp receive thread
        TCPrecv_thread = Thread(target=self.TCPrecv, args=())
        TCPrecv_thread.start()

        try:
            while True:
                
                e = pygame.event.wait()
                if e.type == pygame.QUIT:
                    raise StopIteration
                if e.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.circle(screen, color, e.pos, radius)
                    self.UDPsock.sendto(pickle.dumps((e.pos, last_pos, color)), self.server_address)
                    draw_on = True
                if e.type == pygame.MOUSEBUTTONUP:
                    draw_on = False
                if e.type == pygame.MOUSEMOTION:
                    if draw_on:
                        pygame.draw.circle(screen, color, e.pos, radius)
                        self.roundline(screen, color, e.pos, last_pos,  radius)
                        self.UDPsock.sendto(pickle.dumps((e.pos, last_pos, color)), self.server_address)
                    last_pos = e.pos
                pygame.display.flip()
        except StopIteration:
            pass

        pygame.quit()


if __name__ == "__main__":
    client = client()
    client.main()

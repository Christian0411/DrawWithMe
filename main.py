'''
Citations:
    - Drawing Functionality: https://stackoverflow.com/questions/597369/how-to-create-ms-paint-clone-with-python-and-pygame
'''
import pygame, random
import socket
import pickle
from threading import Thread
import queue
import pygame_textinput

class client: 
    def __init__(self):
        self.q = queue.Queue()
        self.UDPsock = None
        self.UDPdata = None
        self.UDP_address = None
        self.isDrawer = False

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
            self.UDPdata, server = self.UDPsock.recvfrom(4096)
            try:
                self.UDPdata = pickle.loads(self.UDPdata)
                print(self.UDPdata)
            except:
                pass
    def TCPrecv(self):
        while True:
            print("asdf")
            TCPdata = self.TCPsock.recv(4096)
            if TCPdata != "": 
                self.handle_tcp_data(TCPdata)


    def handle_tcp_data(self,data_tuple):
        try:
            data_tuple = pickle.loads(data_tuple)
            if data_tuple[0] == "UDPport":
                self.start_UDP(data_tuple[1])
            if data_tuple[0] == "makeDrawer":
                self.isDrawer = data_tuple[1]

        except:
            pass

    def start_UDP(self, port):
        print(port)
        self.UDP_address = ("localhost", port)
        self.UDPsock.bind(("localhost", port))
        self.UDPrecv_thread.start()
        
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
        
        self.chatinput = pygame_textinput.TextInput()
        self.server_address = ('localhost', 11000)
        self.TCPsock.connect(self.server_address)
        # start the tcp receive thread
        self.TCPrecv_thread = Thread(target=self.TCPrecv, args=())
        self.TCPrecv_thread.daemon = True
        self.UDPrecv_thread = Thread(target=self.UDPrecv, args=())
        self.UDPrecv_thread.daemon = True
        self.TCPrecv_thread.start()

        
        clock = pygame.time.Clock()
        # this surface represents the are the chat is in
        chat_bar_surface = pygame.Surface((800,20))
        # fill the surface with a color
        chat_bar_surface.fill((96,106,117))

        try:
            while True:
                events = pygame.event.get()
                # If enter has been pressed
                if self.chatinput.update(events):
                    print(self.chatinput.get_text())
                    self.chatinput.clear_text()
                
                # Draw the input onto the chat area surface
                chat_bar_surface.blit(self.chatinput.get_surface(), (0, 3))
                # Draw the chat area surface onto the screen
                screen.blit(chat_bar_surface, (0,580))
                # Refresh the chat area
                chat_bar_surface.fill((96,106,117))
               

                for e in events:
                    if e.type == pygame.QUIT:
                        raise StopIteration
                    if e.type == pygame.MOUSEBUTTONDOWN and self.isDrawer:
                        pygame.draw.circle(screen, color, e.pos, radius)
                        try:
                            self.UDPsock.sendto(pickle.dumps((e.pos, last_pos, color)), self.UDP_address)
                        except:
                            pass
                        draw_on = True
                    if e.type == pygame.MOUSEBUTTONUP and self.isDrawer:
                        draw_on = False
                    if e.type == pygame.MOUSEMOTION and self.isDrawer:
                        if draw_on:
                            pygame.draw.circle(screen, color, e.pos, radius)
                            self.roundline(screen, color, e.pos, last_pos,  radius)
                            try:
                                self.UDPsock.sendto(pickle.dumps((e.pos, last_pos, color)), ("localhost", 10000))
                            except Exception as b:
                                print(b)
                        last_pos = e.pos
                if not self.isDrawer:
                    try:
                        pos, last_pos, color = self.UDPdata[1]
                        pygame.draw.circle(screen, color, pos, radius)
                        self.roundline(screen, color, pos, last_pos,  radius)
                    except:
                        pass

                pygame.display.update()
                clock.tick(30)
        except StopIteration:
            self.stop_recv_thread()

        pygame.quit()

        


if __name__ == "__main__":
    client = client()
    client.main()

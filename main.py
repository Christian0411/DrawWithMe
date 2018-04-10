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
pygame.init()

class client:
    def __init__(self):
        self.q = queue.Queue()
        self.UDPsock = None
        self.UDPdata = None
        self.UDP_address = None
        self.isDrawer = False
        self.playersCount = 0
        self.players_list = []
        self.playeroffset = 10
        self.UDPdatalist = []

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
            self.UDPdata, server = self.UDPsock.recvfrom(8126)
            try:
                self.UDPdata = pickle.loads(self.UDPdata)
                if self.UDPdata not in self.UDPdatalist:
                    self.UDPdatalist.append(self.UDPdata)
            except:
                pass
    def TCPrecv(self):
        while True:
            TCPdata = self.TCPsock.recv(8126)
            if TCPdata != "":
                self.handle_tcp_data(TCPdata)


    def handle_tcp_data(self,data_tuple):
        try:
            data_tuple = pickle.loads(data_tuple)
            if data_tuple[0] == "UDPport":
                self.start_UDP(data_tuple[1])
            if data_tuple[0] == "makeDrawer":
                self.isDrawer = data_tuple[1]
            if data_tuple[0] == "updatePlayerList":
                for player in data_tuple[1]:
                    self.playeroffset = self.playeroffset + 20
                    self.players_list.append((player, self.playeroffset))
            if data_tuple[0] == "newPlayer":
                self.playeroffset = self.playeroffset + 20
                self.players_list.append((data_tuple[1], self.playeroffset))
        except:
            pass

    def start_UDP(self, port):
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

        pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
        self.myfont = pygame.font.SysFont('Arial', 15)
        textsurface = self.myfont.render('Enter guess:', True, (0, 0, 0))
        scoreboardtext = self.myfont.render('Scoreboard', True, (255, 255, 255))
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
        chat_bar_surface = pygame.Surface((649,20))
        # fill the surface with a color
        chat_bar_surface.fill((96,106,117))

        score_board_surface = pygame.Surface((150, 600))
        score_board_surface.fill((96,106,117))


        try:
            while True:
                events = pygame.event.get()
                # If enter has been pressed
                if self.chatinput.update(events):
                    self.chatinput.clear_text()

                # Draw the input onto the chat area surface
                chat_bar_surface.blit(self.chatinput.get_surface(), (3, 3))
                # Draw the chat area surface onto the screen
                screen.blit(chat_bar_surface, (0,580))
                screen.blit(score_board_surface, (650, 0))
                screen.blit(scoreboardtext, (682, 5))
                self.update_scoreboard(screen)
                # Refresh the chat area
                chat_bar_surface.fill((96,106,117))

                screen.blit(textsurface,(3,560))

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
                        if self.UDPdata in self.UDPdatalist:
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
    def update_scoreboard(self, screen):
        for player in self.players_list:

            playername = self.myfont.render(player[0],True, (255, 255, 255))
            screen.blit(playername, (660, player[1]))


if __name__ == "__main__":
    client = client()
    client.main()

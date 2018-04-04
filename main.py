import pygame, random
import socket
import pickle
screen = pygame.display.set_mode((800,600))
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
sock.bind(('127.0.0.1', 1445))

draw_on = False
last_pos = (0, 0)
color = (255, 128, 0)
radius = 10

def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

try:
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
            pygame.draw.circle(screen, color, e.pos, radius)
            sock.sendto(pickle.dumps((e.pos, last_pos)), server_address)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos,  radius)
                sock.sendto(pickle.dumps((e.pos, last_pos)), server_address)
            last_pos = e.pos
        pygame.display.flip()

except StopIteration:
    pass

pygame.quit()

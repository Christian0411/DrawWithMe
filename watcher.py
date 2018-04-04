import pygame, random
import socket
import sys
import threading
import pickle
import queue

def recv():
    global q
    global sock
    global data

    while True:
        try:
            item = q.get()
            if item == 'stop':
                break
        except:
            pass

        data, server = sock.recvfrom(4096)

def stop_recv_thread():
    global q
    q.put('stop')

def roundline(srf, color, start, end, radius=0.5):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

def main():
    global q
    global sock
    global data

    draw_on = False
    last_pos = (0, 0)
    radius = 10
    data = (0,0)
    drawing = True

    q = queue.Queue()
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 10000)
    sock.bind(('127.0.0.1', 1444))

    pygame.init()

    screen = pygame.display.set_mode((800,600))
    screen.fill((255, 255, 255))

    recv_thread = threading.Thread(target=recv, args=())
    recv_thread.start()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise StopIteration

            pos = data
            try:
                pos, last_pos, color = pickle.loads(pos)
                pygame.draw.circle(screen, color, pos, radius)
                roundline(screen, color, pos, last_pos,  radius)

            except:
                pass
            pygame.display.update()

    except StopIteration:
        stop_recv_thread()

    pygame.quit()

if __name__ == "__main__":
    data = None
    q = None
    sock = None
    main()

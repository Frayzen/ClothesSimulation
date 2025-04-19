from os import read
from numpy.linalg import norm
from pygame import *

import pygame, sys
import numpy as np
from numpy import *
from pygame.locals import *
from pygame.time import Clock

from params import *

init()

screen=display.set_mode((w_screen, h_screen),0,32)

WHITE=(255,255,255)
RED=(255, 0, 0)
GREEN=(0,255,0)
BLUE=(0,0,255)

clock = Clock()

w_nodes = side * nb_x
h_nodes = side * nb_y
node_size = array([w_nodes, h_nodes])
mid = array([w_screen, h_screen]) / 2
from_pos = mid - node_size / 2

pts=np.zeros((nb_y, nb_x, 2))
vels=np.zeros((nb_y, nb_x, 2))
weights=np.ones((nb_y, nb_x))

# Pin the top corner ones
weights[0,0] = inf
weights[0,-1] = inf

for i in range(nb_x):
    for j in range(nb_y):
        offset=array([i * side, j * side])
        pts[j, i] = from_pos + offset

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(WHITE)
    for i in range(nb_x - 1):
        for j in range(nb_y - 1):
            v = pts[j:j+2, i:i+2].flatten().reshape((4,2))
            tmp = v[2].copy()
            v[2] = v[3]
            v[3] = tmp
            draw.polygon(screen, BLUE, v, 2)

    mpos = array(mouse.get_pos())
    curlen = inf
    curids = None
    curpos = None
    for i in range(nb_x):
        for j in range(nb_y):
            pos = pts[j, i]
            dst = norm(pos - mpos)
            if dst < curlen:
                curlen = dst
                curids = (j, i)
                cur = pos
    draw.circle(screen, RED, cur, 5)


    if mouse.get_pressed()[0]:
        pts[curids] = mpos
        weights[curids] = inf

    # Update pos
    dt = clock.tick(FPS) / 150
    for i in range(nb_x):
        for j in range(nb_y):
            vels[j, i][1] += dt * g * 1 / weights[j, i]
            p = pts[j,i]
            pts[j,i] = pts[j,i] + dt * vels[j,i]


    # For all edges
    for i in range(nb_x - 1):
        for j in range(nb_y - 1):
            p1, w1 = pts[j, i], weights[j,i]
            p2, w2 = pts[j + 1, i], weights[j + 1, i]
            p3, w3 = pts[j, i + 1], weights[j, i + 1]

            # Vertical edge
            dist1 = norm(p1 - p2)
            e1 = (side - dist1)*(p1 - p2) / dist1
            # draw.line(screen, )
            # pts[j,i] += e1 * -w1 / (w1 + w2)
            # pts[j + 1,i] += e1 * -w2 / (w1 + w2)

            # Horizontal edge
            dist2 = norm(p1 - p3)
            e2 = (side - dist2)*(p1 - p3) / dist2
            # pts[j,i] += e2 * -w1 / (w1 + w3)
            # pts[j,i+1] += e2 * -w3 / (w1 + w3)




    display.update()

from os import read
from numpy.linalg import norm
from pygame import *

import pygame, sys
import numpy as np
from numpy import *
from pygame.locals import *

from params import *

init()

screen=display.set_mode((w_screen, h_screen),0,32)

WHITE=(255,255,255)
BLUE=(0,0,255)
RED=(255, 0, 0)

w_nodes = side * nb_x
h_nodes = side * nb_y
node_size = array([w_nodes, h_nodes])
mid = array([w_screen, h_screen]) / 2
from_pos = mid - node_size / 2

pts=np.zeros((nb_y, nb_x, 2))

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


    display.update()

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
weights=np.ones((nb_y, nb_x)) # inverse of the mass

# Pin the top corner ones
weights[0,0] = 0
weights[0,-1] = 0

for i in range(nb_x):
    for j in range(nb_y):
        offset=array([i * side, j * side])
        pts[j, i] = from_pos + offset

def disp_tris():
    screen.fill(WHITE)
    for i in range(nb_x - 1):
        for j in range(nb_y - 1):
            v = pts[j:j+2, i:i+2].flatten().reshape((4,2))
            tmp = v[2].copy()
            v[2] = v[3]
            v[3] = tmp
            draw.polygon(screen, BLUE, v, 2)


while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    disp_tris()

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
        # weights[curids] = 0

    dt = clock.tick(FPS) / 150
    # dt = 0.1

    # Update pos
    oldpos = pts.copy()
    for i in range(nb_x):
        for j in range(nb_y):
            vels[j, i][1] += dt * g * weights[j, i]
            pts[j,i] = pts[j,i] + dt * vels[j,i]


    # For all squares
    # for i in range(nb_x - 1):
    #     for j in range(nb_y - 1):
    #         v = pts[j:j+2, i:i+2].flatten().reshape((4,2))
    #         tmp = v[2].copy()
    #         v[2] = v[3]
    #         v[3] = tmp

    #         w = weights[j:j+2, i:i+2].flatten().reshape(4)
    #         w[2], w[3] = w[3], w[2]


    #         """
    #         here:
    #         0 is pts[j,i]
    #         1 is pts[j,i+1]
    #         2 is pts[j+1,i+1]
    #         3 is pts[j+1,i]

    # e1      e2
    #   0____1       
    #   |\  /|       
    #   | \/ |       
    #   | /\ |       
    #   3/__\2       

    #         """

    #         e1 = (v[0] - v[2])
    #         e2 = (v[1] - v[3])
            
    #         curarea = norm(e1) * norm(e2) / 2

    #         grad_e1 = norm(e2) / 2 # how much of the area increases when e1 increases
    #         grad_e2 = norm(e1) / 2 # how much of the area increases when e2 increases

    #         ne1 = grad_e1 * e1/norm(e1) # dir of the gradient of 0 and 2 (inverse)
    #         ne2 = grad_e2 * e2/norm(e2) # dir of the gradient of 1 and 3 (inverse)

    #         darea = (curarea - area)

    #         alpha = 1 / k
    #         lmbda = -darea / ((w[0] + w[2]) * grad_e1 ** 2 + (w[1] + w[3]) * norm(e2) ** 2 + alpha / (dt ** 2))
    #         lmbda *= k

    #         pts[j,i] += lmbda * w[0] * ne1
    #         pts[j,i+1] += lmbda * w[1] * ne2
    #         pts[j+1,i+1] += lmbda * w[2] * -ne1
    #         pts[j+1,i] += lmbda * w[3] * -ne2

    # ensure edges are fixed length
    # verticals
    for i in range(nb_x - 1):
        for j in range(nb_y):
            p0 = pts[j,i]
            p1 = pts[j,i + 1]
            w0 = weights[j,i]
            w1 = weights[j,i + 1]
            e = p0 - p1
            curlen = norm(e)
            grad = 1
            ne = grad * e / norm(e)
            dlen = (curlen - side)
            alpha = 1 / k
            lmbda = -dlen / (w0 + w1 + alpha / (dt ** 2))
            lmbda *= k * 5
            pts[j,i] += lmbda * w0 * ne
            pts[j,i + 1] -= lmbda * w1 * ne
    # horizontal
    for i in range(nb_x):
        for j in range(nb_y - 1):
            p0 = pts[j,i]
            p1 = pts[j+1,i]
            w0 = weights[j,i]
            w1 = weights[j+1,i]
            e = p0 - p1
            curlen = norm(e)
            grad = 1
            ne = grad * e / norm(e)
            dlen = (curlen - side)
            alpha = 1 / k
            lmbda = -dlen / (w0 + w1 + alpha / (dt ** 2))
            lmbda *= k * 5
            pts[j,i] += lmbda * w0 * ne
            pts[j+1,i] -= lmbda * w1 * ne


    for i in range(nb_x):
        for j in range(nb_y):
            vels[j,i] = (pts[j,i] - oldpos[j,i]) / dt

    disp_tris()
    # input()
    display.update()



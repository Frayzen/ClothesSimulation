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


def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    mpos = array(mouse.get_pos())
    curlen = inf
    curids = None
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
    if mouse.get_pressed()[2]:
        pts[curids] = mpos
        weights[curids] = 0
        vels[curids] = array([0,0])

def apply_gravity(vels, weights, dt):
    vels[:, :, 1] += dt * g * weights
    return vels

def update_positions(pts, vels, dt):
    return pts + dt * vels

def apply_edge_constraints(pts, weights, dt, k):
    alpha = 1 / k
    inv_dt_sq = alpha / (dt ** 2)
    
    # Helper function for constraint application
    def apply_constraint(p0, p1, w0, w1):
        e = p0 - p1
        curlen = np.linalg.norm(e)
        if curlen == 0:
            return p0, p1  # Avoid division by zero
        ne = e / curlen
        dlen = (curlen - side)
        lmbda = -dlen / (w0 + w1 + inv_dt_sq)
        return lmbda * w0 * ne, -lmbda * w1 * ne
    
    # Horizontal constraints
    for i in range(nb_x):
        for j in range(nb_y - 1):
            delta_p0, delta_p1 = apply_constraint(
                pts[j, i], pts[j+1, i], weights[j, i], weights[j+1, i])
            pts[j, i] += delta_p0
            pts[j+1, i] += delta_p1
    
    # Vertical constraints
    for i in range(nb_x - 1):
        for j in range(nb_y):
            delta_p0, delta_p1 = apply_constraint(
                pts[j, i], pts[j, i+1], weights[j, i], weights[j, i+1])
            pts[j, i] += delta_p0
            pts[j, i+1] += delta_p1
    
    return pts

while True:
    handle_events()
    
    # Physics update
    oldpos = pts.copy()
    dt = clock.tick(FPS) / 250
    vels = apply_gravity(vels, weights, dt)
    pts = update_positions(pts, vels, dt)
    pts = apply_edge_constraints(pts, weights, dt, k)
    vels = damping * (pts - oldpos) / dt
    
    # Rendering
    screen.fill(WHITE)
    disp_tris()
    display.update()


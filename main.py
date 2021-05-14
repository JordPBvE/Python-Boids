import sys
import math
import random
import pygame
from pygame import Color
from pygame.math import Vector2

from boid import Boid
from boidframe import BoidFrame
from obstacle import Line
from util.palettes import get_random_color_palette
from util.input import *

width = 1024
height = 1024

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
pygame.init()

frame = BoidFrame(width=width, height=height)
color_palette = get_random_color_palette()

# Create boids:
boid_count = 90
for i in range(boid_count):
    random_pos = Vector2(random.randint(10, width - 10), random.randint(10, height -10))
    random_velocity = Vector2(random.uniform(-.5, .5), random.uniform(-.5, .5))
    frame.add_boid(Boid(pos=random_pos, velocity=random_velocity, max_speed=random.uniform(0.2, 0.3)))

# Create Walls
frame.create_walls()

should_run = True
while should_run:
    dt = clock.tick(60)

    frame.do_step(dt, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            process_mouse_event(event, frame)
        elif event.type == pygame.KEYDOWN:
            process_key_event(event, frame)
        elif event.type == pygame.VIDEORESIZE:
            process_resize_event(event, screen, frame)
    pygame.display.update()

    if frame.debug_mode:
        frame.print_collisions()


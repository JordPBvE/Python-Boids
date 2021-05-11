import sys
import math
import random
import pygame
from pygame import Color
from pygame.math import Vector2

from boid import Boid
from boidframe import BoidFrame
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
boid_count = 256
for i in range(boid_count):
    random_pos = Vector2(random.randint(0, width), random.randint(0, height))
    frame.add_boid(Boid(pos=random_pos, color=random.choice(color_palette[1:]), velocity=Vector2(-1, 0), max_speed=random.uniform(0.3, 0.45)))

should_run = True
while should_run:
    dt = clock.tick(60)
    screen.fill(color_palette[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_run = False
        elif event.type == pygame.KEYDOWN:
            process_keydown_event(event, frame)
        elif event.type == pygame.VIDEORESIZE:
            process_resize_event(event, screen, frame)
    frame.do_step(dt, screen)
    pygame.display.update()

import pygame
from pygame.math import Vector2
from pygame import Color
import sys
import random
import math


# class files
from boid import Boid
from boidframe import BoidFrame

width = 1024
height = 1024

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

frame = BoidFrame(width=width, height=height)


color_pallete = [   Color(26, 81, 115),
                    Color(60, 166, 97),
                    Color(242, 194, 48),
                    Color(242, 138, 128),
                    Color(191, 48, 48)]

boid_count = 100
for i in range(boid_count):
    random_pos = Vector2(random.randint(0, width), random.randint(0, height))
    frame.add_boid(Boid(pos=random_pos, color=random.choice(color_pallete), velocity=(Vector2(random.uniform(0.5, 0.8), random.uniform(0.5, 0.7)))))

pygame.init()
while True:
    dt = clock.tick(60)
    screen.fill(Color(0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    frame.do_step(dt, screen)
    pygame.display.update()

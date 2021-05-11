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


color_pallete_clown = [ Color(26, 81, 115),
                        Color(60, 166, 97),
                        Color(242, 194, 48),
                        Color(242, 138, 128),
                        Color(191, 48, 48) ]

color_pallete_sunny = [ Color(255, 195, 0),
                        Color(144, 12, 62),
                        Color(199, 0, 57),
                        Color(255, 87, 51),
                        Color(87, 24, 69) ]

color_pallete_neon = [ Color(0,0,0),
                       Color(250, 0, 154),
                       Color(176, 6, 214),
                       Color(105, 5, 237),
                       Color(17, 6, 214) ]

color_pallete_hackergreen = [ Color(0, 3, 0),
                              Color(6, 47, 64),
                              Color(2, 89, 81),
                              Color(29, 115, 75),
                              Color(22, 140, 64),
                              Color(130, 217, 43) ]

color_pallete = random.choice((color_pallete_clown, color_pallete_sunny, color_pallete_neon, color_pallete_hackergreen))


boid_count = 256
for i in range(boid_count):
    random_pos = Vector2(random.randint(0, width), random.randint(0, height))
    frame.add_boid(Boid(pos=random_pos, color=random.choice(color_pallete[1:]), velocity=Vector2(-1, 0), max_speed=random.uniform(0.3, 0.45)))

pygame.init()
while True:
    dt = clock.tick(60)
    screen.fill(color_pallete[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    frame.do_step(dt, screen)
    pygame.display.update()

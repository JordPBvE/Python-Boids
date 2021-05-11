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

frame = BoidFrame()

for i in range(1000):
    frame.add_boid(Boid((500,500), color=Color(random.randint(0, 255), random.randint(0,255), 28), size=8, velocity=(Vector2(random.uniform(-0.8, 0.8), random.uniform(-0.3, 0.7)))))

pygame.init()
while True:
    dt = clock.tick(60)
    screen.fill(Color(0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    frame.do_step(screen, dt)
    for boid in frame.boid_list:
        boid.draw(screen)
    pygame.display.update()

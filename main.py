import pygame
from pygame.math import Vector2
from pygame import Color
import sys
import random
import math


# class files
from boid import Boid

pygame.init()

pi = math.pi

width = 512
height = 512

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

red = pygame.Color(255, 0, 0)

boid_list = []

for i in range(20):
    boid_list.append(Boid((500,500), velocity=(Vector2(random.uniform(0.2, 0.8), random.uniform(0.3, 0.7)))))

# boid = Boid((500, 500), velocity=Vector2(0.5, -0.25))
# boid = Boid((550, 100), velocity=Vector2(0, -5)).draw(screen)
# boid = Boid((600, 600), velocity=Vector2(0.33, 4)).draw(screen)
# boid = Boid((650, 410), velocity=Vector2(1, 1)).draw(screen)
# boid = Boid((700, 990), velocity=Vector2(-1, 2)).draw(screen)
# boid = Boid((750, 220), velocity=Vector2(-4, 0)).draw(screen)

while True:
    dt = clock.tick(60)
    screen.fill(Color(0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for boid in boid_list:
        boid.do_step(dt)
        boid.draw(screen)
    pygame.display.update()

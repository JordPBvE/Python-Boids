import pygame
import sys
import random
import math

# class files
import boid

pygame.init()

pi = math.pi

width = 1300
height = 700

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

red = pygame.Color(255, 0, 0)

# game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.draw.circle(screen, red, (200, 200), 100)
    pygame.display.update()

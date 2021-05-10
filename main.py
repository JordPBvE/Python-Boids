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

# game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

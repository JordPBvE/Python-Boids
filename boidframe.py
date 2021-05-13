from boid import Boid
import pygame
from pygame import Color
from pygame.math import Vector2


# This is a class that contains all Boid objects
class BoidFrame:
    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height
        self.boid_list = []
        self.obstacle_list = []
        self.obstacle_size = 50
        self.debug_mode = False
        self.build_mode = False

    def add_boid(self, boid):
        self.boid_list.append(boid)
        boid.frame = self

    def add_obstacle(self, obstacle):
        self.obstacle_list.append(obstacle)
        obstacle.frame = self

    def do_step(self, dt, screen):
        for b in self.boid_list:
            b.do_step(dt)
            b.draw(screen)
        for o in self.obstacle_list:
            o.draw(screen)

        if self.build_mode:
            pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), self.obstacle_size, width = 1)

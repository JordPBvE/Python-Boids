from boid import Boid
import pygame
from random import randint
from pygame import Color
from pygame.math import Vector2


# This is a class that contains all Boid objects
class BoidFrame:
    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height
        self.boid_list = []
        self.boid_count = 0
        self.average_boid_pos = Vector2(0, 0)
        self.average_boid_velocity = Vector2(0, 0)

    def update_average_boid_pos(self):
        total_vector = Vector2(0, 0)
        for boid in self.boid_list:
            total_vector += boid.pos
        self.average_boid_pos = total_vector /self.boid_count

    def update_average_boid_velocity(self):
        total_vector = Vector2(0, 0)
        for boid in self.boid_list:
            total_vector += boid.velocity
        self.average_boid_velocity = total_vector / self.boid_count

    def add_boid(self, boid):
        self.boid_count += 1
        self.boid_list.append(boid)
        boid.frame = self
        boid.pos = Vector2(randint(0, self.width), randint(0, self.height))

    def do_step(self, dt, screen):
        self.update_average_boid_pos()
        self.update_average_boid_velocity()
        for b in self.boid_list:
            b.do_step(dt)
            b.draw(screen)

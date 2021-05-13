import random
from datetime import datetime

import pygame
from pygame import Color
from pygame.math import Vector2

from boid import Boid
from obstacle import Line
from util.palettes import get_random_color_palette

# This is a class that contains all Boid objects
class BoidFrame:
    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height
        self.boid_list = []
        self.obstacle_list = []
        self.line_list = []
        self.obstacle_size = 50
        self.debug_mode = False
        self.build_mode = False
        self.color_palette = get_random_color_palette()

    def add_boid(self, boid):
        boid.color = random.choice(self.color_palette[1:])
        self.boid_list.append(boid)
        boid.frame = self

    def add_obstacle(self, obstacle):
        self.obstacle_list.append(obstacle)
        obstacle.frame = self

    def do_step(self, dt, screen):
        screen.fill(self.color_palette[0])
        for b in self.boid_list:
            b.do_step(dt)
            b.draw(screen)
        for o in self.obstacle_list:
            o.draw(screen)
        for l in self.line_list:
            l.draw(screen)

        if self.build_mode:
            pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), self.obstacle_size, width = 1)

    def change_color_palette(self, palette):
        self.color_palette = palette
        for boid in self.boid_list:
            boid.color = random.choice(self.color_palette[1:])

    def print_collisions(self):
        for obstacle in self.obstacle_list:
            collisions = 0
            for boid in self.boid_list:
                if (obstacle.pos - boid.pos).length() < obstacle.radius:
                    collisions += 1
            if collisions > 0:
                print(f"{datetime.now()} | obstacle at pos {(obstacle.pos.x, obstacle.pos.y)} has {collisions} collisions. )")

    def create_walls(self):
        self.obstacle_list = []
        self.line_list = []
        self.line_list.append(Line(Vector2(1,1), Vector2(1, self.height - 1), pygame.Color(255, 255, 255), self))
        self.line_list.append(Line(Vector2(1,1), Vector2(self.width - 1, 1), pygame.Color(255, 255, 255), self))
        self.line_list.append(Line(Vector2(1, self.height - 1), Vector2(self.width - 1, self.height - 1), pygame.Color(255, 255, 255), self))
        self.line_list.append(Line(Vector2(self.width - 1,1), Vector2(self.width - 1, self.height - 1), pygame.Color(255, 255, 255), self))


from boid import Boid
import pygame
from pygame import Color
import math
from pygame.math import Vector2

class Circle():
    def __init__(self,
                pos,
                radius,
                color,
                visible,
                frame = None,
                strength = 1):
        self.frame = frame
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = visible
        self.strength = strength

    def draw(self, surface):
        if (self.visible):
            pygame.draw.circle(surface, self.color, self.pos, self.radius)

class Line():
    def __init__(self,
                begin_pos,
                end_pos,
                color,
                frame):

        self.frame = frame
        self.begin_pos = begin_pos
        self.end_pos = end_pos
        self.color = color
        self.length = (begin_pos - end_pos).length()
        self.circle_radius = 10

        self.populate()

    def populate(self):
        self.frame.line_list.append(self)
        circle_count = math.floor(self.length / (2*self.circle_radius))
        step = (self.end_pos - self.begin_pos) / circle_count
        circle_pos = self.begin_pos
        print(circle_count)
        for i in range(circle_count):
            circle = Circle(circle_pos, self.circle_radius, pygame.Color(255, 255, 255), False, self.frame, strength = 0.4)
            self.frame.obstacle_list.append(circle)
            circle_pos = self.begin_pos + i*step
    
    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.begin_pos, self.end_pos, width = 2)




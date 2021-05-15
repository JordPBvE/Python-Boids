
import pygame
from pygame import Color
import math
from pygame.math import Vector2

class Circle():
    def __init__(self,
                pos = Vector2(0, 0),
                radius = 10,
                color = Color(0, 0, 0),
                visible = True,
                frame = None,
                strength = 1):
        self.frame = frame
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = visible
        self.strength = strength

    def draw(self, surface):
        self.color = self.frame.color_palette[-1]
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
        self.circles = []
        self.length = (begin_pos - end_pos).length()
        self.circle_radius = 10

        self.populate()

    def populate(self):
        circle_count = math.floor(self.length / (2*self.circle_radius))
        step = (self.end_pos - self.begin_pos) / circle_count
        circle_pos = self.begin_pos

        for i in range(circle_count):
            circle = Circle(circle_pos, self.circle_radius, pygame.Color(255, 255, 255), False, self.frame, strength = 0.4)
            self.circles.append(circle)
            circle_pos = self.begin_pos + i*step
    
    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.begin_pos, self.end_pos, width = 2)

class Polygon():
    def __init__(self,
                color,
                frame,
                verteces = [],
                lines = []):
        self.color = color
        self.verteces = verteces
        self.lines = lines

    def add_vertex(self, position):
        self.verteces.append(position)
        if len(self.vertces) >= 2:
            self.lines.append(Line(self.verteces[-2], self.verteces[-1], self.frame.color_palette[-1], self.frame))
    
    def end_polygon(self):
        self.lines.append(Line(self.verteces[-1], self.verteces[0], self.frame.color_palette[-1], self.frame))

    def draw(self):
        for line in self.lines:
            line.draw()




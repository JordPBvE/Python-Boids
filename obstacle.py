import pygame
from pygame import Color
import math
from pygame.math import Vector2


class Circle:
    def __init__(
        self,
        pos=Vector2(0, 0),
        radius=10,
        color=Color(0, 0, 0),
        visible=True,
        frame=None,
        strength=1,
    ):
        self.frame = frame
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = visible
        self.strength = strength

    def draw(self, surface):
        if self.visible:
            pygame.draw.circle(surface, self.frame.palette_selector.palette().obstacle_color, self.pos, self.radius, width = 2)


class Line:
    def __init__(self, begin_pos, end_pos, color, frame):

        self.frame = frame
        self.begin_pos = begin_pos
        self.end_pos = end_pos
        self.color = color
        self.circles = []
        self.length = (begin_pos - end_pos).length()
        self.circle_radius = 10

        self.populate()

    def populate(self):
        circle_count = math.floor(self.length / (2 * self.circle_radius))
        step = (self.end_pos - self.begin_pos) / circle_count
        circle_pos = self.begin_pos

        for i in range(circle_count + 1):
            circle = Circle(
                pos = circle_pos,
                radius = self.circle_radius,
                color = self.frame.palette_selector.palette().obstacle_color,
                visible = True,
                frame = self.frame,
                strength = 0.3,
            )
            self.circles.append(circle)
            circle_pos = self.begin_pos + i * step

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.begin_pos, self.end_pos, width=2)
        for circle in self.circles:
            circle.draw(surface)


class Polygon:
    def __init__(self, color, frame, vertices=[], lines=[]):
        self.color = color
        self.frame = frame
        self.vertices = vertices
        self.lines = lines
        self.create()

    def create(self):
        for i in range(len(self.vertices)):
            self.lines.append(
                Line(
                    self.vertices[i],
                    self.vertices[(i+1)%len(self.vertices)],
                    self.frame.palette_selector.palette().obstacle_color,
                    self.frame,
                ))

    def draw(self, surface):
        for line in self.lines:
            line.draw(surface)

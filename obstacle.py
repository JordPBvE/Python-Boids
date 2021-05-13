from boid import Boid
import pygame
from pygame import Color
from pygame.math import Vector2

class Circle():
    def __init__(self,
                pos = Vector2(0, 0),
                radius = 10,
                color = Color(0, 0, 0),
                visible = True,
                frame = None):
        self.frame = frame
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = visible

    def draw(self, surface):
        if (self.visible):
            pygame.draw.circle(surface, self.color, self.pos, self.radius)



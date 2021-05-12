from boid import Boid
import pygame
from pygame import Color
from pygame.math import Vector2

class Circle():
    def __init__(self,
                pos,
                radius,
                color,
                visible,
                frame = None):
        self.frame = frame
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = visible

    def draw(self, surface):
        if (self.visible):
            pygame.draw.circle(surface, self.color, self.pos, self.radius)



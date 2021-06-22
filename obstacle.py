import pygame
from pygame import Color
import math
from pygame.math import Vector2


class Circle:
    """Circle obstacle class

    Class attributes:
    pos: Vector2(int, int) -- the position (middle point) of the circle
    radius: int -- the radius (size) of the circle in pixels
    color: Color -- the color of the circle
    visible: bool -- whether the circle is visible or not
    frame: BoidFrame -- the boid frame within which the circle is contained
    strength: int -- the strength of the obstacle's repelling force
    permanent: bool -- whether the obstacle is permanent (for example the
    circles that make up the walls); that is, it cannot be deleted through user
    input, after it's been created
    """

    def __init__(
        self,
        pos=Vector2(0, 0),
        radius=10,
        color=Color(0, 0, 0),
        visible=True,
        frame=None,
        strength=1,
        permanent=False,
    ):
        self.frame = frame
        self.pos = pos
        self.radius = radius
        self.color = color
        self.visible = visible
        self.strength = strength
        self.permanent = permanent

    def draw(self, surface):
        """Draw the circle to the surface."""
        if self.visible:
            pygame.draw.circle(
                surface,
                self.frame.palette_selector.palette().obstacle_color,
                self.pos,
                self.radius,
            )


class Line:
    """Line obstacle class

    Class attributes:
    begin_pos: Vector2(int, int) -- the starting point of the line
    end_pos: Vector2(int, int) -- the end of the line
    color: Color -- the color of the line
    frame: BoidFrame -- the boid frame within which the line is contained
    circles: list[Boid] -- the circles that make up the line
    circle_radius: int -- radius in pixels of the circles that make up the line
    length: int -- the length of the line
    permanent: bool -- whether the line is permanent (for example walls); that
    is, it cannot be deleted through user input, after it's been created
    """

    def __init__(self, begin_pos, end_pos, color, frame, permanent=False):
        self.begin_pos = begin_pos
        self.end_pos = end_pos
        self.color = color
        self.frame = frame
        self.circles = []
        self.circle_radius = 10
        self.length = (begin_pos - end_pos).length()
        self.permanent = permanent

        self.populate()

    def populate(self):
        """Create the circles that make up the line obstacle."""
        circle_count = math.floor(self.length / (2 * self.circle_radius))
        step = (self.end_pos - self.begin_pos) / circle_count
        circle_pos = self.begin_pos

        for i in range(circle_count + 1):
            circle = Circle(
                pos=circle_pos,
                radius=self.circle_radius,
                color=self.frame.palette_selector.palette().obstacle_color,
                visible=False,
                frame=self.frame,
                strength=0.1,
            )
            self.circles.append(circle)
            circle_pos = self.begin_pos + i * step

    def draw(self, surface):
        """Draw line."""
        pygame.draw.line(
            surface,
            self.frame.palette_selector.palette().obstacle_color,
            self.begin_pos,
            self.end_pos,
            width=2,
        )
        for circle in self.circles:
            circle.draw(surface)


class Polygon:
    """Polygon obstacle class

    Class attributes:
    color: Color -- the RGB color of the polygon
    lines: list[Line] -- the lines that make up the polygon
    vertices: list[Vector2(int, int)] -- the vertices that make up the line
    color: Color -- the RGB color of the polygon
    permanent: bool -- whether the polygon is permanent; that is, it cannot be
    deleted through user input, after it's been created
    """

    def __init__(self, color, frame, vertices=[], lines=[], permanent=False):
        self.frame = frame
        self.lines = lines
        self.vertices = vertices
        self.color = color
        self.permanent = permanent

        self.create()

    def create(self):
        """Create the lines that make up the polygon."""
        for i in range(len(self.vertices)):
            self.lines.append(
                Line(
                    self.vertices[i],
                    self.vertices[(i + 1) % len(self.vertices)],
                    self.frame.palette_selector.palette().obstacle_color,
                    self.frame,
                )
            )

    def draw(self, surface):
        """Draw the polygon."""
        if len(self.vertices) == 2:
            pygame.draw.line(
                surface,
                self.frame.palette_selector.palette().obstacle_color,
                self.vertices[0],
                self.vertices[1],
                width=3
            )
        elif len(self.vertices) > 2:
            pygame.draw.polygon(
                surface,
                self.frame.palette_selector.palette().obstacle_color,
                self.vertices,
            )

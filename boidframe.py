import random
from datetime import datetime

import pygame
from pygame import Color
from pygame.math import Vector2

from boid import Boid
from framemodes import FrameModes
from obstacle import Line, Polygon
from util.palettes import PaletteSelector


class BoidFrame:
    """Class containing all information about the scene that is rendered.
    
    Class attributes:
    width: int -- the width of the frame (matching window resolution)
    height: int -- the height of the frame (matching window resolution)
    mode: int -- the mode that the application is in (default, build, etc.)
    boid_list: list[Boid] -- a list containing all boids
    palette_selector: PaletteSelector -- the palette selector that helps with
    changes of palettes
    paused: bool -- a flag indicating whether boid movement is paused or not
    obstacle_size: int -- the size of obstacles in pixels
    obstacle_list: list[Obstacle] -- a list containing all obstacles
    polygon_vertices: list[Vector2(int, int)] -- list of vertices that make up
    the polygon that is currently being built (when in polygon build mode)
    """
    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height
        self.mode = FrameModes.MODE_DEFAULT
        self.boid_list = []
        self.palette_selector = PaletteSelector()
        self.paused = False
        self.obstacle_size = 50
        self.obstacle_list = []
        self.polygon_vertices = []
        self.create_walls()

    def add_boid(self, boid):
        """Add a boid to the frame."""
        boid.color = random.choice(self.palette_selector.palette().boid_palette)
        self.boid_list.append(boid)
        boid.frame = self

    def add_obstacle(self, obstacle):
        """Add an obstacle to the frame"""
        self.obstacle_list.append(obstacle)
        obstacle.frame = self

    def do_step(self, dt, screen):
        """Do a step for the next frame.

        Arguments:
        dt -- the time passed since the last frame was rendered
        """
        screen.fill(self.palette_selector.palette().background_color)

        if not self.paused:
            for b in self.boid_list:
                b.do_step(dt)

        if self.mode == FrameModes.MODE_DEBUG:
            self.debug_draw_obstacle_connections(screen)
            self.debug_draw_neighbor_connections(screen)

        drawables = self.boid_list + self.obstacle_list
        for drawable in drawables:
            drawable.draw(screen)

        if self.mode == FrameModes.MODE_BUILD_POLYGON:
            # Draw the polygon obstacle that's being built
            if len(self.polygon_vertices) > 1:
                pygame.draw.polygon(
                    screen,
                    self.palette_selector.palette().obstacle_color,
                    self.polygon_vertices + [pygame.mouse.get_pos()],
                    width=3,
                )
            elif len(self.polygon_vertices) == 1:
                pygame.draw.line(
                    screen,
                    self.palette_selector.palette().obstacle_color,
                    self.polygon_vertices[0],
                    pygame.mouse.get_pos(),
                    width=3,
                )
        elif self.mode == FrameModes.MODE_BUILD:
            # Draw the circle obstacle that's being built
            pygame.draw.circle(
                screen,
                self.palette_selector.current_palette.obstacle_color,
                pygame.mouse.get_pos(),
                self.obstacle_size,
                width=3,
            )

    def update_colors(self):
        """Update colors of all objects to the appropriate palette color."""
        for obstacle in self.obstacle_list:
            obstacle.color = self.palette_selector.palette().obstacle_color
        for boid in self.boid_list:
            boid.color = random.choice(self.palette_selector.palette().boid_palette)

    def next_palette(self):
        """Change the palette to the next."""
        self.palette_selector.nxt()
        self.update_colors()

    def prev_palette(self):
        """Change the palette to the previous."""
        self.palette_selector.prv()
        self.update_colors()

    def create_walls(self):
        """Create walls around the borders of the frame/window."""
        new_walls = []
        new_walls.append(
            Line(
                Vector2(1, 1),
                Vector2(1, self.height - 1),
                self.palette_selector.palette().obstacle_color,
                self,
                permanent=True,
            )
        )
        new_walls.append(
            Line(
                Vector2(1, 1),
                Vector2(self.width - 1, 1),
                self.palette_selector.palette().obstacle_color,
                self,
                permanent=True,
            )
        )
        new_walls.append(
            Line(
                Vector2(1, self.height - 1),
                Vector2(self.width - 1, self.height - 1),
                self.palette_selector.palette().obstacle_color,
                self,
                permanent=True,
            )
        )
        new_walls.append(
            Line(
                Vector2(self.width - 1, 1),
                Vector2(self.width - 1, self.height - 1),
                self.palette_selector.palette().obstacle_color,
                self,
                permanent=True,
            )
        )
        if self.obstacle_list == []:
            self.obstacle_list += new_walls
        else:
            for i in range(len(new_walls)):
                self.obstacle_list[i] = new_walls[i]

    def create_polygon(self):
        """Create polygon from stored vertices."""
        self.obstacle_list.append(
            Polygon(
                color=self.palette_selector.palette().obstacle_color,
                frame=self,
                vertices=self.polygon_vertices,
                lines=[],
            )
        )

    def debug_draw_neighbor_connections(self, surface):
        """Debug: draw the connections between neighboring boids as lines."""
        for boid in self.boid_list:
            for neighbor in boid.neighbors:
                diff = boid.pos - neighbor.pos
                if diff.length() < boid.neighbor_radius:
                    pygame.draw.line(
                        surface,
                        pygame.Color(100, 100, 100),
                        boid.pos,
                        neighbor.pos,
                        width=1,
                    )

    def debug_draw_obstacle_connections(self, surface):
        """Debug: draw the connections between boids and obstacles as lines."""
        for boid in self.boid_list:
            for obstacle in boid.near_obstacles:
                diff = boid.pos - obstacle.pos
                if diff.length() < boid.neighbor_radius + obstacle.radius:
                    pygame.draw.line(
                        surface,
                        pygame.Color(200, 100, 100),
                        boid.pos,
                        obstacle.pos,
                        width=2,
                    )

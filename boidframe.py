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
    # A class containing all information about the scene:
    # boids, obstacles, colors, etc.
    def __init__(self, width=256, height=256):
        self.width = width
        self.height = height
        self.mode = FrameModes.MODE_DEFAULT
        self.polygon_vertices = []
        self.boid_list = []
        self.obstacle_list = []
        self.obstacle_size = 50
        self.palette_selector = PaletteSelector()
        self.paused = False
        self.create_walls()

    def add_boid(self, boid):
        boid.color = random.choice(self.palette_selector.palette().boid_palette)
        self.boid_list.append(boid)
        boid.frame = self

    def add_obstacle(self, obstacle):
        self.obstacle_list.append(obstacle)
        obstacle.frame = self

    def do_step(self, dt, screen):
        screen.fill(self.palette_selector.palette().background_color)

        if not self.paused:
            for b in self.boid_list:
                b.do_step(dt)

        if self.mode == FrameModes.MODE_DEBUG:
            # self.debug_print_collisions()
            self.debug_draw_neighbor_connections(screen)
            self.debug_draw_obstacle_connections(screen)

        drawables = self.boid_list + self.obstacle_list
        for drawable in drawables:
            drawable.draw(screen)

        if (
            self.mode == FrameModes.MODE_BUILD_POLYGON
            and len(self.polygon_vertices) > 1
        ):
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

        if self.mode == FrameModes.MODE_BUILD:
            pygame.draw.circle(
                screen,
                self.palette_selector.current_palette.obstacle_color,
                pygame.mouse.get_pos(),
                self.obstacle_size,
                width=3,
            )

    def update_colors(self):
        for obstacle in self.obstacle_list:
            obstacle.color = self.palette_selector.palette().obstacle_color
        for boid in self.boid_list:
            boid.color = random.choice(self.palette_selector.palette().boid_palette)

    def next_palette(self):
        self.palette_selector.nxt()
        self.update_colors()

    def prev_palette(self):
        self.palette_selector.prv()
        self.update_colors()

    def create_walls(self):
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
        self.obstacle_list.append(
            Polygon(
                color=self.palette_selector.palette().obstacle_color,
                frame=self,
                vertices=self.polygon_vertices,
                lines=[],
            )
        )

    def debug_draw_neighbor_connections(self, surface):
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

    def debug_print_collisions(self):
        # TODO: fix this, currently broken
        for obstacle in self.obstacle_list:
            collisions = 0
            for boid in self.boid_list:
                if (obstacle.pos - boid.pos).length() < obstacle.radius:
                    collisions += 1
            if collisions > 0:
                print(
                    f"{datetime.now()} | obstacle at pos {(obstacle.pos.x, obstacle.pos.y)} has {collisions} collisions. )"
                )

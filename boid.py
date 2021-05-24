import math
import copy
from random import randint
import pygame
from pygame import Color
from pygame.math import Vector2

from obstacle import Polygon, Line
from framemodes import FrameModes


class Boid:
    def __init__(
        self,
        frame=None,
        pos=Vector2(0, 0),
        size=6,
        velocity=Vector2(1, 1),
        max_speed=0.30,
        min_speed=0.15,
        color=Color(255, 255, 255),
    ):

        self.frame = frame
        self.neighbors = []
        self.near_obstacles = []
        self.checkradius = 150
        self.obstacle_radius = 2 * self.checkradius
        self.pos = pos
        self.size = size
        self.velocity = velocity
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.color = color

    def draw(self, surface):
        # draw boid with pygame
        s = (
            self.size * self.velocity.normalize()
        )  # use the normalized velocity vector to draw the head
        head = self.pos + s

        # makes a copy of s rotated 90 degrees to the right
        # deepcopy is used to prevent unintended changes to s
        s_right = copy.deepcopy(s)
        s_right.x, s_right.y = s_right.y, -s_right.x
        foot_1 = self.pos - s + 0.5 * s_right

        # same thing, but rotated 90 degrees to the left
        s_left = copy.deepcopy(s)
        s_left.x, s_left.y = -s_left.y, s_left.x
        foot_2 = self.pos - s + 0.5 * s_left

        # pygame.draw.circle(surface, self.color,self.pos, self.checkradius, width = 1)

        pygame.draw.polygon(surface, self.color, (head, foot_1, foot_2))

    def do_step(self, dt):
        self.change_velocity()
        self.pos = self.pos + dt * self.velocity
        self.pos.x = self.pos.x % self.frame.width
        self.pos.y = self.pos.y % self.frame.height

    def change_velocity(self):
        self.identify_neighbors()

        v1 = self.rule1()
        v2 = self.rule2()
        v3 = self.rule3()
        v4 = self.avoid_obstacles()
        v5 = self.move_toward_mouse()

        if self.frame.mode == FrameModes.MODE_FOLLOW_MOUSE:
            self.velocity = self.velocity + (v1 + v2 + v3 + v4) * 2 + v5 * 5
        else:
            self.velocity = self.velocity + v1 + v2 + v3 + v4 + v5

        magnitude = self.velocity.length()

        if magnitude > self.max_speed:
            self.velocity = self.velocity / (magnitude / self.max_speed)
        if magnitude < self.min_speed:
            self.velocity = self.velocity / (magnitude / self.min_speed)

    def identify_neighbors(self):
        self.neighbors = []
        for boid in self.frame.boid_list:
            diff = self.pos - boid.pos

            if diff.length() < self.checkradius:
                self.neighbors.append(boid)

        self.near_obstacles = []
        for obstacle in self.frame.obstacle_list:
            if isinstance(obstacle, Polygon):
                for l in obstacle.lines:
                    for o in l.circles:
                        diff = self.pos - o.pos
                        if diff.length() - o.radius < self.obstacle_radius:
                            self.near_obstacles.append(o)
            elif isinstance(obstacle, Line):
                for o in obstacle.circles:
                    diff = self.pos - o.pos
                    if diff.length() - o.radius < self.obstacle_radius:
                        self.near_obstacles.append(o)
            else:
                diff = self.pos - obstacle.pos

                if diff.length() - obstacle.radius < self.obstacle_radius:
                    self.near_obstacles.append(obstacle)

    def rule1(self):
        # Move towards the center of all boids
        com = Vector2(0, 0)
        neigborcount = len(self.neighbors)

        for boid in self.neighbors:
            com += boid.pos / neigborcount

        # difference vector between boid position and center of mass
        diff = (com - self.pos) / 6000

        # return Vector2(0,0)
        return diff

    def rule2(self):
        # Move away from neighbouring boids that are just a bit too close
        cumulative_diverging_vector = Vector2(0, 0)

        for boid in self.neighbors:
            diverging_vector = self.pos - boid.pos

            len = diverging_vector.length()

            if 0 < len < (self.size * 8):
                diverging_vector.x /= len
                diverging_vector.y /= len
                cumulative_diverging_vector += diverging_vector

        cumulative_diverging_vector += self.velocity / 2
        cumulative_diverging_vector /= 80

        # return Vector2(0,0)
        return cumulative_diverging_vector

    def rule3(self):
        # Allign with neighboring boids
        total_vector = Vector2(0, 0)

        for boid in self.neighbors:
            total_vector += boid.velocity

        average_neighbor_velocity = total_vector / len(self.neighbors)
        velocity_correction = (average_neighbor_velocity - self.velocity) / 60

        return velocity_correction

    def avoid_obstacles(self):
        # this factor (should be 0 <= factor <= 1) determines the distribution
        # between direct avoidance (moving directly away), and steering avoidance
        # (steering around obstacles)
        factor_direct = 0.4

        # calculate direct avoidance vector (moving directly away from obstacles)
        cumulative_diverging_direct = Vector2(0, 0)
        if factor_direct > 0:
            for obstacle in self.near_obstacles:
                diverging_vector = self.pos - obstacle.pos
                diverging_vector -= diverging_vector * (
                    obstacle.radius / diverging_vector.length()
                )
                if diverging_vector.length() < (self.size * 20):
                    strength = 1 / (diverging_vector.length() ** 2)
                    diverging_vector *= strength
                    cumulative_diverging_direct += diverging_vector
            cumulative_diverging_direct /= 2

        # calculate steering avoidance vector (steering around obstacles)
        cumulative_diverging_steering = Vector2(0, 0)
        if factor_direct < 1:
            for obstacle in self.near_obstacles:
                # "rename" variables to shorten the equation for d below
                px = self.pos.x
                py = self.pos.y
                mx = obstacle.pos.x
                my = obstacle.pos.y
                vx = self.velocity.x
                vy = self.velocity.y
                # d here is the distance from the midpoint of the obstacle to the
                # line through the midpoint of the boid with the direction of its
                # velocity vector
                d = lambda vvx, vvy: abs(
                    (vvy / vvx) * mx - my + (py - (vvy / vvx) * px)
                ) / (math.sqrt(1 + (vvy / vvx) ** 2))
                dist_vector_line_to_obstacle = d(vx, vy)

                to_obstacle = obstacle.pos - self.pos
                angle_with_obstacle = self.velocity.angle_to(to_obstacle)
                # the "+ 10" is there to make boids that would scratch the edge
                # of the obstacle also steer away
                is_obstacle_in_front = (
                    dist_vector_line_to_obstacle < obstacle.radius + 10
                    and abs(angle_with_obstacle) < 90
                )

                if is_obstacle_in_front:
                    dist_to_obstacle = (to_obstacle).length() - obstacle.radius
                    strength = math.sqrt(obstacle.radius) / dist_to_obstacle
                    # If the distance after turing left is smaller, turn right (since we're trying to increase the distance) - and vice versa
                    if angle_with_obstacle >= 0:
                        cumulative_diverging_steering += (
                            strength * self.velocity.rotate(-90)
                        )
                    else:
                        cumulative_diverging_steering += (
                            strength * self.velocity.rotate(90)
                        )
            # cumulative_diverging_steering *= 2

        return (
            factor_direct * cumulative_diverging_direct
            + (1 - factor_direct) * cumulative_diverging_steering
        )

    def move_toward_mouse(self):
        if self.frame.mode == FrameModes.MODE_FOLLOW_MOUSE:
            mouse_pos = Vector2()
            mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
            margin = 0.15
            mouse_pos.x = max(
                margin * self.frame.width,
                min(mouse_pos.x, self.frame.width * (1 - margin)),
            )
            mouse_pos.y = max(
                margin * self.frame.height,
                min(mouse_pos.y, self.frame.height * (1 - margin)),
            )
            diff = (mouse_pos - self.pos).normalize()
            return 0.005 * diff
        else:
            return Vector2(0, 0)

    def avoid_walls(self):
        return Vector2(0, 0)

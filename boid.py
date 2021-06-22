import math
import copy
import pygame
from pygame import Color
from pygame.math import Vector2

from obstacle import Polygon, Line
from framemodes import FrameModes


class Boid:
    """Boid object

    Class instance attributes:
    frame: BoidFrame -- the BoidFrame object within which the boid is contained
    pos: Vector2(int, int) -- the (2d) position vector of the boid
    size: int -- the size of the boid (from center to "head", in pixels)
    velocity: Vector2(float, float) -- the (2d) velocity vector of the boid
    max_speed: float -- maximum boid speed (maximum velocity vector length)
    min_speed: float -- minimum boid speed (minimum velocity vector length)
    color: Color -- the RGB color of the boid
    """

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
        self.pos = pos
        self.size = size
        self.velocity = velocity
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.color = color
        self.neighbor_radius = 150
        self.obstacle_radius = 2 * self.neighbor_radius
        self.neighbors = []
        self.near_obstacles = []

    def draw(self, surface):
        """Draw the boid to the given surface using pygame.

        Arguments:
        surface -- the surface that the boid should be rendered to
        """
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

        pygame.draw.polygon(surface, self.color, (head, foot_1, foot_2))

    def do_step(self, dt):
        """Do a step for the next frame, calculating velocity and moving.

        Arguments:
        dt -- the time passed since the last frame was rendered
        """
        # It's necessary to identify neighbors and obstacles for the
        # calculations
        self.identify_neighbors()
        self.identify_obstacles()
        # Update boid velocity and position
        self.change_velocity()
        self.pos = self.pos + dt * self.velocity
        # Teleport boid to opposite end of the screen if it goes off-screen.
        self.pos.x = self.pos.x % self.frame.width
        self.pos.y = self.pos.y % self.frame.height

    def change_velocity(self):
        """Change the velocity based on the 'boid algorithm'."""
        v_coh = self.get_cohesion_component()
        v_sep = self.get_separation_component()
        v_alg = self.get_alignment_component()
        v_avd = self.get_obstacle_avoidance_component()

        v_res = v_coh + v_sep + v_alg + v_avd
        if self.frame.mode == FrameModes.MODE_FOLLOW_MOUSE:
            v_mou = self.get_mouse_component()
            self.velocity = self.velocity + v_res * 2 + v_mou * 5
        else:
            self.velocity = self.velocity + v_res

        # Cap speed:
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        if speed < self.min_speed:
            self.velocity = self.velocity.normalize() * self.min_speed

    def identify_neighbors(self):
        """Find all the boid's neighbors."""
        self.neighbors = []
        for boid in self.frame.boid_list:
            diff = self.pos - boid.pos

            if diff.length() < self.neighbor_radius:
                self.neighbors.append(boid)

    def identify_obstacles(self):
        """Find obstacles within the boid's obstacle radius."""
        self.near_obstacles = []
        for obstacle in self.frame.obstacle_list:
            if isinstance(obstacle, Polygon):
                for line in obstacle.lines:
                    for circle in line.circles:
                        diff = self.pos - circle.pos
                        diff_adjusted = diff.length() - circle.radius
                        if diff_adjusted < self.obstacle_radius:
                            self.near_obstacles.append(circle)
            elif isinstance(obstacle, Line):
                for circle in obstacle.circles:
                    diff = self.pos - circle.pos
                    if diff.length() - circle.radius < self.obstacle_radius:
                        self.near_obstacles.append(circle)
            else:
                diff = self.pos - obstacle.pos

                if diff.length() - obstacle.radius < self.obstacle_radius:
                    self.near_obstacles.append(obstacle)

    def get_cohesion_component(self):
        """Get velocity component that points to the center of all boids."""
        com = Vector2(0, 0)
        neigbor_count = len(self.neighbors)

        for boid in self.neighbors:
            com += boid.pos / neigbor_count

        # difference vector between boid position and center of mass
        diff = (com - self.pos) / 6000

        return diff

    def get_separation_component(self):
        """Get velocity component that separates boids that are too close."""
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

        return cumulative_diverging_vector

    def get_alignment_component(self):
        """Get velocity component that aligns boid velocity with neighbors."""
        total_vector = Vector2(0, 0)

        for boid in self.neighbors:
            total_vector += boid.velocity

        average_neighbor_velocity = total_vector / len(self.neighbors)
        velocity_correction = (average_neighbor_velocity - self.velocity) / 60

        return velocity_correction

    def obstacle_avoid_direct(self):
        result = Vector2(0, 0)
        for obstacle in self.near_obstacles:
            diverging_vector = self.pos - obstacle.pos
            diverging_vector -= diverging_vector * (
                obstacle.radius / diverging_vector.length()
            )
            if diverging_vector.length() < (self.size * 20):
                strength = 1 / (diverging_vector.length() ** 2)
                diverging_vector *= strength
                result += diverging_vector
        result /= 2
        return result

    def obstacle_avoid_steering(self):
        result = Vector2(0, 0)
        for obstacle in self.near_obstacles:
            # "rename" variables to shorten the equation for
            # `dist_vector_line_to_obstacle` below
            px = self.pos.x
            py = self.pos.y
            ox = obstacle.pos.x
            oy = obstacle.pos.y
            q = self.velocity.y/self.velocity.x
            # d here is the distance from the midpoint of the obstacle to
            # the line through the midpoint and head of the boid
            dist_vector_line_to_obstacle = (
                abs((q) * ox - oy + (py - (q) * px))
                / (math.sqrt(1 + (q) ** 2))
            )

            to_obstacle = obstacle.pos - self.pos
            angle_with_obstacle = self.velocity.angle_to(to_obstacle)
            # the "+ 10" is there to make boids that would scratch the edge
            # of the obstacle also steer away
            is_obstacle_in_front = (
                dist_vector_line_to_obstacle < obstacle.radius + 10
                and abs(angle_with_obstacle) < 90
            )

            if is_obstacle_in_front:
                dist_to_obstacle = to_obstacle.length() - obstacle.radius
                # The below formula was the result of experimentation
                strength = math.sqrt(obstacle.radius) / dist_to_obstacle
                # If the angle to the obstacle is nonnegative, turn right,
                # otherwise turn left
                if angle_with_obstacle >= 0:
                    result += (
                        strength * self.velocity.rotate(-90)
                    )
                else:
                    result += (
                        strength * self.velocity.rotate(90)
                    )
        return result

    def get_obstacle_avoidance_component(self, factor_direct=0.6):
        """Get velocity component that steers the boid around obstacles.

        Arguments:
        factor_direct: int -- a value between 0 and 1 that determines the
        distribution between direct avoidance (moving directly away) and
        steering avoidance steering around obstacles. A value of 1 results in
        direct avoidance exclusively, 0 results in just steering avoidance.
        """
        # calculate direct avoidance vector (directly away from obstacles)
        cumulative_diverging_direct = Vector2(0, 0)
        if factor_direct > 0:
            cumulative_diverging_direct = self.obstacle_avoid_direct()

        # calculate steering avoidance vector (steering around obstacles)
        cumulative_diverging_steering = Vector2(0, 0)
        if factor_direct < 1:
            cumulative_diverging_steering = self.obstacle_avoid_steering()
        return (
            factor_direct * cumulative_diverging_direct
            + (1 - factor_direct) * cumulative_diverging_steering
        )

    def get_mouse_component(self, margin=0.15):
        """Calculate the velocity component that moves toward mouse cursor.

        Keyword arguments:
        margin: float -- the factor of screen space that should be considered
        margin, that is: space that the mouse cannot enter
        """
        mouse_pos = Vector2()
        mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
        # Cap the mouse position to prevent boids from
        # flying off screen when following the mouse
        mouse_pos.x = max(
            margin * self.frame.width,
            min(mouse_pos.x, self.frame.width * (1 - margin)),
        )
        mouse_pos.y = max(
            margin * self.frame.height,
            min(mouse_pos.y, self.frame.height * (1 - margin)),
        )
        # Calculate difference and normalize (so that the)
        # distance to the mouse doesn't affect the strength
        # of the mouse pull
        diff = (mouse_pos - self.pos).normalize()
        return 0.005 * diff

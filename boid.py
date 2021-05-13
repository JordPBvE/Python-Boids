import math
import copy
from random import randint
import pygame
from pygame import Color
from pygame.math import Vector2

class Boid:
    def __init__(self,
                frame = None,
                pos = Vector2(0, 0),
                size = 8,
                velocity = Vector2(1,1),
                max_speed = 0.30,
                color = Color(255,255,255),): 

        self.frame = frame
        self.neighbors = []
        self.near_obstacles = []
        self.checkradius = 150
        self.pos = pos
        self.size = size
        self.velocity = velocity
        self.max_speed = max_speed
        self.color = color


    def draw(self, surface):
        # draw boid with pygame
        s = self.size * self.velocity.normalize() # use the normalized velocity vector to draw the head
        head = self.pos + s

        # makes a copy of s rotated 90 degrees to the right
        # deepcopy is used to prevent unintended changes to s
        s_right = copy.deepcopy(s) 
        s_right.x, s_right.y = s_right.y, -s_right.x 
        foot_1 = self.pos - s + 0.5 * s_right

        # same thing, but rotated 90 degrees to the left
        s_left = copy.deepcopy(s)
        s_left.x , s_left.y = -s_left.y, s_left.x 
        foot_2 = self.pos - s + 0.5 * s_left
        
        # pygame.draw.circle(surface, self.color,self.pos, self.checkradius, width = 1)
        
        # for boid in self.neighbors:
        #     diff = self.pos - boid.pos
        #     if diff.length() < self.checkradius:
        #         pygame.draw.line(surface, pygame.Color(100, 100, 100), self.pos, boid.pos, width = 1)

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

        self.velocity = self.velocity + v1 + v2 + v3 + v4

        magnitude = self.velocity.length()

        if magnitude > self.max_speed:
            self.velocity = self.velocity / (magnitude/self.max_speed)

    def identify_neighbors(self):
        self.neighbors = []
        for boid in self.frame.boid_list:
            diff = self.pos - boid.pos

            if diff.length() < self.checkradius:
                self.neighbors.append(boid)

        self.near_obstacles = []
        for obstacle in self.frame.obstacle_list:
            diff = self.pos - obstacle.pos

            if diff.length() - obstacle.radius < self.checkradius:
                self.near_obstacles.append(obstacle)


    def rule1(self): 
        # Move towards the center of all boids
        com = Vector2(0,0)
        neigborcount = len(self.neighbors)

        for boid in self.neighbors:
            com += boid.pos/neigborcount
        
        # difference vector between boid position and center of mass
        diff = (com - self.pos)/6000

        # return Vector2(0,0)
        return diff


    def rule2(self):
        # Move away from neighbouring boids that are just a bit too close
        cumulative_diverging_vector = Vector2(0,0)

        for boid in self.neighbors:
            diverging_vector = self.pos - boid.pos

            len = diverging_vector.length()

            if  0 < len < (self.size * 8):
                diverging_vector.x /= len
                diverging_vector.y /= len
                cumulative_diverging_vector += diverging_vector
            
        cumulative_diverging_vector += self.velocity/2
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
        cumulative_diverging_vector = Vector2(0,0)

        for obstacle in self.near_obstacles:
            px = self.pos.x
            py = self.pos.y
            mx = obstacle.pos.x
            my = obstacle.pos.y
            vx = self.velocity.x
            vy = self.velocity.y
            d = lambda vvx, vvy: abs((vvy/vvx) * mx - my + (py - (vvy/vvx) * px)) / (math.sqrt(1 + (vvy/vvx)**2))
            dist_vector_line_to_obstacle = d(vx, vy)

            # Use radius slightly bigger than that of the obstacle, makes it look more natural
            rad = obstacle.radius + 5

            vect_self_to_obstacle = (self.pos - obstacle.pos)
            is_obstacle_detectable = vect_self_to_obstacle.length() < (4 * rad)
            vect_self_to_obstacle -= vect_self_to_obstacle * (rad/vect_self_to_obstacle.length())

            is_obstacle_in_front = dist_vector_line_to_obstacle < rad

            if is_obstacle_detectable and is_obstacle_in_front:
                strength = math.sqrt(rad) / (vect_self_to_obstacle.length())
                right_component =  strength * self.velocity.rotate(-90)
                left_component = strength * self.velocity.rotate(90)
                right_rotated_vector = self.velocity + right_component
                left_rotated_vector = self.velocity + left_component
                # If the distance after turing left is smaller, turn right (since we're trying to increase the distance) - and vice versa
                if d(left_rotated_vector.x, left_rotated_vector.y) <= d(right_rotated_vector.x, right_rotated_vector.y):
                    cumulative_diverging_vector += right_component
                else:
                    cumulative_diverging_vector += left_component
            
        cumulative_diverging_vector *= 2
        return cumulative_diverging_vector




    def avoid_walls(self):
        
        return Vector2(0,0)



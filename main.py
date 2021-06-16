import sys
import math
import random
import pygame
from pygame import Color
from pygame.math import Vector2

from boid import Boid
from boidframe import BoidFrame
from obstacle import Line
from util.input import *
from messagedisplay import MessageDisplay


def main():
    width = 1080
    height = 720

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    pygame.display.set_caption("    [boids]")
    pygame.init()

    frame = BoidFrame(width=width, height=height)
    message_display = MessageDisplay()

    # Create boids:
    boid_count = 40
    for i in range(boid_count):
        random_pos = Vector2(
            random.randint(10, width - 10), random.randint(10, height - 10)
        )
        random_velocity = Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        frame.add_boid(
            Boid(
                pos=random_pos,
                velocity=random_velocity,
                max_speed=random.uniform(0.2, 0.3),
            )
        )

    should_run = True
    while should_run:
        dt = clock.tick(60)
        frame.do_step(dt, screen)
        message_display.render_message(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                process_mouse_event(event, frame, message_display)
            elif event.type == pygame.KEYDOWN:
                process_key_event(event, frame, message_display)
            elif event.type == pygame.VIDEORESIZE:
                process_resize_event(event, screen, frame)
        pygame.display.update()


if __name__ == "__main__":
    main()

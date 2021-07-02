import random
import pygame
from pygame.math import Vector2

from boid import Boid
from boidframe import BoidFrame
from util.messagedisplay import MessageDisplay
from util.input import (
    process_mouse_event, process_key_event, process_resize_event
)


def main():
    width = 1080
    height = 720

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    pygame.display.set_caption("    [boids]")
    pygame.init()

    boid_frame = BoidFrame(width=width, height=height)
    message_display = MessageDisplay()
    message_display.show_message("[ b o i d s ]")

    # Create boids:

    # ================= CHANGE BOID COUNT ================
    boid_count = 40
    # ====================================================

    # Leave a margin for the boids positions, so that they
    # don't spawn on the edge of the screen
    border_margin = 20
    for _ in range(boid_count):
        random_pos = Vector2(
            random.randint(border_margin, width - border_margin),
            random.randint(border_margin, height - border_margin),
        )
        random_velocity_x = random.uniform(-0.5, 0.5)
        random_velocity_y = random.uniform(-0.5, 0.5)
        random_velocity = Vector2(random_velocity_x, random_velocity_y)
        boid_frame.add_boid(
            Boid(
                pos=random_pos,

                # ================= CHANGE BOID SIZE =================
                size = 6,
                # ====================================================

                velocity=random_velocity,
                max_speed=random.uniform(0.2, 0.3),
            )
        )

    should_run = True
    while should_run:
        # The clock is used to keep track of the time between each frame
        dt = clock.tick(60)
        boid_frame.do_step(dt, screen)
        message_display.render_message(screen)
        # Handle events (such as input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                process_mouse_event(event, boid_frame, message_display)
            elif event.type == pygame.KEYDOWN:
                process_key_event(event, boid_frame, message_display)
            elif event.type == pygame.VIDEORESIZE:
                process_resize_event(event, screen, boid_frame)
        pygame.display.update()


if __name__ == "__main__":
    main()

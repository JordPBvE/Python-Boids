import pygame
from pygame.math import Vector2

from obstacle import Circle
from util.palettes import get_random_color_palette

def process_mouse_event(event, boidFrame):
    pressed = pygame.mouse.get_pressed()[ 0 ]
    position = Vector2()
    position.x, position.y = pygame.mouse.get_pos()

    if pressed and boidFrame.build_mode:
        new_circle = Circle(position, boidFrame.obstacle_size, pygame.Color(230, 20, 0), True)
        new_circle.frame = boidFrame
        boidFrame.obstacle_list.append(new_circle)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:
            if boidFrame.obstacle_size < 300:
                boidFrame.obstacle_size *= 1.2
        elif event.button == 5:
            if boidFrame.obstacle_size > 10:
                boidFrame.obstacle_size /= 1.2

def process_key_event(event, frame):
    if event.key == pygame.K_r:
        frame.obstacle_list = []
        frame.create_walls()
    if event.key == pygame.K_d:
        frame.debug_mode = not frame.debug_mode
    if event.key == pygame.K_b:
        frame.build_mode = not frame.build_mode
    if event.key == pygame.K_p:
        frame.change_color_palette(get_random_color_palette())

def process_resize_event(event, screen, frame):
    frame.width = event.w
    frame.height = event.h
    frame.create_walls()

import pygame
from pygame.math import Vector2

from obstacle import Circle
import util.palettes 
from boidframe import BoidFrame

def process_mouse_event(event, boidFrame):
    mouse_pos = Vector2()
    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()

    if boidFrame.mode == BoidFrame.MODE_DEFAULT:
        handle_mouse_input_mode_default(event, boidFrame)
    elif boidFrame.mode == BoidFrame.MODE_DEBUG:
        pass
    elif boidFrame.mode == BoidFrame.MODE_BUILD:
        handle_mouse_input_mode_build(event, boidFrame, mouse_pos)
    elif boidFrame.mode == BoidFrame.MODE_BUILD_POLYGON:
        pass
        ###############################################
        ## Add vertex to polygon that is being drawn ##
        ###############################################


def handle_mouse_input_mode_default(event, boidFrame):
    pass


def handle_key_input_mode_default(event, boidFrame):
    pass


def handle_mouse_input_mode_build(event, boidFrame, mouse_pos):
    # get the tuple of values for which mouse button was clicked
    # e.g. (True, False, False) when only LMB was pressed
    buttons_pressed = pygame.mouse.get_pressed()
    if buttons_pressed[0]: # LMB
        new_circle = Circle(mouse_pos, boidFrame.obstacle_size, boidFrame.color_palette[-1], True)
        new_circle.frame = boidFrame
        boidFrame.obstacle_list.append(new_circle)
    if buttons_pressed[1]: # RMB
        boidFrame.mode = BoidFrame.MODE_BUILD_POLYGON
    # Handle scroling:
    if event.button == 4:
        if boidFrame.obstacle_size < 300:
            boidFrame.obstacle_size *= 1.2
    elif event.button == 5:
        if boidFrame.obstacle_size > 10:
            boidFrame.obstacle_size /= 1.2


def handle_key_input_mode_build(event, boidFrame):
    if event.key == pygame.K_r:
        boidFrame.obstacle_list = []
        boidFrame.create_walls()


def process_key_event(event, boidFrame):
    if boidFrame.mode == BoidFrame.MODE_DEFAULT:
        handle_key_input_mode_default(event, boidFrame)
    elif boidFrame.mode == BoidFrame.MODE_DEBUG:
        pass
    elif boidFrame.mode == BoidFrame.MODE_BUILD:
        handle_key_input_mode_build(event, boidFrame)
    elif boidFrame.mode == BoidFrame.MODE_BUILD_POLYGON:
        pass

    if event.key == pygame.K_p:
        boidFrame.change_color_palette(util.palettes.get_random_color_palette())
    if event.key == pygame.K_d:
        boidFrame.mode = BoidFrame.MODE_DEBUG
    if event.key == pygame.K_b:
        boidFrame.mode = BoidFrame.MODE_BUILD
    if event.key in (pygame.K_q, pygame.K_ESCAPE):
        boidFrame.mode = BoidFrame.MODE_DEFAULT


def process_resize_event(event, screen, frame):
    frame.width = event.w
    frame.height = event.h
    frame.create_walls()

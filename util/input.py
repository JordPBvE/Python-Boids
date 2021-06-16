import pygame
from pygame.math import Vector2

from obstacle import Circle
import util.palettes
from boidframe import BoidFrame
from framemodes import FrameModes


def process_mouse_event(event, boidFrame, message_display):
    mouse_pos = Vector2()
    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()

    if boidFrame.mode == FrameModes.MODE_DEFAULT:
        handle_mouse_input_mode_default(event, boidFrame)
    elif boidFrame.mode == FrameModes.MODE_DEBUG:
        pass
    elif boidFrame.mode == FrameModes.MODE_BUILD:
        handle_mouse_input_mode_build(event, boidFrame, mouse_pos)
    elif boidFrame.mode == FrameModes.MODE_BUILD_POLYGON:
        handle_mouse_input_mode_build_polygon(event, boidFrame, mouse_pos)


def handle_mouse_input_mode_default(event, boidFrame):
    pass


def handle_key_input_mode_default(event, boidFrame, message_display):
    if event.key == pygame.K_m:
        boidFrame.mode = FrameModes.MODE_FOLLOW_MOUSE
        message_display.show_message("Mouse following mode activated. Boids will now follow the mouse.")

def handle_mouse_input_mode_build_polygon(event, boidFrame, mouse_pos):
    buttons_pressed = pygame.mouse.get_pressed()
    if buttons_pressed[0]:  # LMB
        boidFrame.polygon_vertices.append(mouse_pos)
    if buttons_pressed[2]:  # RMB
        if len(boidFrame.polygon_vertices) > 1:
            boidFrame.create_polygon()
            boidFrame.polygon_vertices = []

def handle_mouse_input_mode_build(event, boidFrame, mouse_pos):
    # get the tuple of values for which mouse button was clicked
    # e.g. (True, False, False) when only LMB was pressed
    buttons_pressed = pygame.mouse.get_pressed()
    if buttons_pressed[0]:  # LMB
        new_circle = Circle(
            mouse_pos,
            boidFrame.obstacle_size,
            boidFrame.palette_selector.palette().obstacle_color,
            True,
        )
        new_circle.frame = boidFrame
        boidFrame.obstacle_list.append(new_circle)
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
    elif event.key == pygame.K_b:
        boidFrame.mode = FrameModes.MODE_DEFAULT


def process_key_event(event, boidFrame, message_display):
    if boidFrame.mode == FrameModes.MODE_DEFAULT:
        handle_key_input_mode_default(event, boidFrame, message_display)
    elif boidFrame.mode == FrameModes.MODE_FOLLOW_MOUSE:
        pass
    elif boidFrame.mode == FrameModes.MODE_DEBUG:
        pass
    elif boidFrame.mode == FrameModes.MODE_BUILD:
        handle_key_input_mode_build(event, boidFrame)
    elif boidFrame.mode == FrameModes.MODE_BUILD_POLYGON:
        handle_key_input_mode_build(event, boidFrame)


    if event.key == pygame.K_p:
        boidFrame.paused = not boidFrame.paused
        msg = "Paused." if boidFrame.paused else "Resumed."
        message_display.show_message(msg, 1)
    elif event.key == pygame.K_RIGHT:
        boidFrame.next_palette()
        message_display.show_message(f"Switched to palette `{boidFrame.palette_selector.current_palette.name}`")
    elif event.key == pygame.K_LEFT:
        boidFrame.prev_palette()
        message_display.show_message(f"Switched to palette `{boidFrame.palette_selector.current_palette.name}`")
    elif event.key == pygame.K_d:
        boidFrame.mode = FrameModes.MODE_DEBUG
        message_display.show_message("Enabled debug mode.", 2)
    elif event.key == pygame.K_b:
        boidFrame.mode = FrameModes.MODE_BUILD
        message_display.show_message("Build mode activated; left click to place an obstacle, use scrollwheel to adjust size.", 4)
    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
        boidFrame.mode = FrameModes.MODE_DEFAULT
        message_display.show_message("Now in default mode.", 2)
    elif event.key == pygame.K_BACKSPACE: 
        if not boidFrame.obstacle_list[-1].permanent:
            boidFrame.obstacle_list.pop()
    if event.key == pygame.K_SPACE:
        if boidFrame.mode == FrameModes.MODE_BUILD_POLYGON:
            boidFrame.mode = FrameModes.MODE_BUILD
            message_display.show_message("You can now place circular obstacles")
        elif boidFrame.mode == FrameModes.MODE_BUILD:
            boidFrame.mode = FrameModes.MODE_BUILD_POLYGON
            message_display.show_message("You can now place Polygons")


def process_resize_event(event, screen, boidFrame):
    boidFrame.width = event.w
    boidFrame.height = event.h
    boidFrame.create_walls()

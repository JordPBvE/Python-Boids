import pygame
from obstacle import Circle

def process_mouse_event(event, boidFrame):
    pressed = pygame.mouse.get_pressed()[ 0 ]
    position = pygame.mouse.get_pos()

    if pressed:
        new_circle = Circle(position, boidFrame.obstacle_size, pygame.Color(230, 20, 0), True)
        new_circle.frame = boidFrame
        boidFrame.obstacle_list.append(new_circle)


def process_key_pressed(boidFrame, surface):
    factor = 1.02
    keys = pygame.key.get_pressed()  #checking pressed keys

    if keys[pygame.K_UP]:
        if boidFrame.obstacle_size < 300:
            boidFrame.obstacle_size *= factor

        pygame.draw.circle(surface, (255, 255, 255), pygame.mouse.get_pos(), boidFrame.obstacle_size, width = 1)

    if keys[pygame.K_DOWN]:
        if boidFrame.obstacle_size > 10:
            boidFrame.obstacle_size /= factor

        pygame.draw.circle(surface, (255, 255, 255), pygame.mouse.get_pos(), boidFrame.obstacle_size, width = 1)

def process_key_event(event, frame):
    if event.key == pygame.K_r:
        frame.obstacle_list = []
        

def process_resize_event(event, screen, frame):
    frame.width = event.w
    frame.height = event.h

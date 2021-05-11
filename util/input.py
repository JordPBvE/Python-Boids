import pygame

def process_keydown_event(event, boidFrame):
    if event.key == pygame.K_UP:
        for boid in boidFrame.boid_list:
            boid.pos.y -= boidFrame.height / 10
    elif event.key == pygame.K_DOWN:
        for boid in boidFrame.boid_list:
            boid.pos.y += boidFrame.height / 10

def process_resize_event(event, screen, frame):
    frame.width = event.w
    frame.height = event.h

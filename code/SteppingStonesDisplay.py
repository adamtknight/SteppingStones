import os
import random
import pygame
import math
import sys
import asyncio
import qtm
import main

def start_program():
    asyncio.ensure_future(main.setup())
    asyncio.get_event_loop().run_forever()
    
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    stone_counter = 0
    screen_width = 1500
    screen_height = 600

    # Indicates pygame is running
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Stepping Stones")

    # object current co-ordinates 
    x = 200
    y = 200
    
    # dimensions of the object 
    stone_width = 50
    stone_height = 20

    #height on screen of the object
    left_stone_height = 100
    right_stone_height = 150

    # velocity / speed of movement
    vel = 1

    #step length of the participant in pixels
    step_length = 100

    #list of stones
    stones = []

    clock = pygame.time.Clock()

    class Stone(object):
        def __init__(self, x, side):
            self.x = x
            self.side = side
            
        def draw(self, surface):
            if self.side == "left":
                pygame.draw.rect(surface, (223, 50, 223), (self.x,left_stone_height, stone_width, stone_height))
            else:
                pygame.draw.rect(surface, (223, 50, 223), (self.x,right_stone_height, stone_width, stone_height))
    

    side = "right"
    stones.append(Stone(1, side))  
    prev_stone = stones[0]      
    running = True 
    
    while running:
        
        screen.fill((255, 255, 255))
        if(prev_stone.x > step_length):
            if side == "left" : side = "right"
            else: side = "left"
            stones.append(Stone(1, side))
            prev_stone = stones[len(stones) - 1] 
        dt = clock.tick(1000)
        for stone in stones:
            if stone.x < screen_width and stone.x > 0:
                stone.x = stone.x + vel * dt
                stone.draw(screen)
            else:
                stones.pop(stones.index(stone))
    

        pygame.display.update()
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

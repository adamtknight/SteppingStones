import pygame
import os
from typing import List

# Initialize pygame library and center the screen
pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Set some initial variables
stone_counter = 0
screen_width = 1000
screen_height = 500

# Create the screen and set the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stepping Stones")

# Initialize object coordinates, dimensions, and velocity
x = 200
y = 200
stone_width = 100
stone_height = 60
left_stone_height = 100
right_stone_height = 200
vel = 1
step_length = 100
stones = []

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

class Stone:
    def __init__(self, x: int, side: str) -> None:
        """
        Initializes a new stone object with the given x-coordinate and side
        """
        self.x = x
        self.side = side

    def draw(self, surface) -> None:
        """
        Draws the stone on the given surface
        """
        if self.side == "left":
            pygame.draw.rect(surface, (223, 50, 223), (self.x,left_stone_height, stone_width, stone_height))
        else:
            pygame.draw.rect(surface, (223, 50, 223), (self.x,right_stone_height, stone_width, stone_height))

side = "right"
stones.append(Stone(1, side))  
prev_stone = stones[0]      
running = True 
# Create a new surface for the stone
stone_surface = pygame.Surface((stone_width, stone_height))

# Draw the stone to the surface
pygame.draw.rect(stone_surface, (223, 50, 223), (0, 0, stone_width, stone_height))

# Convert the surface to display format
stone_surface = stone_surface.convert()

running = True 
while running:
    # Clear the screen
    screen.fill((255, 255, 255))
    #add new stones
    if(prev_stone.x > step_length):
        if side == "left" : side = "right"
        else: side = "left"
        stones.append(Stone(1, side))
        prev_stone = stones[len(stones) - 1] 
    # update the position of stones
    for stone in stones:
        if stone.x < screen_width and stone.x > 0:
            stone.x = stone.x + vel
            screen.blit(stone_surface, (stone.x, stone.side == "left" and left_stone_height or right_stone_height))
        else:
            stones.pop(stones.index(stone))
    # Update the screen
    pygame.display.update()
    # process events in the background
    pygame.event.pump()
    # Check for a quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

import asyncio
import csv
import random # library for asynchronous programming
import sys # library for system-specific parameters and functions
import qtm # library for connecting to the QTM server
import pygame # library for creating GUI elements
import os
import win32api

##########IMPORTANT############

#Screen 1 resolution = 1900x1200
#Screen 2 resolution = 1280x800
#Extend screens and ensure screen 2 (The Projector) is in top right corner
#Can be found in the display settings of this computer

####INPUT VALUES#####

TREADMILL_SPEED_RIGHT = 1.25 # m/s
TREADMILL_SPEED_LEFT = 1.25 # m/s
STEP_LENGTH_RIGHT = 0.67 # m
STEP_LENGTH_LEFT = 0.67 # m
STEP_WIDTH = 0.3 # m
STONE_WIDTH = 0.3 # m
STONE_HEIGHT = 0.15 # m
COLLECTION_TIME = 5 # s
FREQUENCY = 100 # frames/sec

RIGHT_SHIFT_BACK_DIST = 0.1 # m
RIGHT_SHIFT_FORWARD_DIST = 0.1 # m
RIGHT_SHIFT_RIGHT_DIST = 0.15 # m
RIGHT_SHIFT_LEFT_DIST = 0.15 # m

LEFT_SHIFT_BACK_DIST = 0.1 # m
LEFT_SHIFT_FORWARD_DIST = 0.1 # m
LEFT_SHIFT_RIGHT_DIST = 0.15 # m
LEFT_SHIFT_LEFT_DIST = 0.15 # m

FILEPATH_TO_STEPPATH = "C:/Users/Neurolab/Documents/Projects/Knight/SteppingStones/code/Temp_Main/TEST"


# Initialize pygame library and position the screen

pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1920, 360"


# Set some initial variables

screen_width = 1250
screen_height = 400

# Create the screen and set the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stepping Stones")


# Initialize object coordinates, dimensions, and velocity
# TODO
x = 0
y = 0
step_width = STEP_WIDTH * 331.3
stone_width= STONE_WIDTH * 331.3
stone_height = STONE_HEIGHT * 331.3
left_stone_y = 204 - stone_height/2 + step_width/2
right_stone_y = 204 - stone_height/2 - step_width/2
vel_left = TREADMILL_SPEED_LEFT * 331.3
vel_right = TREADMILL_SPEED_RIGHT* 331.3
step_length_left = STEP_LENGTH_LEFT * 331.3
step_length_right = STEP_LENGTH_RIGHT * 331.3
rsbd = RIGHT_SHIFT_BACK_DIST* 331.3
rsfd = RIGHT_SHIFT_FORWARD_DIST * 331.3
rsrd = RIGHT_SHIFT_RIGHT_DIST * 331.3
rsld = RIGHT_SHIFT_LEFT_DIST * 331.3
lsbd = LEFT_SHIFT_BACK_DIST * 331.3
lsfd = LEFT_SHIFT_FORWARD_DIST * 331.3
lsrd = LEFT_SHIFT_RIGHT_DIST * 331.3
lsld = LEFT_SHIFT_LEFT_DIST * 331.3

stone_path_arr = []
stones = []
TL_x, TL_y,TR_x, TR_y,BL_x, BL_y,BR_x, BR_y = 649,20,1139, 25 ,648,386,1140,389

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# clear the screen
screen.fill((255, 255, 255))
# Draw the 4 circles at the corners of the screen
pygame.draw.circle(screen, (255, 0, 0), (TL_x, TL_y), 1)
pygame.draw.circle(screen, (255, 0, 0), (TR_x, TR_y), 1)
pygame.draw.circle(screen, (255, 0, 0), (BL_x, BL_y), 1)
pygame.draw.circle(screen, (255, 0, 0), (BR_x, BR_y), 1)

# Draw the text message asking the user to press enter to start
font = pygame.font.Font(None, 30)
text = font.render("Press enter to start...", True, (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (screen_width // 2, screen_height // 2)
screen.blit(text, text_rect)

pygame.display.flip() 

#Align the Screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        break

# clear the screen
screen.fill((255, 255, 255))

#Refresh Screen When Complete
pygame.display.flip()


#Class for stepping stone
class Stone:
    def __init__(self, x: int, y: int, side: str, id: int, pertrubed: int ) -> None:
        """
        Initializes a new stone object with the given x-coordinate, side, ID, and Pertrubed
        """
        self.x = x
        self.y = y
        self.side = side
        self.id=stone_counter
        self.pertrubed = pertrubed
        self.color = (252, 3, 148)

    def draw(self, surface) -> None:
        """
        Draws the stone on the given surface
        """
        if self.side == "left":
            pygame.draw.rect(surface, self.color, (self.x,self.y, stone_width, stone_height))
        else:
            pygame.draw.rect(surface, self.color, (self.x,self.y, stone_width, stone_height))

global circle_x, circle_y, frame_number, stone_counter, color

# set the pertrubed array
try:
    with open(FILEPATH_TO_STEPPATH, "r") as file:
        content = file.read()
        stone_path_arr = [int(x) for x in content.split()]
except FileNotFoundError:
    print("file not found")


stone_counter = 0
side = "right"
stone_counter+=1
init_stone = Stone(x, right_stone_y, side, stone_counter, stone_path_arr[stone_counter-1])
stones.append(init_stone)
prev_stone = stones[0]

running = True
while running:
    # process events that have occured
    pygame.event.pump()

    # Check if pygame screen has been exited
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            asyncio.get_event_loop().stop()

    # clear the screen
    screen.fill((255, 255, 255))

    #add new stone if needed
    if side == "right" and prev_stone.x > step_length_left :
        if side == "left" : side = "right"
        else: side = "left"
        stone_counter+=1
        stones.append(Stone(0, left_stone_y, side, stone_counter, stone_path_arr[stone_counter-1]))
        prev_stone = stones[len(stones) - 1]
    elif side == "left" and prev_stone.x > step_length_right :
        if side == "left" : side = "right"
        else: side = "left"
        stone_counter+=1
        stones.append(Stone(0, right_stone_y, side, stone_counter, stone_path_arr[stone_counter-1]))
        prev_stone = stones[len(stones) - 1]
    
    time_since_last_frame = clock.tick() / 1000 
    
    # calculate distance to move
    distance_to_move_right = vel_right * time_since_last_frame
    distance_to_move_left = vel_left * time_since_last_frame

    threshold = 375
    for stone in stones:
        if stone.x < screen_width and stone.x >= 0 and stone.side == "right":
            stone.x = stone.x + distance_to_move_right
            if stone.pertrubed and stone.x > threshold:
                if stone.pertrubed == 1:
                    stone.x = stone.x - rsbd
                elif stone.pertrubed == 2:
                    stone.x = stone.x + rsfd
                elif stone.pertrubed == 3:
                    stone.y = stone.y - rsrd
                elif stone.pertrubed == 4:
                    stone.y = stone.y + rsld
                stone.pertrubed = 0
                stone.color = (252, 3, 3)
            stone.draw(screen)
            
            
        elif stone.x < screen_width and stone.x >= 0 and stone.side == "left":
            stone.x = stone.x + distance_to_move_right
            if stone.pertrubed and stone.x > threshold:
                if stone.pertrubed == 5:
                    stone.x = stone.x - lsbd
                elif stone.pertrubed == 6:
                    stone.x = stone.x + lsfd
                elif stone.pertrubed == 7:
                    stone.y = stone.y - lsrd
                elif stone.pertrubed == 8:
                    stone.y = stone.y + lsld
                stone.pertrubed = 0
                stone.color = (252, 3, 3)
            stone.draw(screen)
            
        else:
            del_stone = stones.pop(stones.index(stone))
            del del_stone
    # update the display
    pygame.display.flip()

        






    
    





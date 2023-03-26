import asyncio
import atexit
import csv
import math
import random # library for asynchronous programming
import sys
import time # library for system-specific parameters and functions
import qtm # library for connecting to the QTM server
import pygame # library for creating GUI elements
import os
import win32api
import cv2
import numpy as np


##########IMPORTANT############

#Screen 1 resolution = 1900x1200
#Screen 2 resolution = 1280x800
#Extend screens and ensure screen 2 (The Projector) is in top right corner
#Can be found in the display settings of this computer

####INPUT VALUES#####

TREADMILL_SPEED_RIGHT = 1 # m/s
TREADMILL_SPEED_LEFT = 1 # m/s
STEP_LENGTH_RIGHT = 0.67 # m
STEP_LENGTH_LEFT = 0.67 # m
STEP_WIDTH = 0.3 # m
STONE_WIDTH = 0.3 # m
STONE_HEIGHT = 0.15 # m
COLLECTION_TIME = 5 # s
FREQUENCY = 100 # frames/sec

RIGHT_SHIFT_BACK_DIST = 0.5 # m
RIGHT_SHIFT_FORWARD_DIST = 0.5 # m
RIGHT_SHIFT_RIGHT_DIST = 0.15 # m
RIGHT_SHIFT_LEFT_DIST = 0.15 # m

LEFT_SHIFT_BACK_DIST = 0.5 # m
LEFT_SHIFT_FORWARD_DIST = 0.5 # m
LEFT_SHIFT_RIGHT_DIST = 0.15 # m
LEFT_SHIFT_LEFT_DIST = 0.15 # m
USE_THRESHOLD_MARKER = False

#Use distance from wall, ensure USE_THRESHOLD_MARKER is set to false if using
DISTANCE_FROM_WALL = 0 # m


#Use Threshold marker, ensure USE_THRESHOLD_MARKER is set to true if using
LATENCY = 81.5 #ms
THRESHOLD_ARR = [1, 1.5] # m
PREDICTIVE = True
THRESHOLD_MARKER_ID = 1 #Where in marker list, for AIM model, indexed at 0

FILEPATH_TO_STEPPATH = "C:/Users/Neurolab/Documents/Projects/Knight/SteppingStones/Stepping-Stone-Paths/Trial2"
FILEPATH_TO_OUTPUT_DATA = "C:/Users/Neurolab/Documents/Projects/Knight/SteppingStones/code/"

#####START OF CODE######

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
x = 1
y = 1
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
dfw = DISTANCE_FROM_WALL *331.3
threshold_arr = [x * 331.3 for x in THRESHOLD_ARR]
count = 0
latency_ms = LATENCY
latency_pix = LATENCY *0.3313

# Function to apply homography and coordinate transformation
def apply_homography_and_transformation(H, T, u, v):
    transformed_u, transformed_v = np.dot(T, np.array([u, v]))
    uv = np.array([transformed_u, transformed_v, 1])
    x, y, w = np.dot(H, uv)
    return x / w, y / w


def apply_inverse_homography(H_inv, x, y):
    xy = np.array([x, y, 1])
    u, v, w = np.dot(H_inv, xy)
    return -v / w, -u / w

# Sample pixel space points (u, v) and real space points (x, y)
pixel_points = [(679, 44), (776, 130), (773, 344), (963, 172), (1205, 70), (1127, 344) ]
real_world_points = [(979.2, 1068.4), (724.3, 777.7), (81.2, 788.3), (600.1, 215.5), (920.6, -521.2), (88.8, -281.2) ]

# Transform the pixel space points
T = np.array([[0, -1], [-1, 0]])
transformed_pixel_points = [(-v, -u) for (u, v) in pixel_points]

# Compute the homography matrix
real_world_points = np.float32(real_world_points)
transformed_pixel_points = np.float32(transformed_pixel_points)

H, _ = cv2.findHomography(transformed_pixel_points, real_world_points)
H_inv = np.linalg.inv(H)

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

def exit_handler():
    print("Exiting...")
    # your code here
    
atexit.register(exit_handler)

#Class for stepping stone
class Stone:
    def __init__(self, x: int, y: int, side: str, id: int, perturbed: int, threshold: float ) -> None:
        """
        Initializes a new stone object with the given x-coordinate, side, ID, and perturbed
        """
        self.x = x
        self.y = y
        self.side = side
        self.id=id
        self.perturbed = perturbed
        self.color = (252, 3, 148)
        self.threshold = threshold

    def draw(self, surface) -> None:
        """
        Draws the stone on the given surface
        """
        if self.side == "left":
            pygame.draw.rect(surface, self.color, (self.x,self.y, stone_width, stone_height))
        else:
            pygame.draw.rect(surface, self.color, (self.x,self.y, stone_width, stone_height))


def on_packet(packet):
    """
    Callback function that is called everytime a data packet arrives from QTM.
    This function updates QTM variables.
    """
    global markers, frame_number
    frame_number = packet.framenumber
    header, markers = packet.get_3d_markers_no_label()
        

async def draw_stones():
    """
    Function to draw the stepping stones on the screen and updates the display.
    This function runs as an asynchronous task.
    """
    global markers, frame_number
    # set the perturbed array
    try:
        with open(FILEPATH_TO_STEPPATH, "r") as file:
            content = file.read()
            stone_path_arr = [int(x) for x in content.split()]
    except FileNotFoundError:
        print("file not found")
    stone_counter = 0
    side = "right"
    stone_counter+=1
    init_stone = Stone(x, right_stone_y, side, stone_counter, stone_path_arr[stone_counter-1], random.choice(threshold_arr))
    stones.append(init_stone)
    prev_stone = stones[0]
    with open('data.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Frame Number", "Marker X", "Marker Y", "Stone Number", "Stone X", "Stone Y", "Pertrubed", "Threshold", "Side"])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            pygame.draw.circle(screen, (0, 0, 0), (1030 , 365), 3)  
            if keys[pygame.K_RETURN]:
                break
        while True:
            # process events that have occured
            pygame.event.pump()
            
            # Check if pygame screen has been exited
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    asyncio.get_event_loop().stop()
            
            # clear the screen
            screen.fill((255, 255, 255))
            
            # #add new stone if needed
            if side == "right" and prev_stone.x > step_length_left :
                if side == "left" : side = "right"
                else: side = "left"
                stone_counter+=1
                stones.append(Stone(1, left_stone_y, side, stone_counter, stone_path_arr[stone_counter-1], random.choice(threshold_arr)))
                prev_stone = stones[len(stones) - 1]
            elif side == "left" and prev_stone.x > step_length_right :
                if side == "left" : side = "right"
                else: side = "left"
                stone_counter+=1
                stones.append(Stone(1, right_stone_y, side, stone_counter, stone_path_arr[stone_counter-1], random.choice(threshold_arr)))
                prev_stone = stones[len(stones) - 1]
            
            time_since_last_frame = clock.tick() / 1000
            # calculate distance to move
            distance_to_move_right = vel_right * time_since_last_frame
            distance_to_move_left = vel_left * time_since_last_frame
            if USE_THRESHOLD_MARKER: threshold_marker_location = (1030 - (markers[THRESHOLD_MARKER_ID].y) *0.3313)
            else: threshold_marker_location = 0
            
            
            for stone in stones:
                if stone.x < screen_width and stone.x > 0:
                    if stone.side == "right":                       
                        stone.x = stone.x + distance_to_move_right
                        if (stone.perturbed and ((
                            (threshold_marker_location - (stone.x + stone_width)) <
                            (stone.threshold + latency_pix * TREADMILL_SPEED_RIGHT) and USE_THRESHOLD_MARKER) or (
                            not USE_THRESHOLD_MARKER and stone.x > dfw 
                            ))
                        ):
                            if stone.perturbed == 1:
                                stone.x = stone.x - rsbd
                            elif stone.perturbed == 2:
                                stone.x = stone.x + rsfd
                            elif stone.perturbed == 3:
                                stone.y = stone.y - rsrd
                            elif stone.perturbed == 4:
                                stone.y = stone.y + rsld
                            stone.perturbed = 0
                            stone.color = (252, 3, 3)
                        stone.draw(screen)
                        # csvwriter.writerow([frame_number, markers[THRESHOLD_MARKER_ID].x, markers[THRESHOLD_MARKER_ID].y, stone.id, stone.x, stone.y, stone.perturbed, stone.threshold, stone.side])
                        for marker in markers:   
                            if marker.x > -200 and marker.x < 1000  and marker.y> 116.8 and marker.y < 1400 and stone.id == 5:
                                s_x, s_y = apply_homography_and_transformation(H, T, stone.x - latency_pix * TREADMILL_SPEED_RIGHT, stone.y)
                                # csvwriter.writerow([frame_number, marker.x, marker.y, stone.id, s_x, s_y, stone.perturbed, stone.threshold, stone.side])
                                csvwriter.writerow([frame_number, marker.y, s_y])
                    else:
                        stone.x = stone.x + distance_to_move_left
                        if (stone.perturbed and ((
                            (threshold_marker_location - (stone.x + stone_width)) <
                            (stone.threshold + latency_pix * TREADMILL_SPEED_LEFT) and USE_THRESHOLD_MARKER) or (
                            not USE_THRESHOLD_MARKER and stone.x > dfw 
                            ))
                        ):
                            if stone.perturbed == 5:
                                stone.x = stone.x - lsbd
                            elif stone.perturbed == 6:
                                stone.x = stone.x + lsfd
                            elif stone.perturbed == 7:
                                stone.y = stone.y - lsrd
                            elif stone.perturbed == 8:
                                stone.y = stone.y + lsld
                            stone.perturbed = 0
                            stone.color = (252, 3, 3)
                        stone.draw(screen)
                        # csvwriter.writerow([frame_number, markers[THRESHOLD_MARKER_ID].x, markers[THRESHOLD_MARKER_ID].y, stone.id, stone.x, stone.y, stone.perturbed, stone.threshold, stone.side])
                        for marker in markers:
                            if marker.x > -200 and marker.x < 1000  and marker.y> 116.8 and marker.y < 1400 and stone.id == 5:
                                s_x, s_y = apply_homography_and_transformation(H, T, stone.x + latency_pix * TREADMILL_SPEED_RIGHT, stone.y)
                                csvwriter.writerow([frame_number, marker.x, marker.y, stone.id, s_x, s_y, stone.perturbed, stone.threshold, stone.side])
      
                else:
                    stones.pop(stones.index(stone))
            # for marker in markers:
            #     if marker.x > -200 and marker.x < 1000  and marker.y> 116.8 and marker.y < 1400: 
            #         cx, cy = apply_inverse_homography(H_inv, marker.x, marker.y) 
            #         print(str(cx) + ", " + str(cy))     
            #         pygame.draw.circle(screen, (255, 0, 0), (cx, cy), 5)
            # update the display
            pygame.display.update()
            await asyncio.sleep(0.001)
            
   

async def setup():
    """
    Main function that connects to QTM server and starts the draw_stones task
    """
    # connect to QTM server
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    # stream frame data and pass on_packet function as callback
    await connection.stream_frames(components=["3dnolabels", "3d"], on_packet=on_packet)
    asyncio.ensure_future(draw_stones())

if __name__ == "__main__":
    # start the setup function as a task
    asyncio.ensure_future(setup())
    # run event loop forever
    asyncio.get_event_loop().run_forever()

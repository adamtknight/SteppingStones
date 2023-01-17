import asyncio # library for asynchronous programming
import sys # library for system-specific parameters and functions
import qtm # library for connecting to the QTM server
import pygame # library for creating GUI elements
import os

# Initialize pygame library and center the screen
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "0,365"

# Set some initial variables
stone_counter = 0
screen_width = 1250
screen_height = 400

# Create the screen and set the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stepping Stones")

# Initialize object coordinates, dimensions, and velocity
x = 200
y = 200
stone_width = 100
stone_height = 60
left_stone_height = 50
right_stone_height = 150
vel = 1
step_length = 150
stones = []
TL_x, TL_y,TR_x, TR_y,BL_x, BL_y,BR_x, BR_y = 717,16,1140,384,717,382,1140,20
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

#Class for stepping stone
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

def on_packet(packet):
    """
    Callback function that is called everytime a data packet arrives from QTM.
    This function updates the position of the circle on the screen.
    """
    global circle_x, circle_y, frame_number
    frame_number = packet.framenumber
    header, markers = packet.get_3d_markers_no_label()
          
        

async def draw_stones():
    """
    Function to draw the stepping stones on the screen and updates the display.
    This function runs as an asynchronous task.
    """
    global circle_x, circle_y, frame_number
    side = "right"
    stones.append(Stone(1, side))  
    prev_stone = stones[0]      
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            break

    while True:
        pygame.event.pump()  # Process any events that have occurred
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # clear the screen
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
                stone.draw(screen)
            else:
                stones.pop(stones.index(stone))
        
        # display the frame number
        font = pygame.font.Font(None, 30)
        text = font.render("Frame number: {}".format(frame_number), True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # update the display
        pygame.display.flip()
        await asyncio.sleep(0.01)
   

async def setup():
    """
    Main function that connects to QTM server and starts the draw_stones task
    """
    # connect to QTM server
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    # stream frame data and pass on_packet function as callback
    await connection.stream_frames(components=["3dnolabels"], on_packet=on_packet)
    asyncio.ensure_future(draw_stones())

if __name__ == "__main__":
    # start the setup function as a task
    asyncio.ensure_future(setup())
    # run event loop forever
    asyncio.get_event_loop().run_forever()

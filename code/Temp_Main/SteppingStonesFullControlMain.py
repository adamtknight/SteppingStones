import asyncio
import csv # library for asynchronous programming
import sys # library for system-specific parameters and functions
import qtm # library for connecting to the QTM server
import pygame # library for creating GUI elements
import os
 
# Initialize pygame library and center the screen
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "0,365"

# Set some initial variables
screen_width = 1250
screen_height = 400

# Create the screen and set the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stepping Stones")

# Initialize object coordinates, dimensions, and velocity
x = 200
y = 200
step_width = 100
stone_width = 100
stone_height = 60
left_stone_height = 200 - stone_height/2 + step_width/2
right_stone_height = 200 - stone_height/2 - step_width/2
vel = 332.214 # move ___ pixels per second
step_length = 225
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

#Align the Screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        break

#Class for stepping stone
class Stone:
    def __init__(self, x: int, side: str, id: int) -> None:
        """
        Initializes a new stone object with the given x-coordinate, side and ID
        """
        self.x = x
        self.side = side
        self.id=stone_counter

    def draw(self, surface, color = (255,0,205)) -> None:
        """
        Draws the stone on the given surface
        """
        if self.side == "left":
            pygame.draw.rect(surface, color, (self.x,left_stone_height, stone_width, stone_height))
        else:
            pygame.draw.rect(surface, color, (self.x,right_stone_height, stone_width, stone_height))
async def package_receiver(queue):
    """ Asynchronous function that processes queue until None is posted in queue """
    
    global markers, frame_number
    while True:
        packet = await queue.get()
        if packet is None:
            break
        frame_number = packet.framenumber
        header, markers = packet.get_3d_markers_no_label()
   
          
async def draw_stones():
    """
    Function to draw the stepping stones on the screen and updates the display.
    This function runs as an asynchronous task.
    """

    global circle_x, circle_y, frame_number, stone_counter, color
    stone_counter = 0
    side = "right"
    stones.append(Stone(1, side, stone_counter))
    stone_counter+=1  
    prev_stone = stones[0]


    while True:
        pygame.event.pump()  # Process any events that have occurred
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # clear the screen
        screen.fill((255, 255, 255))
        color = (255, 0 ,205)
        #add new stones
        if(prev_stone.x > step_length):
            if side == "left" : side = "right"
            else: side = "left"
            stones.append(Stone(1, side, stone_counter))
            stone_counter+=1
            prev_stone = stones[len(stones) - 1]
            print(prev_stone.id)
        # get time since last frame in seconds
        time_since_last_frame = clock.tick() / 1000 
        # calculate distance to move
        distance_to_move = vel * time_since_last_frame 
        for marker in markers:
            if marker.y > 835:
                color=(255,0,0)
                break
        # update the position of stones
        for stone in stones:
            if stone.x < screen_width and stone.x > 0:
                stone.x = stone.x + distance_to_move
                stone.draw(screen, color)
                # Save the stone's pixel coordinates and the current frame number to a CSV file
                with open("stones.csv", "a", newline="") as f:
                    with open("stones.csv", "a", newline="") as f:
                        writer = csv.DictWriter(f, fieldnames=["Frame Number", "Stone ID", "X", "Y", "Side", "Marker Loc"])
                        height = right_stone_height if stone.side == "right" else left_stone_height
                        writer.writerow({"Frame Number": frame_number, "Stone ID": stone.id, "X": stone.x, "Y": height, "Side": stone.side, "Marker Loc": marker.y})
                
            else:
                del_stone = stones.pop(stones.index(stone))
                del del_stone
        for stone in stones:
            print(stone.id)   
        
        # display the frame number
        font = pygame.font.Font(None, 30)
        text = font.render("Frame number: {}".format(frame_number), True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # update the display
        pygame.display.flip()
        await asyncio.sleep(0.01)
   
async def shutdown(delay, connection, receiver_future, queue):

    # wait desired time before exiting
    await asyncio.sleep(delay)

    # make sure package_receiver task exits
    queue.put_nowait(None)
    await receiver_future

    # tell qtm to stop streaming
    await connection.stream_frames_stop()

    # stop the event loop, thus exiting the run_forever call
    loop.stop()

  

async def setup():
    """ main function """

    connection = await qtm.connect("127.0.0.1")

    if connection is None:
        return -1

    async with qtm.TakeControl(connection, "QTMpassword"):

        state = await connection.get_state()
        if state != qtm.QRTEvent.EventConnected:
            await connection.new()
            try:
                await connection.await_event(qtm.QRTEvent.EventConnected, timeout=10)
            except asyncio.TimeoutError:
                return -1

        queue = asyncio.Queue()

        receiver_future = asyncio.ensure_future(package_receiver(queue))

        await connection.stream_frames(components=["3dnolabels"], on_packet=queue.put_nowait)
        await connection.start()
        
        
        asyncio.ensure_future(draw_stones())
        asyncio.ensure_future(shutdown(120, connection, receiver_future, queue))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # start the setup function as a task
    asyncio.ensure_future(setup())
    # run event loop forever
    asyncio.get_event_loop().run_forever()

import asyncio # library for asynchronous programming
import sys # library for system-specific parameters and functions
import qtm # library for connecting to the QTM server
import pygame # library for creating GUI elements

# initialize pygame library
pygame.init()

# set up the screen with a size of 800x600
screen = pygame.display.set_mode((800, 600))

# set the caption/title of the screen to "Moving Circle"
pygame.display.set_caption("Moving Circle")

# initialize variables to store circle position and frame number
circle_x, circle_y = 0, 0
frame_number = 0

def on_packet(packet):
    """
    Callback function that is called everytime a data packet arrives from QTM.
    This function updates the position of the circle on the screen.
    """
    global circle_x, circle_y, frame_number
    frame_number = packet.framenumber
    header, markers = packet.get_3d_markers_no_label()
    for marker in markers:
        if marker.x > 0 and marker.x < 800  and marker.y>0 and marker.y <600:
            circle_x, circle_y = 800 - marker.y ,  600 - marker.x
        

async def draw_circle():
    """
    Function to draw the circle on the screen and updates the display.
    This function runs as an asynchronous task.
    """
    global circle_x, circle_y, frame_number
    while True:
        pygame.event.pump()  # Process any events that have occurred
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # clear the screen
        screen.fill((0, 0, 0))
        
        # draw the circle
        pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), 25)
        
        # display the frame number
        font = pygame.font.Font(None, 30)
        text = font.render("Frame number: {}".format(frame_number), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        # update the display
        pygame.display.flip()
        await asyncio.sleep(0.01)

async def setup():
    """
    Main function that connects to QTM server and starts the draw_circle task
    """
    # connect to QTM server
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    # stream frame data and pass on_packet function as callback
    await connection.stream_frames(components=["3dnolabels"], on_packet=on_packet)
    asyncio.ensure_future(draw_circle())

if __name__ == "__main__":
    # start the setup function as a task
    asyncio.ensure_future(setup())
    # run event loop forever
    asyncio.get_event_loop().run_forever()

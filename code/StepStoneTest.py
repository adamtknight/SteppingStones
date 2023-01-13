import asyncio
import sys
import qtm
import pygame

# initialize pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Circle")

# initialize variables to store circle position and frame number
circle_x, circle_y = 0, 0
frame_number = 0

def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    global circle_x, circle_y, frame_number
    frame_number = packet.framenumber
    header, markers = packet.get_3d_markers_no_label()
    for marker in markers:
        if marker.x > 0 and marker.x < 800  and marker.y>0 and marker.y <600:
            circle_x, circle_y = marker.x, marker.y
        

async def draw_circle():
    """ Function to draw the circle on the screen """
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
    """ Main function """
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    await connection.stream_frames(components=["3dnolabels"], on_packet=on_packet)
    asyncio.ensure_future(draw_circle())

if __name__ == "__main__":
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()

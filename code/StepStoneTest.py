import asyncio # library for asynchronous programming
import sys # library for system-specific parameters and functions
import qtm # library for connecting to the QTM server
import pygame # library for creating GUI elements
import logging
# initialize pygame library
pygame.init()

# set up the screen with a size of 800x600
screen = pygame.display.set_mode((200, 200))

# set the caption/title of the screen to "Moving Circle"
pygame.display.set_caption("Moving Circle")

# initialize variables to store circle position and frame number
circle_x, circle_y = 0, 0
frame_number = 0
LOG = logging.getLogger("example")

          
async def package_receiver(queue):
    """ Asynchronous function that processes queue until None is posted in queue """
    LOG.info("Entering package_receiver")
    global circle_x, circle_y, frame_number
    while True:
        packet = await queue.get()
        if packet is None:
            break
        header, markers = packet.get_3d_markers_no_label()
        LOG.info("Component info: %s", header)
        frame_number = packet.framenumber
        for marker in markers:
            if marker.x > 0 and marker.x < 200 * 3  and marker.y> 0 and marker.y < 200 *3:
                circle_x, circle_y = (200 - marker.y/3) , (200 - marker.x/3)

    LOG.info("Exiting package_receiver")   

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
        screen.fill((0, 255, 0))
        
        # draw the circle
        pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), 5)
        
        # display the frame number
        font = pygame.font.Font(None, 30)
        text = font.render("Frame number: {}".format(frame_number), True, (255, 255, 255))
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
                LOG.error("Failed to start new measurement")
                return -1

        queue = asyncio.Queue()

        receiver_future = asyncio.ensure_future(package_receiver(queue))

        await connection.stream_frames(components=["3dnolabels"], on_packet=queue.put_nowait)
        await connection.start()
        asyncio.ensure_future(shutdown(30, connection, receiver_future, queue))
        asyncio.ensure_future(draw_circle())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # start the setup function as a task
    asyncio.ensure_future(setup())
    # run event loop forever
    asyncio.get_event_loop().run_forever()

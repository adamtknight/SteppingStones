

import SteppingStonesDisplay
import math
import sys
import asyncio
import qtm
import pygame
import testdisplay
from queue import Queue

FrameNumber = 0
frame_queue = Queue()

def on_packet(packet):
    global FrameNumber
    FrameNumber = packet.framenumber
    frame_queue.put(FrameNumber)
    """ Callback function that is called everytime a data packet arrives from QTM """
    print("Framenumber: {}".format(packet.framenumber))
    header, markers = packet.get_3d_markers()
    print("Component info: {}".format(header))
    for marker in markers:
        print("\t", marker)

async def handle_data():
    """ Function for handling data packets """
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return
    await connection.stream_frames(components=["3d"], on_packet=on_packet)

async def main():
    """ Main function """
     # create task to run the data handling function
    data_task = asyncio.create_task(handle_data())
    # create task to run the Pygame function
    pygame_task = asyncio.create_task(SteppingStonesDisplay.start_program())
    #pygame_task = asyncio.create_task(testdisplay.TestDisplay())

    await asyncio.gather(pygame_task, data_task)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()



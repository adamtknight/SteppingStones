import asyncio
import qtm
import pyglet

# initialize window
window = pyglet.window.Window(width=800, height=600)

# initialize variable to store frame number
frame_number = 0

def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    global frame_number
    frame_number = packet.framenumber

@window.event
def on_draw():
    """ Function to draw the frame number on the screen """
    global frame_number
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    label = pyglet.text.Label(f"Frame number: {frame_number}",
                              font_name='Arial',
                              font_size=12,
                              x=10, y=10,
                              anchor_x='left', anchor_y='bottom')
    label.draw()

async def setup():
    """ Main function """
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    await connection.stream_frames(components=["3d"], on_packet=on_packet)

if __name__ == "__main__":
    asyncio.ensure_future(setup())
    pyglet.app.run()

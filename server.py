import cv2
import asyncio
import websockets
import base64
import imutils
from picamera2 import Picamera2
import numpy as np

async def handle_connection(websocket, path):
    for frame in get_frames():
        await websocket.send(frame)


def get_frames():
    global camera

    while True:
        image = camera.capture_array("lores")
        rgb = cv2.cvtColor(image, cv2.COLOR_YUV420p2RGB)
        frame = imutils.resize(rgb, width=100)
        _, buffer = cv2.imencode('.png', frame)
        frame = base64.b64encode(buffer)
        yield b'data:image/png;base64,' + frame

# Start video capture
camera = Picamera2()
config = camera.create_preview_configuration(
    lores={ "size": (320, 240) },
)
camera.configure(config)
camera.start()

# Start the server
start_server = websockets.serve(handle_connection, "0.0.0.0", 8000)

# Do async stuff
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

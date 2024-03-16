import time
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

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame_count = 0
    last_fps = 0
    last_time = time.time()

    while True:
        image = camera.capture_array()
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(rgb, width=100)
        frame_count += 1

        cv2.putText(frame, f'FPS: {last_fps}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        _, buffer = cv2.imencode('.png', frame)
        frame = base64.b64encode(buffer)
        yield b'data:image/png;base64,' + frame

        if time.time() - last_time >= 1:
            last_fps = frame_count
            frame_count = 0
            last_time = time.time()

# Start video capture
camera = Picamera2()
config = camera.create_preview_configuration(
    main={ "size": (int(3280/4), int(2464/4)) },
)
camera.configure(config)
camera.set_controls({ "ExposureTime": 8000 })
camera.start()

# Start the server
start_server = websockets.serve(handle_connection, "0.0.0.0", 8000)

# Do async stuff
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

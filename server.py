import time
import cv2
import asyncio
import websockets
import base64
import imutils

async def handle_connection(websocket, path):
    """
    Websocket connection handler
    :param websocket: Conected websocket
    :param path: Path of connected websocket
    :return: None
    """
    for frame in get_frames():
        await websocket.send(frame)


def get_frames():
    """
    Generator function that uses cv2 to stream frames to a websocket,
    yielding byte-encoded frames.
    :return: None
    """
    last_saved_at = time.time()
    count = 0

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.png', frame)
            frame = imutils.resize(frame, width=100)

            if time.time() - last_saved_at > 1:
                last_saved_at = time.time()
                filename = f'frame_{count}.png'
                cv2.imwrite(filename, frame)

            frame = base64.b64encode(buffer)
            yield b'data:image/png;base64,' + frame


# Start video capture
camera = cv2.VideoCapture(0, apiPreference=cv2.CAP_V4L2)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
camera.set(cv2.CAP_PROP_FPS, 30)
# Start the server
start_server = websockets.serve(handle_connection, "0.0.0.0", 8000)

# Do async stuff
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

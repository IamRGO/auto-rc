print("loading libraries...")
import time
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import serial

import tensorflow as tf
import model as m
import data
from picamera2 import Picamera2
import imutils

DESIRED_DELAY = 0.185

print("Staring camera...")

camera = Picamera2()
config = camera.create_preview_configuration(
    main={ "size": (int(3280/4), int(2464/4)) },
)
camera.configure(config)
camera.set_controls({ "ExposureTime": 8000 })
camera.start()

print("loading model...")
model = m.create_model()
model.load_weights("brain")

# connects to arduino
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=2400, timeout=1)

input("press enter to begin driving...")
last_fps = 0
last_fps_time = time.time()
last_capture_time = time.time()
fps = 0

while True:
  start_time = time.time()
  image = camera.capture_array()

  input_list = [
    data.parse_image(image)
  ]

  result = model(
    np.array(input_list, dtype=np.float32),
  )

  duration_ms = int((time.time() - last_capture_time) * 1000)
  last_capture_time = time.time()
  print("Processed...", last_fps, "fps", duration_ms, "ms")
  result = result.numpy()[0]
  print(result)

  throttle_val = 114

  if int(result[0] * 100) in range(25, 35):
    print("SLOW DOWN!!!")
    throttle_val = 81

  steering_val = np.interp(result[0], [0, 1.0], [40, 130])

  message = "D" + str(steering_val) + " " + str(throttle_val)
  arduino.write(message.encode("UTF-8"))
  fps += 1

  time_to_sleep = DESIRED_DELAY - (time.time() - start_time)
  time_to_sleep = 0.0

  if time_to_sleep > 0:
    print("Sleep!", time_to_sleep)
    time.sleep(time_to_sleep)

  if time.time() - last_fps_time > 1:
    last_fps = fps
    last_fps_time = time.time()
    fps = 0

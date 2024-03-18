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


print("Staring camera...")

# camera = cv2.VideoCapture(-1)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# camera.set(cv2.CAP_PROP_FPS, 30)
# camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

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
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=5)

input("press enter to begin driving...")
while True:
  print("taking a picture...")
  # _, frame = camera.grab()  # read the camera frame
  image = camera.capture_array()
  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  frame = imutils.resize(rgb, width=320)
  image = cv2.resize(frame, (320, 240))

  input_list = [
    data.parse_image(image)
  ]

  print("running a prediction...")
  result = model.predict(
    np.array(input_list, dtype=np.float32),
    verbose=0,
  )

  result = result[0]

  print(result)

  steering_val = np.interp(result[0], [0, 1.0], [40, 130])
  # throttle_val = np.interp(result[1], [0.0, 1.0], [90, 150])

  # if result[1] == 0:
  #     throttle_val = 0

  throttle_val = 150

  message = "D" + str(steering_val) + " " + str(throttle_val)
  arduino.write(message.encode("UTF-8"))
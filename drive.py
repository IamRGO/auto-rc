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
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=2400, timeout=5)

input("press enter to begin driving...")
while True:
  print("taking a picture...")
  image = camera.capture_array()

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
  throttle_val = 130

  message = "D" + str(steering_val) + " " + str(throttle_val)
  arduino.write(message.encode("UTF-8"))
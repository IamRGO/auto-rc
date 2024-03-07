print("loading libraries...")
import time
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import serial

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

import data

print("Staring camera...")

camera = cv2.VideoCapture(-1)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 96)
camera.set(cv2.CAP_PROP_FPS, 30)


print("loading model...")
model = Sequential([
  Dense(494, activation='relu', input_dim=128 * 96),
  Dense(128, activation='relu'),
  Dense(64, activation='relu'),
  Dense(32, activation='relu'),
  Dense(16, activation='relu'),
  Dense(2, activation='sigmoid')
])

model.load_weights("brain")

# connects to arduino
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=5)

input("press enter to begin driving...")
while True:
  print("taking a picture...")
  _, frame = camera.read()  # read the camera frame
  image = cv2.resize(frame, (128, 96))
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

  light_yellow = np.array([20, 35, 100])
  dark_yellow = np.array([100, 200, 177])

  mask = cv2.inRange(hsv, light_yellow, dark_yellow)

  result = cv2.bitwise_and(image, image, mask = mask)

  input_list = [
    data.parse_image(result)
  ]

  print("running a prediction...")
  result = model.predict(
    np.array(input_list, dtype=np.float32),
    verbose=0,
  )

  result = result[0]

  print(result)

  steering_val = np.interp(result[0], [0.0, 1.0], [40, 130])
  throttle_val = np.interp(result[1], [0.0, 1.0], [90, 250])

  if result[1] == 0:
      throttle_val = 0

  message = "D" + str(steering_val) + " " + str(throttle_val)
  arduino.write(message.encode("UTF-8"))
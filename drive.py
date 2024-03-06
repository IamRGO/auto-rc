import time
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

import data

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)

model = Sequential([
  Dense(494, activation='relu', input_dim=128 * 96),
  Dense(128, activation='relu'),
  Dense(64, activation='relu'),
  Dense(32, activation='relu'),
  Dense(16, activation='relu'),
  Dense(2, activation='sigmoid')
])

model.load_weights("brain")

while True:
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

  result = model.predict(np.array(input_list, dtype=np.float32))

  print(result)
  steering = int(result[0][0] * 100)

  if steering in range(45, 55):
    print("Turn STRAIGHT")
  elif steering in range(0, 45):
    print("Turn LEFT")
  else:
    print("Turn RIGHT")

  time.sleep(1)




print("loading libraries...")
import cv2
import numpy as np

import tensorflow as tf
import model as m
import data

print("loading model...")
model = m.create_model()
model.load_weights("brain")

while True:
  print("taking a picture...")
  frame_index = input("Enter frame index: ")

  frame = cv2.imread("debug/frame_" + frame_index + ".png")

  input_list = [
    data.parse_image(result)
  ]

  print("running a prediction...")
  result = model.predict(
    np.array(input_list, dtype=np.float32),
    verbose=0,
  )

  result = result[0]
  steering_val = np.interp(result[0], [0.0, 1.0], [40, 130])

  print(result[0], "->", steering_val)

# 18 -> 0.56
# 22 -> 0.50
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

import data

input_list = []
output_list = []

print("Loading images...")

for i in range(522):
  i = str(i)

  print("loading...", i)

  output_data = data.read_output("processed_temp/data_" + i + ".txt")

  if output_data == None:
    continue
  elif output_data[1] < 0:
    continue

  output_list.append(output_data)

  input_list.append(
    data.read_input('processed_temp/frame_' + i + '.png')
  )

input_list = np.array(input_list[20:], dtype=np.float32)
output_list = np.array(output_list[20:], dtype=np.float32)
validation_input_list = np.array(input_list[:20], dtype=np.float32)
validation_output_list = np.array(output_list[:20], dtype=np.float32)

model = Sequential([
  Dense(128, activation='relu', input_dim=len(input_list[0])),
  Dense(64, activation='relu'),
  Dense(32, activation='relu'),
  Dense(2, activation='sigmoid')
])

model.compile(
  optimizer=tf.keras.optimizers.legacy.RMSprop(learning_rate=0.01),
  loss = 'mean_absolute_error',
)

print("training...")
train_history = model.fit(
  input_list,
  output_list,
  epochs=100,
  verbose=1,
  validation_data=(
    validation_input_list,
    validation_output_list
  )
)

model.save_weights("brain")
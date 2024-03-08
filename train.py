import cv2
import numpy as np
import os
import glob

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

import data

gpus = tf.config.list_physical_devices('GPU')

if gpus:
  try:
    tf.config.set_visible_devices(gpus[0], 'GPU')
  except RuntimeError as e:
    print(e)

input_list = []
output_list = []

print("Loading images...")

file_list = glob.glob("processed_temp/*png")
file_index = 0
for image_path in file_list:
  i = image_path[len("processed_temp/frame_"):-4]
  file_index += 1

  print("loading...", i, "(", file_index, "/", len(file_list), ")")

  data_path = "processed_temp/data_" + i + ".txt"

  if os.path.isfile(data_path) == False:
    continue

  output_data = data.read_output(data_path)

  if output_data == None:
    continue
  elif output_data[1] < 0:
    continue

  output_list.append(output_data)

  input_list.append(
    data.read_input(image_path)
  )

input_list = np.array(input_list, dtype=np.float32)
output_list = np.array(output_list, dtype=np.float32)

model = Sequential([
  Conv2D(16, 3, padding='same', activation='relu', input_shape=(320, 240, 1)),
  MaxPooling2D(),
  Conv2D(32, 3, padding='same', activation='relu'),
  MaxPooling2D(),
  Conv2D(64, 3, padding='same', activation='relu'),
  MaxPooling2D(),
  Flatten(),
  Dense(128, activation='relu'),
  Dropout(0.2),
  Dense(64, activation='relu'),
  Dropout(0.2),
  Dense(32, activation='relu'),
  Dropout(0.2),
  Dense(16, activation='relu'),
  Dropout(0.2),
  Dense(2, activation='sigmoid')
])

model.compile(
  optimizer=tf.keras.optimizers.legacy.Adadelta(learning_rate=0.01),
  loss = 'mean_squared_error',
)

print("training...")
train_history = model.fit(
  input_list,
  output_list,
  epochs=300,
  verbose=1,
  # validation_split=0.1,
)

model.save_weights("brain")
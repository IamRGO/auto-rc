import cv2
import numpy as np
import os
import glob

import tensorflow as tf
import model as m
import data

gpus = tf.config.list_physical_devices('GPU')

if gpus:
  try:
    tf.config.set_visible_devices(gpus[0], 'GPU')
  except RuntimeError as e:
    print(e)

input_list = []
output_list = []

bucket_list = []

for i in range (0, 105, 5):
  r = range(i, i + 4)
  bucket_list.append(
    [r, 0]
  )

print("Loading images...")

file_list = glob.glob("processed_temp/*png")
file_index = 0
for image_path in file_list:
  i = image_path[len("processed_temp/frame_"):-4]
  file_index += 1

  if file_index % 100 == 0:
    print("loading...", i, "(", file_index, "/", len(file_list), ")")

  data_path = "processed_temp/data_" + i + ".txt"

  if os.path.isfile(data_path) == False:
    continue

  output_data = data.read_output(data_path)

  if output_data == None:
    continue

  steering = output_data[0] * 100
  bucket_index = int(steering / 5)

  if bucket_list[bucket_index][1] > 305:
    continue

  bucket_list[bucket_index][1] += 1

  output_list.append(output_data)

  input_list.append(
    data.read_input(image_path)
  )

input_list = np.array(input_list, dtype=np.float32)
output_list = np.array(output_list, dtype=np.float32)

model = m.create_model()

model.compile(
  optimizer=tf.keras.optimizers.legacy.Adadelta(learning_rate=0.01, decay=0.001),
  loss = 'mean_squared_error',
)

print("training...")
train_history = model.fit(
  input_list,
  output_list,
  epochs=50,
  verbose=1,
  validation_split=0.2,
)

model.save_weights("brain")

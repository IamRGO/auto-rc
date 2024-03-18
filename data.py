import tensorflow as tf
import cv2
import numpy as np

def read_output(file_path):
  file = open(file_path, 'r')
  data = file.read()
  file.close()

  steering, throttle = data.split(":")
  steering = int(steering) # range 40, 131
  steering = np.interp(steering, [40, 130], [0.0, 1.0])

  # throttle = int(throttle)
  # throttle = np.interp(throttle, [90, 130], [0.0, 1.0])

  return [steering]

def read_input(file_path):
  image = cv2.imread(file_path)
  img_tensor = tf.convert_to_tensor(image, dtype=tf.float32)
  img_resized = tf.image.resize_with_pad(img_tensor, 120, 160)
  img_gray = tf.image.rgb_to_grayscale(img_resized)
  return img_gray

def parse_image(image):
  rgb_image = mask_image(image)
  img_tensor = tf.convert_to_tensor(rgb_image, dtype=tf.float32)
  img_resized = tf.image.resize_with_pad(img_tensor, 120, 160)
  img_gray = tf.image.rgb_to_grayscale(img_resized)
  return img_gray

def mask_image(image):
  image = cv2.resize(image, (160, 120))

  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  light_ya = np.array([17, 100, 44])
  dark_ya = np.array([35, 310, 150])

  mask = cv2.inRange(hsv, light_ya, dark_ya)
  result = cv2.bitwise_or(image, image, mask = mask)
  result[mask == 255] = [255, 255, 255]

  rgb_image = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)

  return rgb_image
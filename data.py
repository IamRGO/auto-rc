import tensorflow as tf
import cv2
import numpy as np

IMAGE_WIDTH = 160
IMAGE_HEIGHT = 120

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
  img_resized = tf.image.resize_with_pad(img_tensor, IMAGE_HEIGHT, IMAGE_WIDTH)
  img_gray = tf.image.rgb_to_grayscale(img_resized)
  return img_gray

def parse_image(image):
  rgb_image = mask_image(image, "RGB")
  img_tensor = tf.convert_to_tensor(rgb_image, dtype=tf.float32)
  img_resized = tf.image.resize_with_pad(img_tensor, IMAGE_HEIGHT, IMAGE_WIDTH)
  img_gray = tf.image.rgb_to_grayscale(img_resized)
  return img_gray

def mask_image(image, image_format="BGR"):
  image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))

  if image_format == "BGR":
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  else:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

  light_ya = np.array([17, 100, 44])
  dark_ya = np.array([35, 310, 150])

  mask = cv2.inRange(hsv, light_ya, dark_ya)
  result = cv2.bitwise_or(hsv, hsv, mask = mask)
  result[mask == 255] = [255, 255, 255]

  rgb_image = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
  # cv2.imwrite("debug.png", rgb_image)

  return rgb_image
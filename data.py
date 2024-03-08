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

  throttle = int(throttle) # range 90, 180
  throttle = np.interp(throttle, [90, 180], [0.0, 1.0])

  return [steering, throttle]

def read_input(file_path):
  image = cv2.imread(file_path)
  small_image = cv2.resize(image, (320, 240))
  return parse_image(small_image)

def parse_image(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  img_tensor = tf.convert_to_tensor(hsv, dtype=tf.float32)
  img_gray = tf.image.rgb_to_grayscale(img_tensor)
  img_resized = tf.image.resize_with_pad(img_gray, 320, 240)
  return img_resized


import cv2
import numpy as np
import pdb

image = cv2.imread('rope_sample__.png')

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# remove [0, 0, 255]

min_h, min_s, min_v = np.min(hsv, axis=(0, 1))
max_h, max_s, max_v = np.max(hsv, axis=(0, 1))
print(str(min_h) + ",", str(min_s) + ",", min_v)
print(str(max_h) + ",", str(max_s) + ",", max_v)
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

# image = cv2.imread('saves/frame_0.png')
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# lower_white = np.array([30, 30, 135])
# upper_white = np.array([36, 137, 170])
# mask = cv2.inRange(hsv, lower_white, upper_white)
# result = cv2.bitwise_and(image, image, mask = mask)

# large = cv2.resize(result, (0,0), fx=5, fy=5)

# cv2.imwrite('result.png', large)

# open saves/frame_#{i}.png
list_of_files = [f for f in listdir('saves') if isfile(join('saves', f))]
for file in list_of_files:
  image = cv2.imread('saves/' + file)
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

  lower_white = np.array([30, 35, 135])
  upper_white = np.array([36, 137, 170])
  mask = cv2.inRange(hsv, lower_white, upper_white)
  result = cv2.bitwise_and(image, image, mask = mask)

  large = cv2.resize(result, (0,0), fx=5, fy=5)

  cv2.imwrite('processed/result_' + file, large)
  print('saves/result_' + file)
  print('---')

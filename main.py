import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import shutil

list_of_files = [f for f in listdir('temp') if isfile(join('temp', f))]

for file in list_of_files:
  if "png" in file:
    image = cv2.imread('temp/' + file)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # light_yellow = np.array([30, 3, 150])
    # dark_yellow = np.array([72, 109, 167])
    light_yellow = np.array([20, 35, 100])
    dark_yellow = np.array([100, 200, 177])

    mask = cv2.inRange(hsv, light_yellow, dark_yellow)
    result = cv2.bitwise_and(image, image, mask = mask)

    large = cv2.resize(result, (0,0), fx=5, fy=5)

    # cv2.imwrite('processed/result_' + file, large)

    cv2.imwrite('processed_temp/' + file, result)

    print('temp/result_' + file)
    print('---')

  else:
    shutil.move('temp/' + file, 'processed_temp/' + file)
    print("data moved")
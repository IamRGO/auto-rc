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

    light_yellow = np.array([20, 50, 140])
    dark_yellow = np.array([100, 200, 250])

    mask = cv2.inRange(hsv, light_yellow, dark_yellow)
    result = cv2.bitwise_and(image, image, mask = mask)

    cv2.imwrite('processed_temp/' + file, result)

    print('temp/result_' + file)
    print('---')

  else:
    shutil.move('temp/' + file, 'processed_temp/' + file)
    print("data moved")
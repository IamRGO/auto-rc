import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import shutil
import data

list_of_files = [f for f in listdir('temp') if isfile(join('temp', f))]

for file in list_of_files:
  if "png" in file:
    image = cv2.imread('temp/' + file)
    result = data.mask_image(image)
    cv2.imwrite('processed_temp/' + file, result)

    print('temp/result_' + file)
    print('---')

  else:
    shutil.move('temp/' + file, 'processed_temp/' + file)
    print("data moved")
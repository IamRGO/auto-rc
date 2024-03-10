import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import shutil
import data

list_of_files = [f for f in listdir('temp') if isfile(join('temp', f))]

count = 0
total = len(list_of_files)

for file in list_of_files:
  count += 1

  if count % 100 == 0:
    print("Processing", file, "(", count, "/", total, ")")

  if "png" in file:
    image = cv2.imread('temp/' + file)
    result = data.mask_image(image)
    cv2.imwrite('processed_temp/' + file, result)
  else:
    shutil.move('temp/' + file, 'processed_temp/' + file)
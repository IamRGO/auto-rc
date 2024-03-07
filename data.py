import cv2

def read_output(file_path):
  file = open(file_path, 'r')
  data = file.read()
  file.close()

  steering, throttle = data.split(":")
  steering = int(steering) # range 40, 131
  steering = (steering - 40) / (131 - 40)

  throttle = int(throttle) # range 87, 250
  throttle = (throttle - 87) / (180 - 87)

  return [steering, throttle]

def read_input(file_path):
  image = cv2.imread(file_path)
  small_image = cv2.resize(image, (320, 240))
  return parse_image(small_image)

def parse_image(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  input_data = []

  for row in hsv:
    for pixel in row:
      if pixel.tolist() == [0, 0, 0]:
        input_data.append(0)
      else:
        input_data.append(1)

  return input_data

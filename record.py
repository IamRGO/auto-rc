import cv2
import serial
import time

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=5)
time.sleep(2)
print("Sending data...")

count = int(input("where do you want to start?"))

while True:
    _, frame = camera.read()  # read the camera frame
    filename = f'temp/frame_{count}.png'
    cv2.imwrite(filename, frame)

    arduino.write(b"stats")
    steering = str(arduino.readline().decode("UTF-8").strip())
    throttle = str(arduino.readline().decode("UTF-8").strip())

    filename = f'temp/data_{count}.txt'
    file = open(filename, "w")
    file.write(steering + ":" + throttle)
    file.close()

    print("data collected", count)
    count += 1

    # time.sleep(0.3334)
import cv2
import serial
import time
import imutils
from picamera2 import Picamera2

camera = Picamera2()
config = camera.create_preview_configuration(
    main={ "size": (int(3280/4), int(2464/4)) },
)
camera.configure(config)
camera.set_controls({ "ExposureTime": 10000 })
camera.start()

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.3)

time.sleep(2)
print("Sending data...")

count = int(input("where do you want to start?"))

while True:
    image = camera.capture_array()
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(rgb, width=320)

    image_filename = f'/home/pi/usb/temp/frame_{count}.png'

    try:
        arduino.write(b"stats")
        steering, throttle = list(str(arduino.readline().decode("UTF-8").strip()).split(":"))
    except UnicodeDecodeError:
        print("Invalid data from arduino...")
        arduino.flush()
        continue

    if steering == "" or throttle == "":
        continue

    data_filename = f'/home/pi/usb/temp/data_{count}.txt'
    file = open(data_filename, "w")
    file.write(steering + ":" + throttle)
    file.close()
    cv2.imwrite(image_filename, frame)
    print("saved data...")

    print("data collected", count, "steering", steering, "throttle", throttle)
    count += 1

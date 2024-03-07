import time
import numpy as np
import serial

arduino = serial.Serial(port='/dev/cu.usbserial-1410', baudrate=9600, timeout=5)
time.sleep(2)
command_list = [
    [0.0, 0.0],
    [1.0, 0.0],
    [0.5, 0.5],
    [0.5, 0.0],
]

for steering, throttle in command_list:
    print(steering, throttle)
    steering_val = np.interp(steering, [0.0, 1.0], [40, 130])
    throttle_val = np.interp(throttle, [0.0, 1.0], [90, 250])

    if throttle == 0:
        throttle_val = 0

    message = "D" + str(steering_val) + " " + str(throttle_val)
    print(message)
    arduino.write(message.encode("UTF-8"))
    input()


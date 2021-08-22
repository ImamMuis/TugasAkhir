import time, RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2750)
kit.servo[1].set_pulse_width_range(500, 2750)

def servoMove(channel = 0, start = 10, stop = 170, speed = 1):
    print("Speed: ", speed)
    print("Servo Channel: ", channel)
    print("Move from", start, "to", stop)
    print("")
    speed = float(0.02 / speed)
    for x in range(90, stop):
        kit.servo[channel].angle = x
        time.sleep(speed)
    for x in range(stop, start, -1):
        kit.servo[channel].angle = x
        time.sleep(speed)
    for x in range(start, 90):
        kit.servo[channel].angle = x
        time.sleep(speed)
    time.sleep(0.5)

try: 
    while True:
        servoMove(0, 20, 160, 1)
        time.sleep(2)
        servoMove(1, 20, 160, 1)
        time.sleep(2)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    GPIO.cleanup()
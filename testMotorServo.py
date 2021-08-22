import time, RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2750)
kit.servo[1].set_pulse_width_range(500, 2750)

    
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

import time
import motorLib
import RPi.GPIO as GPIO

try:
    while True:
        motorLib.motorStart("FORWARD")
        motorLib.motorStop()
        time.sleep(1)
        
        motorLib.motorStart("REVERSE")
        motorLib.motorStop()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    motorLib.motorStop()
    GPIO.cleanup()
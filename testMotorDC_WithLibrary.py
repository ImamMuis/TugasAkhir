import time
import RPi.GPIO as GPIO
import MotorDC_Library as mLib

try:
    while True:
        mLib.motorStart("FORWARD")
        mLib.motorStop()
        time.sleep(1)
        
        mLib.motorStart("REVERSE")
        mLib.motorStop()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    mLib.motorStop()
    GPIO.cleanup()
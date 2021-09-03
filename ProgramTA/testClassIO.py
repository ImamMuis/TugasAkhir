import InputOutput as IO
import RPi.GPIO as GPIO
import time

Selenoid = IO.Output(11)

try:
    while True:
        Selenoid.buka()
        time.sleep(1)
        Selenoid.kunci()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    GPIO.cleanup()
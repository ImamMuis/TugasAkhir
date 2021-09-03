import time
import RPi.GPIO as GPIO

Solenoid = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(Solenoid, GPIO.OUT)

try: 
    while True:
        GPIO.output(Solenoid, 1)
        print("Buka")
        time.sleep(1)
        
        GPIO.output(Solenoid, 0)
        print("Kunci")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Program Error!")

finally:
    GPIO.cleanup()

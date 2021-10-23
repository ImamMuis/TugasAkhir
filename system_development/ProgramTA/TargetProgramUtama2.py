import time
import RPi.GPIO as GPIO
import sistemPintu2 as sp

GPIO.setmode(GPIO.BCM)

sp.Solenoid(14)
sp.Solenoid.output()

try:
    while True:
        sp.Solenoid.off()
        time.sleep(1)
        sp.Solenoid.on()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    GPIO.cleanup()
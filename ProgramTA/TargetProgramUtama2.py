import time
import RPi.GPIO as GPIO
import sistemPintu2 as sp

GPIO.setmode(GPIO.BCM)

sp.PIR(17)
sp.Solenoid(14)
# sp.L_Switch(22, 27)
# sp.driverMotor(15, 18)
# sp.LED_Indicator(9, 10, 11)

try:  
    # sp.PIR.setup()
    
    while True:       
        sp.PIR.userMasuk()
        time.sleep(1) 
        sp.PIR.userMasuk()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    GPIO.cleanup()
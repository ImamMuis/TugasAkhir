import RPi.GPIO as GPIO
import sistemPintu2 as sp

sp.PIR(17)
sp.Solenoid(14)
sp.L_Switch(22, 27)
sp.driverMotor(15, 18)
sp.LED_Indicator(9, 10, 11)

try:  
    sp.PIR.setup()
    sp.Solenoid.kunci()
    
    while True:       
        user = input("Wajah dikenali? y/n: ")

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    GPIO.cleanup()
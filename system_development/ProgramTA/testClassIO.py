import time
import sistemPintu2 as sp
# import sistemKamera as sk
import RPi.GPIO as GPIO

SensorPIR = sp.PIR(17)
L_Switch = sp.L_Switch(22, 27)

Solenoid = sp.Solenoid(14)
Motor = sp.driverMotor(15, 18)

try:
    while True:
        # Solenoid.buka()
        # time.sleep(1)
        # Solenoid.kunci()
        # time.sleep(1)
        L_Switch.Buka()
        L_Switch.Tutup()
        time.sleep(0.02)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    GPIO.cleanup()
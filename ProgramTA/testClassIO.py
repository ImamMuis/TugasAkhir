import sistemPintu2 as sp
# import sistemKamera as sk
import RPi.GPIO as GPIO

SensorPIR = sp.PIR(17)
LSBuka, LSTutup = sp.L_Switch(22, 27)

Motor1 = sp.PIN.Output(15)
Motor2 = sp.PIN.Output(18)
Solenoid = sp.PIN.Output(14)

try:
    while True:
        pass

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    GPIO.cleanup()
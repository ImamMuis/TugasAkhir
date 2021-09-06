import InputOutput as IO
import RPi.GPIO as GPIO
import time

Selenoid = IO.Output(14)
SensorPIR = sp.PIN.Input(17)
LS_Buka = sp.PIN.Input(22)
LS_Tutup = sp.PIN.Input(27)

Motor1 = sp.PIN.Output(15)
Motor2 = sp.PIN.Output(18)
Solenoid = sp.PIN.Output(14)

try:
    while True:
        Selenoid.kunci()
        time.sleep(1)
        Selenoid.buka()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    IO.clean()
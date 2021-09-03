import RPi.GPIO as GPIO

class PIR:
    def __init__(self, pinPIR):
        self.pinPIR = pinPIR
        GPIO.setup(self.pinPIR, GPIO.IN)
        
    def detect(self):
        GPIO.input(self.pinPIR)

class L_Switch:
    def __init__(self, pinBuka, pinTutup):
        self.pinBuka = pinBuka
        self.pinTutup = pinTutup
        GPIO.setup(self.pinBuka, GPIO.IN)
        GPIO.setup(self.pinTutup, GPIO.IN)
    
    def LS_Buka(self):
        GPIO.input(self.pinBuka)
    
    def LS_Tutup(self):
        GPIO.input(self.pinTutup)
        
class Solenoid:
    def __init__(self, pinSol):
        self.pinSol = pinSol
        GPIO.setup(self.pinSol, GPIO.OUT)
    
    def buka(self):
        GPIO.output(self.pinSol, 0)

    def kunci(self):
        GPIO.output(self.pinSol, 1)

class driverMotor:
    def __init__(self, pinLogic1, pinLogic2):
        self.pinLogic1 = pinLogic1
        self.pinLogic2 = pinLogic2
        GPIO.setup(self.pinLogic1, GPIO.OUT)
        GPIO.setup(self.pinLogic2, GPIO.OUT)

def setupPintu():
    print("Memastikan Pintu Tertutup")

def cleanGPIO():
    GPIO.cleanup()
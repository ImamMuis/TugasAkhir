import RPi.GPIO as GPIO

class PIR:
    def __init__(self, pinPIR):
        self.pinPIR = pinPIR
        GPIO.setup(self.pinPIR, GPIO.IN)
        
    def detect(self):
        GPIO.input(self.pinPIR)

def setupPintu():
    print("Memastikan Pintu Tertutup")

def cleanGPIO():
    GPIO.cleanup()
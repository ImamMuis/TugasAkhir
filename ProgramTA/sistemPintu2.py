import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class PIR:
    def __init__(self, pinPIR):
        self.pinPIR = pinPIR
        GPIO.setup(self.pinPIR, GPIO.IN)
        print('PIR di pin', self.pinPIR)
        
    def userMasuk(self):
        print('PIR Mendeteksi')
        GPIO.input(self.pinPIR)

class L_Switch:
    def __init__(self, pinBuka, pinTutup):
        self.pinBuka = pinBuka
        self.pinTutup = pinTutup
        GPIO.setup(self.pinBuka, GPIO.IN)
        GPIO.setup(self.pinTutup, GPIO.IN)
        print('LSBuka di pin', self.pinBuka)
        print('LSTutup di pin', self.pinTutup)
            
    def LS_Buka(self):
        GPIO.input(self.pinBuka)
        print('Pintu terbuka')
    
    def LS_Tutup(self):
        GPIO.input(self.pinTutup)
        print('Pintu tertutup')
        
class Solenoid:
    def __init__(self, pinSol):
        self.pinSol = pinSol
        GPIO.setup(self.pinSol, GPIO.OUT)

    def buka(self):
        GPIO.output(self.pinSol, 1)
        
    def kuncin(self):
        GPIO.output(self.pinSol, 0)

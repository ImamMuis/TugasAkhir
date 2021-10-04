import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class PIR:
    def __init__(self, pinPIR):
        self.pinPIR = pinPIR
        GPIO.setup(self.pinPIR, GPIO.IN)
        print('GPIO', self.pinPIR, 'sebagai Input  PIR')
        
    def userMasuk(self):
        print('PIR Mendeteksi')
        GPIO.input(self.pinPIR)

class L_Switch:
    def __init__(self, pinBuka, pinTutup):
        self.pinBuka = pinBuka
        self.pinTutup = pinTutup
        GPIO.setup(self.pinBuka, GPIO.IN)
        GPIO.setup(self.pinTutup, GPIO.IN)
        print('GPIO', self.pinBuka, 'sebagai Input  LS_Buka')
        print('GPIO', self.pinTutup, 'sebagai Input  LSTutup')
            
    def Buka(self):
        if GPIO.input(self.pinBuka) == True:
            print('Pintu terbuka')
    
    def Tutup(self):
        if GPIO.input(self.pinTutup) == True:
            print('Pintu tertutup')
        
class Solenoid:
    def __init__(self, pinSol):
        self.pinSol = pinSol
        GPIO.setup(self.pinSol, GPIO.OUT)
        print('GPIO', self.pinSol, 'sebagai Output Solenoid')

    def buka(self):
        GPIO.output(self.pinSol, 1)
        print('Solenoid terbuka')
        
    def kunci(self):
        GPIO.output(self.pinSol, 0)
        print('Solenoid terkunci')

class driverMotor:
    def __init__(self, pinLogic1, pinLogic2):
        self.pinLogic1 = pinLogic1
        self.pinLogic2 = pinLogic2
        print('GPIO', self.pinLogic1, 'sebagai Output pinMotor1')
        print('GPIO', self.pinLogic2, 'sebagai Output pinMotor2')

    def forward(self):
        GPIO.output(self.pinLogic1, 0)
        GPIO.output(self.pinLogic2, 1)
        print('Rotasi motor: Forward')
    
    def reverse(self):
        GPIO.output(self.pinLogic1, 1)
        GPIO.output(self.pinLogic2, 0)
        print('Rotasi motor: Reverse')
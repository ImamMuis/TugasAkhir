import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

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
    
        
class driverServo:
    def __init__(self, pinServo1, pinServo2, pinMotor):
        self.pinServo1 = pinServo1
        self.pinServo2 = pinServo2
        self.pinMotor = pinMotor
        
    def frequency(self, freq):
        pca.frequency = freq
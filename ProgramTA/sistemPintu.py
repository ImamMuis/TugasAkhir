import time
import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

motorPWM_Channel = 3
motorZERO = 0
motorMIN = 13653
motorMAX = 2 ** 16 - 1
GPIO.setmode(GPIO.BCM)

class PIR:
    def __init__(self, pinPIR):
        self.pinPIR = pinPIR
        GPIO.setup(self.pinPIR, GPIO.IN)
        
    def detect(self):
        GPIO.input(self.pinPIR)

    def setup(self):
        print("Menyiapkan Sensor PIR...") 
        time.sleep(0.5)

        while GPIO.input(self.pinPIR) == 1:
            print("Sensor PIR belum siap")
            print("Mohon untuk tidak ada pergerakan terlebih dahulu!\n")
            time.sleep(0.5)

        print("Sensor PIR Siap!\n")
        time.sleep(0.5)

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

    def bukaPintu(self):
        GPIO.output(self.pinLogic1, 1)
        GPIO.output(self.pinLogic2, 0)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    def tutupPintu(self):
        GPIO.output(self.pinLogic1, 0)
        GPIO.output(self.pinLogic2, 1)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    def tutupPintu(self):
        GPIO.output(self.pinLogic1, 0)
        GPIO.output(self.pinLogic2, 1)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    def motorStop(self, forceBreak = 0):
        if forceBreak == 0:
            print("Motor Stop\n")
            motorSpeed(motorMIN, motorZERO, -200, 1)

        elif forceBreak == 1:
            GPIO.output(self.pinLogic1, 0)
            GPIO.output(self.pinLogic2, 0)
            
class LED_Indicator:
    def __init__(self, LEDMerah, LEDKuning, LEDHijau):
        self.LEDMerah = LEDMerah
        self.LEDKuning = LEDKuning
        self.LEDHijau = LEDHijau
        GPIO.setup(self.LEDMerah, GPIO.OUT)
        GPIO.setup(self.LEDKuning, GPIO.OUT)
        GPIO.setup(self.LEDHijau, GPIO.OUT)
    

    def Merah(self):
        GPIO.output(self.LEDMerah, 1)
        GPIO.output(self.LEDKuning, 0)
        GPIO.output(self.LEDHijau, 0)

    def Kuning(self):
        GPIO.output(self.LEDMerah, 0)
        GPIO.output(self.LEDKuning, 1)
        GPIO.output(self.LEDHijau, 0)

    def Hijau(self):
        GPIO.output(self.LEDMerah, 0)
        GPIO.output(self.LEDKuning, 0)
        GPIO.output(self.LEDHijau, 1)

class driverServo:
    def __init__(self, servoX, servoY, PWMMotor):
        self.servoX = servoX
        self.servoY = servoY
        self.PWMMotor = PWMMotor
    
def motorSpeed(begin, end, step, accel):    
    if accel == 0:
        pca.channels[motorPWM_Channel].duty_cycle = motorMIN
        time.sleep(0.02)   
    elif accel == 1:
        for i in range(begin, end, step):
            pca.channels[motorPWM_Channel].duty_cycle = i
            if GPIO.input(pin_pintuBuka) or GPIO.input(pin_pintuTutup) == 1:
                break
            time.sleep(0.02)
            
def setupPintu():
    print("Memastikan Pintu Tertutup")

def cleanGPIO():
    GPIO.cleanup()
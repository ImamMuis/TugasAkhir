import time
# import busio
# import RPi.GPIO as GPIO
# from board import SCL, SDA
# from adafruit_pca9685 import PCA9685

GPIO.setmode(GPIO.BCM)
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
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
        
class driverMotor(L_Switch, driverServo):
    def __init__(self, pinLogic1, pinLogic2):
        self.pinLogic1 = pinLogic1
        self.pinLogic2 = pinLogic2
        GPIO.setup(self.pinLogic1, GPIO.OUT)
        GPIO.setup(self.pinLogic2, GPIO.OUT)
        
    def setSpeed(speedMIN, speedMAX):
        return speedMIN, speedMAX
    
    def motorSpeed(begin, end, step, accel):
        pca.channels[super().pinMotor].duty_cycle = 13653
        time.sleep(0.02)
        
        if accel == 0:
            pca.channels[super().pinMotor].duty_cycle = begin
            
        elif accel == 1:
            for i in range(begin, end, step):
                pca.channels[super().pinMotor].duty_cycle = i
                if super().LS_Buka or super().LS_Tutup == 1:
                    break
        else:
            print("Parameter 'accel' harus 0 atau 1!")
    
    def motorStop(forceBreak = 0):
        if forceBreak == 0:
            motorSpeed(16384, motorZERO, -15, 0)
        elif forceBreak == 1:
            GPIO.output(pin_motorLogic1, 0)
            GPIO.output(pin_motorLogic2, 0)

    def bukaPintu(self):
        Min, Max = super().setSpeed()
        GPIO.output(self.pinLogic1, 1)
        GPIO.output(self.pinLogic2, 0)
        super().motorSpeed(Min, Max, 4, 1)
        
    def tutupPintu(self):
        Max, Min = super().setSpeed()
        GPIO.output(self.pinLogic1, 0)
        GPIO.output(self.pinLogic2, 1)
        super().motorSpeed(Min, Max, 4, 1)

class Pintu:
    def __init__(self):
        pass


    def tutupPintu(self):
        return super().tutupPintu()

class Tele:
    def __init__(self, token):
        self.token = token
        telegram_bot = telepot.Bot(self.token)
        
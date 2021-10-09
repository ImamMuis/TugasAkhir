import time
import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

pin_solenoid    = 14
pin_pintuBuka   = 22
pin_pintuTutup  = 27
pin_motorLogic1 = 15
pin_motorLogic2 = 18
motorPWM_Channel = 2

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50
# GPIO.setmode(GPIO.BCM)

# waktuPintuTerbuka = 0

GPIO.setup(pin_pintuBuka, GPIO.IN)
GPIO.setup(pin_pintuTutup, GPIO.IN)
GPIO.setup(pin_solenoid, GPIO.OUT)
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)

def motorStart(mode):
    motorMIN = 2 ** 12
    motorMAX = 2 ** 16 - 1
    if mode == "REVERSE":
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        
    elif mode == "FORWARD":
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)
        motorSpeed(motorMIN, motorMAX, 4, 1)
    
    elif mode == "CLOSE":
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, 0, 0, 0)
    else:
        print("Nilai 'mode' harus FORWARD, REVERSE atau CLOSE!\n")

def motorStop(forceBreak = 0):
    motorZERO = 0
    if forceBreak == 0:
        motorSpeed(16384, motorZERO, -15, 0)
    elif forceBreak == 1:
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 0)
    

def motorSpeed(begin, end, step, accel):    
    pca.channels[motorPWM_Channel].duty_cycle = 13653
    time.sleep(0.02)
    
    if accel == 0:
        pca.channels[motorPWM_Channel].duty_cycle = begin
        
    elif accel == 1:
        for i in range(begin, end, step):
            pca.channels[motorPWM_Channel].duty_cycle = i
            if GPIO.input(pin_pintuBuka) or GPIO.input(pin_pintuTutup) == 1:
                break
        
def sistemPintu(kondisi):
    if kondisi == "Buka":
        GPIO.output(pin_solenoid, 1)
        time.sleep(0.5)
        print("Pintu dibuka\n")
        while GPIO.input(pin_pintuBuka) == 0:
            motorStart("FORWARD")
    elif kondisi == "Tutup":
        print("Pintu ditutup\n")
        while GPIO.input(pin_pintuTutup) == 0:
            motorStart("REVERSE")
        GPIO.output(pin_solenoid, 0)
            
    motorStop(1)
    time.sleep(0.1)
    
def setupPIR(pin_sensorPIR):
    print("Menyiapkan Sensor PIR...")
    GPIO.setup(pin_sensorPIR, GPIO.IN)
    while GPIO.input(pin_sensorPIR) == 1:
        print("Sensor PIR belum siap")
        print("Mohon untuk tidak ada pergerakan terlebih dahulu!\n")
        time.sleep(1)
    print("Sensor PIR Siap!\n")
    time.sleep(0.1)
    
def setupPintu():
    print("Memastikan Pintu Tertutup")
    if GPIO.input(pin_pintuTutup) == 0:
        print("Pintu sedang terbuka! Pintu akan ditutup...")
        GPIO.output(pin_solenoid, 1)
        while GPIO.input(pin_pintuTutup) == 0:
            motorStart(mode = "CLOSE")        
    motorStop(1)
    print("Pintu sudah tertutup!\n")
    time.sleep(0.5)
    GPIO.output(pin_solenoid, 0)
    
def waktuTunggu(pin_sensorPIR):
    waktuPintuTerbuka = 0
    while waktuPintuTerbuka < 10:
        if waktuPintuTerbuka < 5:
            print("Pintu sudah terbuka, silakan masuk")
        else:
            timerPintu = 10-waktuPintuTerbuka
            print("\nMohon segera masuk")
            print("Pintu akan ditutup dalam waktu ", timerPintu, "detik")
            
        if GPIO.input(pin_sensorPIR) == 1:
            print("\nAnda sudah masuk")
            break
        waktuPintuTerbuka += 1   
        time.sleep(1)
        
    if waktuPintuTerbuka == 10:
        print("\nAnda tidak segera masuk")
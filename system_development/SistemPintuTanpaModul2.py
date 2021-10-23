import time
import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

waktuPintuTerbuka = 0
motorPWM_Channel = 3
motorZERO = 0
motorMIN = 2 ** 15
motorMAX = 2 ** 16 - 1
GPIO.setmode(GPIO.BCM)

pin_LedMerah    = 9
pin_LedKuning   = 10
pin_LedHijau    = 11
pin_solenoid    = 14
pin_pintuBuka   = 22
pin_pintuTutup  = 27
pin_sensorPIR   = 17
pin_motorLogic1 = 15
pin_motorLogic2 = 18

GPIO.setup(pin_sensorPIR, GPIO.IN)
GPIO.setup(pin_pintuBuka, GPIO.IN)
GPIO.setup(pin_pintuTutup, GPIO.IN)
GPIO.setup(pin_solenoid, GPIO.OUT)
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)
GPIO.setup(pin_LedMerah, GPIO.OUT)
GPIO.setup(pin_LedKuning, GPIO.OUT)
GPIO.setup(pin_LedHijau, GPIO.OUT)

GPIO.output(pin_solenoid, 0)
GPIO.output(pin_motorLogic1, 0)
GPIO.output(pin_motorLogic2, 0)
time.sleep(0.5)

def motorStart(mode):
    if mode == "FORWARD":
        print("Mode: Forward\n")
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    elif mode == "REVERSE":
        print("Mode: Reverse\n")
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    elif mode == "CLOSE":
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, 0, 0, 0)

    else:
        print("Parameter 'mode' harus FORWARD atau REVERSE!\n")

def motorStop(forceBreak = 0):
    if forceBreak == 0:
        print("Motor Stop\n")
        motorSpeed(motorMIN, motorZERO, -200, 1)
    elif forceBreak == 1:
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 0)
    
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

def setupPIR():
    print("Menyiapkan Sensor PIR...") 
    time.sleep(0.5)

    while GPIO.input(pin_sensorPIR) == 1:
        print("Sensor PIR belum siap")
        print("Mohon untuk tidak ada pergerakan terlebih dahulu!\n")
        time.sleep(0.5)

    print("Sensor PIR Siap!\n")
    time.sleep(0.5)

def setupPintu():
    print("Memastikan Pintu Tertutup")
    if GPIO.input(pin_pintuTutup) == 0:
        print("Pintu sedang terbuka! Pintu akan ditutup...")
        GPIO.output(pin_solenoid, 1)
        while GPIO.input(pin_pintuTutup) == 0:
            motorStart("CLOSE")        
    motorStop(1)
    print("Pintu sudah tertutup!\n")
    time.sleep(2)
    GPIO.output(pin_solenoid, 0)

def sistemPintu(kondisi):
    if kondisi == "Buka":
        print("Pintu dibuka")
        LedIndicator(0, 1, 0) 
        GPIO.output(pin_solenoid, 1)
        time.sleep(0.5)

        while GPIO.input(pin_pintuBuka) == 0:
            motorStart("FORWARD")
        
        print("Pintu terbuka")
        LedIndicator(0, 0, 1) 

    elif kondisi == "Tutup":
        print("Pintu ditutup")
        LedIndicator(0, 1, 0) 

        while GPIO.input(pin_pintuTutup) == 0:
            motorStart("REVERSE")

        time.sleep(0.5)
        GPIO.output(pin_solenoid, 0)
        print("Pintu tertutup")y
        LedIndicator(1, 0, 0) 
    motorStop(1)
    time.sleep(0.1)

def checkUser():
    global waktuPintuTerbuka
    user = input("Wajah dikenali? y/n:")

    if user == 'y':
        sistemPintu("Buka")
        while waktuPintuTerbuka < 10:
            if GPIO.input(pin_sensorPIR) == 1:
                print("Anda sudah masuk")
                break

            if waktuPintuTerbuka < 5:
                print("Pintu sudah terbuka, silakan masuk")

            else:
                timerPintu = 10-waktuPintuTerbuka
                print("Mohon segera masuk")
                print("Pintu akan ditutup dalam waktu ", timerPintu, "detik\n")

            waktuPintuTerbuka += 1   
            time.sleep(1)
            
        if waktuPintuTerbuka == 10:
            print("Anda tidak segera masuk")

        waktuPintuTerbuka = 0
        
        sistemPintu("Tutup")
        
    elif user == 'n':
        print("Kirim foto ke telegram...")

def LedIndicator(merah, kuning, hijau):
    global pin_LedMerah
    global pin_LedKuning
    global pin_LedHijau
    
    GPIO.output(pin_LedMerah, merah)
    GPIO.output(pin_LedKuning, kuning)
    GPIO.output(pin_LedHijau, hijau)

try:
    LedIndicator(0, 1, 0)
    setupPIR()
    setupPintu()
    LedIndicator(1, 0, 0)

    while True:
        checkUser()

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    GPIO.cleanup()
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
motorMIN = 27306
motorMAX = 2 ** 16 - 1
GPIO.setmode(GPIO.BCM)

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

def motorStart(mode):
    if mode == "REVERSE":
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, 16384,      2, 1)
        motorSpeed(16384,    motorMAX, 100, 1)
        
    elif mode == "FORWARD":
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)
        motorSpeed(motorMIN, 16384,      2, 1)
        motorSpeed(16384,    motorMAX, 100, 1)
    
    elif mode == "CLOSE":
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, 0, 0, 0)
    else:
        print("Parameter 'mode' harus FORWARD, REVERSE atau CLOSE!\n")

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
            time.sleep(0.02 )
        
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
#         time.sleep(5)
        GPIO.output(pin_solenoid, 0)
#         time.sleep(1)
            
    motorStop(1)
    time.sleep(0.1)

try:    
    print("Menyiapkan Sensor PIR...") 
    while GPIO.input(pin_sensorPIR) == 1:
        print("Sensor PIR belum siap")
        print("Mohon untuk tidak ada pergerakan terlebih dahulu!\n")
        time.sleep(1)
    print("Sensor PIR Siap!\n")
    time.sleep(0.5)
    
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
    
    while True:
        user = input("Wajah dikenali? y/n:")
        
        if user == 'y':
            sistemPintu("Buka")
            
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
            waktuPintuTerbuka = 0
            
            sistemPintu("Tutup")
            
        elif user == 'n':
            print("Kirim foto ke telegram...")
                
except KeyboardInterrupt:
    print("\nProgram Stop")

except:
    print("\nOther Error or exception occured!")

finally:
    motorStop()
    GPIO.cleanup()
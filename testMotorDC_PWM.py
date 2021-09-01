import time
import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)

pca.frequency = 50
pin_motorLogic1 = 15
pin_motorLogic2 = 18
motorPWM_Channel = 3
motorZERO = 0
motorMIN = 27306
motorMAX = 2 ** 16 - 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)

def motorStart(mode):
    print("Motor Start")

    if mode == "FORWARD":
        print("Mode: Forward\n")
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)
        motorSpeed(motorMIN, motorMAX, 300, 1)

    elif mode == "REVERSE":
        print("Mode: Reverse\n")
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, motorMAX, 300, 1)

    else:
        print("Parameter 'mode' harus FORWARD atau REVERSE!\n")

def motorStop():
    print("Motor Stop\n")
    motorSpeed(motorMIN, motorZERO, -200, 1)
    GPIO.output(pin_motorLogic1, 0)
    GPIO.output(pin_motorLogic2, 0)

def motorSpeed(begin, end, step, accel):
    if accel == 1:
        pca.channels[motorPWM_Channel].duty_cycle = motorMIN
        time.sleep(0.02)

    for i in range(begin, end, step):
        pca.channels[motorPWM_Channel].duty_cycle = i
        time.sleep(0.02)
        
try:
    while True:
        motorStart("FORWARD")
        motorStop()
        time.sleep(1)

        motorStart("REVERSE")
        motorStop()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    motorStop()
    GPIO.cleanup()
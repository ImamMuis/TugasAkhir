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
motorMIN = 2 ** 12
motorMAX = 2 ** 16 - 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)

def motorSpeed(begin, end, step, accel):
    if accel == 1:
        pca.channels[motorPWM_Channel].duty_cycle = 32768
        time.sleep(0.02)

    for i in range(begin, end, step):
        pca.channels[motorPWM_Channel].duty_cycle = i
        time.sleep(0.02)
        
def motorStop():
    print("Motor Stop\n")
    motorSpeed(32768, 0, -200, 0)
    GPIO.output(pin_motorLogic1, 0)
    GPIO.output(pin_motorLogic2, 0)

try:
    while True:
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)
        time.sleep(0.02)
        
        pca.channels[motorPWM_Channel].duty_cycle = 27306
        time.sleep(0.02)
        
        for i in range(27306, 65535, 100):
            if i > 65535:
                i = 65535
            pca.channels[motorPWM_Channel].duty_cycle = i
            time.sleep(0.02)
            
        time.sleep(0.02)
        for i in range(65535, 27306, -100):
            if i < 27306:
                i = 27306             
            pca.channels[motorPWM_Channel].duty_cycle = i
            time.sleep(0.02)
            
        time.sleep(0.02)
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 0)
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    motorStop()
    GPIO.cleanup()
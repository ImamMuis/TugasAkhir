# Library untuk Motor DC
# Library untuk delay
import time

# Library untuk menggunakan komunikasi I2C
import busio
from board import SCL, SDA

# Library untuk menggunakan GPIO Raspberry
import RPi.GPIO as GPIO

# Library untuk menggunakan Driver Servo PCA9685 
from adafruit_pca9685 import PCA9685

# Mengatur Driver Servo berkomunikasi dengan Raspberry
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)

# Konfigurasi Driver Servo & Motor
V_in    = 24 #V (Tegangan untuk motor DC)
freq    = 50 #Hz (Frekuensi PWM)
PWM_Res = 2 ** 16 - 1 #Lebar bit PWM
pca.frequency = freq

# Pin GPIO 15 dan 18 sebagai pengatur arah rotasi motor
pin_motorLogic1 = 15
pin_motorLogic2 = 18

# Channel PWM 2 Driver Servo sebagai pengatur kecepatan motor DC
motorPWM_Channel = 2

# Batas motor untuk berhenti
motorZERO = 0

# Batas minimal motor bergerak (Duty Cycle: 6% atau 2V)
motorMIN = 2 ** 12

# Batas minimal motor bergerak (Duty Cycle: 100% atau 24V)
motorMAX = PWM_Res

# Memakai GPIO mode BCM
GPIO.setmode(GPIO.BCM)

# Mengatur pin arah rotasi motor sebagai output
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)

# Fungsi untuk menggerakkan motor
# Parameter: 'mode', diisi dengan FORWARD atau REVERSE
# FORWARD: Buka Pintu
# REVERSE: Tutup Pintu
def motorStart(mode):
    
    # Print untuk mengetahui perintah yang akan dieksekusi
    print("Motor Start")

    # Jika parameter 'moode' diisi FORWARD, maka
    # Pin arah rotasi motor diatur menjadi 1 dan 0
    if mode == "FORWARD":
        print("Mode: Forward\n")

        # GPIO diatur agar motor berputar FORWARD
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)

        # Motor bergerak dengan parameter:
        # Kecepatan awal: motorMIN (2V)
        # Kecepatan akhir: motorMAX (24V)
        # Nilai increment: 4 (kecepatan naik)
        # Nilai Akselerasi: 1 (Ya)
        motorSpeed(motorMIN, motorMAX, 4, 1)
    

    # Jika parameter 'moode' diisi REVERSE, maka
    # Pin arah rotasi motor diatur menjadi 0 dan 1
    elif mode == "REVERSE":
        print("Mode: Reverse\n")

        # GPIO diatur agar motor berputar REVERSE
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)

        # Motor bergerak dengan parameter:
        # Kecepatan awal: motorMIN (2V)
        # Kecepatan akhir: motorMAX (24V)
        # Nilai increment: 4 (kecepatan naik)
        # Nilai Akselerasi: 1 (Ya)
        motorSpeed(motorMIN, motorMAX, 4, 1)

    # Kondisi jika parameter 'mode' tidak diisi FORWARD ataupun REVERSE
    else:
        print("Parameter 'mode' harus FORWARD atau REVERSE!\n")

# Fungsi untuk menghentikan motor
def motorStop():

    # Print untuk mengetahui perintah yang akan dieksekusi
    print("Motor Stop\n")

    # Motor bergerak dengan parameter:
    # Kecepatan awal: motorMAX (24V)
    # Kecepatan akhir: motorZERO (0V)
    # Nilai decrement: -15 (kecepatan turun)
    # Nilai Akselerasi: 0 (Tidak)  
    motorSpeed(motorMAX, motorZERO, -15, 0)

    # GPIO diatur agar motor diam
    GPIO.output(pin_motorLogic1, 0)
    GPIO.output(pin_motorLogic2, 0)

# Fungsi untuk mengeksekusi perputaran motor dengan Parameter:
# begin: Kecepatan awal motor
# end  : Kecepatan akhir motor
# step : Nilai increment/decrement perubahan kecepatan motor
# accel: Nilai Akselerasi
def motorSpeed(begin, end, step, accel):

    # Jika parameter akselerasi bernilai 1, maka
    # Motor diinisiasi dengan nilai PWM 13653 (5V) 
    if accel == 1:
        # Channel PWM 2 pada Driver Servo
        # mengeluarkan nilai PWM sebesar 13653
        # atau Duty Cycle 20,83% dari nilai max 65535 
        pca.channels[motorPWM_Channel].duty_cycle = 13653

        # Delay 20ms
        time.sleep(0.02)

    # Perulangan untuk perubahan kecepatan motor
    for i in range(begin, end, step):
        pca.channels[motorPWM_Channel].duty_cycle = i

def motorCalc(value, selector):
    # 1: Input berupa PWM
    # 2: Input berupa Duty Cycle
    # 3: Input berupa V_out

    perioda = 1 / freq

    if selector == "PWM":
        PWM_Out = value
        if PWM_Out > PWM_Res:
            print("Nilai PWM terlalu besar!")

        dutyCycle = PWM_Out / PWM_Res 
        V_Out = dutyCycle * V_in 

    elif selector == "DUTYCYCLE":
        dutyCycle = value
        if dutyCycle > 100:
            print("Nilai Duty Cycle terlalu besar!")

        V_Out = dutyCycle * V_in 
        PWM_Out = dutyCycle * PWM_Res

    elif selector == "VOUT":
        V_Out = value
        if V_Out > V_in:
            print("Nilai V_out terlalu besar!")

        dutyCycle = V_Out / V_in
        PWM_Out = dutyCycle * PWM_Res

    else:
        print("Parameter 'value' harus PWM, DUTYCYCLE atau VOUT!\n")

    T_on = dutyCycle * perioda
    T_off = perioda - T_on

    print("Perioda   :", perioda, "ms")
    print("PWM       :", PWM_Out)
    print("Duty Cycle:", dutyCycle, "%")
    print("Voltage   :", V_Out, "V")
    print("Time On   :", T_on, "ms")
    print("Time Off  :", T_off, "ms")
    print("")
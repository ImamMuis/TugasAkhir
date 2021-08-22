import time
import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

# Mengatur Driver Servo berkomunikasi dengan Raspberry
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)

# Frekuensi Driver Servo
pca.frequency = 50

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
motorMAX = 2 ** 16 - 1

# Memakai GPIO mode BCM
GPIO.setmode(GPIO.BCM)

# Mengatur pin arah rotasi motor sebagai output
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)

# Fungsi untuk menggerakkan motor
# Parameter: FORWARD atau REVERSE
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
        
try:

    # Perulangan While akan terus dieksekusi (infinite)
    # karena kondisi selau benar (True)
    while True:

        # Memanggil Fungsi motorStart dengan parameter FORWARD
        # agar motor membuka pintu
        motorStart("FORWARD")

        # Memanggil Fungsi motorStop agar motor berhenti
        motorStop()

        # Delay 1 detik
        time.sleep(1)
        
        # Memanggil Fungsi motorStart dengan parameter REVERSE
        # agar motor menutup pintu
        motorStart("REVERSE")

        # Memanggil Fungsi motorStop agar motor berhenti
        motorStop()

        # Delay 1 detik
        time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    motorStop()
    GPIO.cleanup()
import time, RPi.GPIO as GPIO

pin_sensorPIR   = 17
kondisiSebelum  =  0
kondisiSekarang =  0

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_sensorPIR, GPIO.IN)

try:
    print("Menyiapkan Sensor PIR...") 
    time.sleep(0.5)

    while GPIO.input(pin_sensorPIR) == 1:
        print("Sensor PIR belum siap")
        print("Mohon untuk tidak ada pergerakan terlebih dahulu!\n")
        time.sleep(0.5)

    print("Sensor PIR Siap!\n")
    time.sleep(0.5)
    
    while True:
        kondisiSekarang = GPIO.input(pin_sensorPIR)

        if kondisiSekarang == 1 and kondisiSebelum == 0:
            print("Pergerakan terdeteksi!")
            time.sleep(1)
            kondisiSebelum = 1

        elif kondisiSekarang == 0 and kondisiSebelum == 1:
            print("Pergerakan hilang")
            time.sleep(1)
            kondisiSebelum = 0
            
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    GPIO.cleanup()
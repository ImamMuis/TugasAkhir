import time, RPi.GPIO as GPIO

pin_sensorPIR = 17
kondisi = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_sensorPIR, GPIO.IN)

try:
    print("Menyiapkan Sensor PIR...") 
    time.sleep(0.5)
    while GPIO.input(pin_sensorPIR) == 1:
        print("Sensor PIR belum siap")
        time.sleep(0.5)
    print("Sensor PIR Siap!\n")
    time.sleep(0.5)
    
    while True:
        kondisi = GPIO.input(pin_sensorPIR)
        if kondisi == 1:
            print("Pergerakan Terdeteksi!")
            time.sleep(1)
        else:
            print("Tidak ada pergerakan")
            time.sleep(1)

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")

finally:
    GPIO.cleanup()

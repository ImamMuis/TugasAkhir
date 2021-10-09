import RPi.GPIO as GPIO
import sistemPintu0 as sp

GPIO.setmode(GPIO.BCM)

pin_sensorPIR = 17
GPIO.setup(pin_sensorPIR, GPIO.IN)

try:    
    sp.setupPIR(pin_sensorPIR)
    sp.setupPintu()
    
    while True:
        user = input("Wajah dikenali? y/n:")
        
        if user == 'y':
            sp.sistemPintu("Buka")
            sp.waktuTunggu(pin_sensorPIR)
            sp.sistemPintu("Tutup")
            
        elif user == 'n':
            print("Kirim foto ke telegram...")
                
except KeyboardInterrupt:
    print("\nProgram Stop")

except:
    print("\nOther Error or exception occured!")

finally:
    sp.motorStop()
    GPIO.cleanup()
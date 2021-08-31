import RPi.GPIO as GPIO
import sistemPintu1 as sp
import sistemKamera as sk

GPIO.setmode(GPIO.BCM)
maxUser = 8
waktuTunggu = 15

sp.PIR(22)
sp.Solenoid(14)
sp.L_Switch(17, 27)
sp.driverMotor(15, 18)

servo0	  = 0
servo1	  = 1
PWM_Motor = 2

sk.driverServo(servo0, servo1, PWM_Motor)
sk.driver()

try:  
    sp.PIR.setup()
    sp.Pintu.setup()
    sp.Solenoid.kunci()
    
    while True:
        jumlahUser = input("Jumlah User di ruangan: ")
        if jumlahUser < maxUser:
            user = input("Wajah dikenali? y/n: ")
            if user == 'y':
                sp.Solenoid.buka()
                sp.Pintu.buka()
                sp.Pintu.tunggu(waktuTunggu)
                if sp.PIR.userMasuk() == True:
                    sp.Tele.notifMasuk()
                sp.Pintu.tutup()
                sp.Solenoid.kunci()
            else:    
                sk.Webcam.foto()
                sp.Tele.tidakDikenal()
        else:
            print("RUANGAN PENUH!")

except KeyboardInterrupt:
    print("\nProgram Stop")

except:
    print("\nOther Error or exception occured!")

finally:
    # motorStop()
    GPIO.cleanup()


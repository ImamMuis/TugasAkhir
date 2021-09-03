import time
import sistemPintu as sp
# import sistemKamera as sk

names = ['Unknown', 'Imam', 'Iis']

sp.PIR(17)
sp.Solenoid(14)
sp.L_Switch(22, 27)
sp.driverMotor(15, 18)
sp.LED_Indicator(9, 10, 11)

waktuTunggu = 0
# channelServoX   = 0
# channelServoY   = 1
# ChannelPWMMotor = 2
# sk.driverServo(channelServoX, channelServoY, ChannelPWMMotor)

try:  
    sp.PIR.setup()
    sp.Pintu.setup()
    sp.Solenoid.kunci()
    
    while True:       
        user = input("Wajah dikenali? y/n: ")
        if user == 'y':
            sp.Solenoid.buka()
            sp.Pintu.buka()


            while waktuPintuTerbuka < 10:
                if sp.PIR.userMasuk() == True:
                    print("User Masuk")
                    # sk.Webcam.foto()
                    # sp.Tele.notifMasuk()
                
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
            sp.Pintu.tutup()
            sp.Solenoid.kunci()

        else:    
            print("User tidak dikenal")
            # sk.Webcam.foto()
            # sp.Tele.notifTidakDikenal()

except KeyboardInterrupt:
    print("Program Stop")

except:
    print("Other Error or exception occured!")
    
finally:
    sp.CleanGPIO()
import sistemPintu as sp
import sistemKamera as sk

names = ['Unknown', 'Imam', 'Iis']

sp.PIR(17)
sp.Solenoid(14)
sp.L_Switch(22, 27)
sp.driverMotor(15, 18)
sp.LED_Indicator(9, 10, 11)

waktuTunggu = 0
channelServoX   = 0
channelServoY   = 1
ChannelPWMMotor = 2
sk.driverServo(channelServoX, channelServoY, ChannelPWMMotor)

try:  
    sp.PIR.setup()
    sp.Pintu.setup()
    sp.Solenoid.kunci()
    
    while True:       
        user = input("Wajah dikenali? y/n: ")
        if user == 'y':
            sp.Solenoid.buka()
            sp.Pintu.buka()
            if sp.PIR.userMasuk() == True:
                sk.Webcam.foto()
                sp.Tele.notifMasuk()
            sp.Pintu.tutup()
            sp.Solenoid.kunci()
        else:    
            sk.Webcam.foto()
            sp.Tele.notifTidakDikenal()

except KeyboardInterrupt:
    print("Program Stop")

finally:
    sp.CleanGPIO()
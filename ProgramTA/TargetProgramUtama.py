import RPi.GPIO as GPIO
import sistemPintu as sp
import sistemKamera as sk

names = ['Unknown', 'Imam', 'Iis']

sp.PIR(17)
sp.Solenoid(14)
sp.L_Switch(22, 27)
sp.driverMotor(15, 18)
channelServoX   = 0
channelServoY   = 1
ChannelPWMMotor = 2

sk.driverServo(channelServoX, channelServoY, ChannelPWMMotor)
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'

sk.TeleBot.Token(tokenBot)


waktuTunggu = 0
try:  
    sp.PIR.setup()
    sp.Pintu.setup()
    sp.Solenoid.kunci()
    
    while True:
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

except KeyboardInterrupt:
    print("\nProgram Stop")

except:
    print("\nOther Error or exception occured!")

finally:
    # motorStop()
    GPIO.cleanup()


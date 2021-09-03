from ProgramTA.sistemPintu import PIR
import RPi.GPIO as GPIO
import sistemPintu as sp
import sistemKamera as sk

names = ['Unknown', 'Imam', 'Iis']

sp.PIR(17)
sp.L_Switch(22, 27)

sp.Solenoid(14)
sp.driverMotor(15, 18)
sp.LED_Indicator(9, 10, 11)

channelServoX   = 0
channelServoY   = 1
ChannelPWMMotor = 2

sk.driverServo(channelServoX, channelServoY, ChannelPWMMotor)
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'
bot = sk.Telebot(tokenBot)

waktuTunggu = 0
try:  
    SensorPIR.setup()
    sp.Pintu.setup()
    Solenoid.kunci()
    
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
    sp.CleanGPIO()
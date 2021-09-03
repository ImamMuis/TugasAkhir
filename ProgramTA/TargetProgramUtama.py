from ProgramTA.sistemPintu import PIR
import RPi.GPIO as GPIO
import sistemPintu as sp
import sistemKamera as sk

names = ['Unknown', 'Imam', 'Iis']

SensorPIR = sp.Input(17)
L_Switch = sp.Input(22, 27)
Solenoid = sp.Output(14)
DriverMotor = sp.Output(15, 18)

channelServoX   = 0
channelServoY   = 1
ChannelPWMMotor = 2

sk.driverServo(channelServoX, channelServoY, ChannelPWMMotor)
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'
bot = sk.Telebot(tokenBot)
# sp.PIR(17)
# sp.Solenoid(14)
# sp.L_Switch(22, 27)
# sp.driverMotor(15, 18)

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
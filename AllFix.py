import os
import cv2
import telepot
import datetime
import time
import busio
import RPi.GPIO as GPIO
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50

names = ['Unknown', 'Imam', 'Iis']

pin_LedMerah    = 9
pin_LedKuning   = 10
pin_LedHijau    = 11
pin_solenoid    = 14
pin_pintuBuka   = 22
pin_pintuTutup  = 27
pin_sensorPIR   = 17
pin_motorLogic1 = 15
pin_motorLogic2 = 18

faceCompare = 20
DetectedFace_Tolerance = 5

userDir = 'img_record'
teleBot_PWD = '201802014'
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

setX = 90
setY = 90
scanArea = [154, 154, 486, 326]

kit = ServoKit(channels=16)
kit.servo[0].angle = setX
kit.servo[1].angle = setY
kit.servo[0].set_pulse_width_range(500, 2750)
kit.servo[1].set_pulse_width_range(500, 2750)

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read('data_training/trainer.xml')

Id = 0
imgRGB = 0
count1 = 0
count2 = 0
chat_id = 0
Quit = False
faceState1 = False
faceState2 = False
TimeBetween = 0.0
DetectedFace_Last =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0
command = ""
faceResult_Now = ""
faceResult_Last = ""
totalUser = len(names)
countID = [0] * totalUser
detectResult = [0] * faceCompare

waktuPintuTerbuka = 0
motorPWM_Channel = 3
motorZERO = 0
motorMIN = 13653
motorMAX = 2 ** 16 - 1
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_sensorPIR, GPIO.IN)
GPIO.setup(pin_pintuBuka, GPIO.IN)
GPIO.setup(pin_pintuTutup, GPIO.IN)
GPIO.setup(pin_solenoid, GPIO.OUT)
GPIO.setup(pin_motorLogic1, GPIO.OUT)
GPIO.setup(pin_motorLogic2, GPIO.OUT)
GPIO.setup(pin_LedMerah, GPIO.OUT)
GPIO.setup(pin_LedKuning, GPIO.OUT)
GPIO.setup(pin_LedHijau, GPIO.OUT)

GPIO.output(pin_solenoid, 0)
GPIO.output(pin_motorLogic1, 0)
GPIO.output(pin_motorLogic2, 0)
time.sleep(0.1)

def Selisih(current, prev):
    num = float(current) - float(prev)
    if num < 0:
        num += 60
    num = round(num, 3)

    return num

def getCurrent(data):
    now = datetime.datetime.now()
    if data == "DATE":
        value = now.strftime("%a, %d - %b - %Y")

    elif data == "Date":
        value = now.strftime("%Y%m%d%H%M%S")

    elif data == "Time":
        value = now.strftime("%H:%M:%S")

    elif data == "second":
        value = str(round(float(str(now).split(":")[-1]), 3))

    else:
        print("WRONG PARAMETER!")

    return value

def saveImage(img):
    waktu = getCurrent("Date")
    namaFile = 'Snapshot.' + str(waktu) + '.jpg'
    cv2.imwrite(userDir + '/' + namaFile, img)

def sendImage(chatId):
    file = os.listdir('/home/pi/1.TugasAkhir/img_record')
    lastImage = sorted(file, key = lambda x: os.path.splitext(x)[0])
    foto = lastImage[-1]
    file = str(userDir) + '/' + str(foto)
    bot.sendPhoto(chatId, photo=open(file, 'rb'))

def teleBot(msg):
    global Quit
    global imgRGB
    global chat_id
    global command
    global teleBot_PWD

    QuitFlag = False
    chat_id = msg['chat']['id']
    command = msg['text']

    print("From User : %s" %chat_id)
    print("Command   : %s\n" %command)

    show_keyboard = {'keyboard':[	['Ambil Foto','Foto Terakhir'], 
                                    ['Waktu Sekarang','Stop Sistem ']
                            ]}

    if command == '/start':
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)

    elif command == 'Ambil Foto':
        saveImage(imgRGB)
        sendImage(chat_id)

    elif command == 'Foto Terakhir':
        sendImage(chat_id)

    elif command == 'Waktu Sekarang':
        now = datetime.datetime.now()
        value1 = now.strftime("Time: %H:%M:%S\n")
        value2 = now.strftime("Day : %a, %d - %b - %Y\n")
        bot.sendMessage(chat_id, str(value1)+str(value2))

    elif command == 'Stop Sistem':
        bot.sendMessage(chat_id, str('Masukan PIN untuk stop TeleBot'))
        QuitFlag = True

    elif command == teleBot_PWD:
        bot.sendMessage(chat_id, str('Sistem Face Recognition terhenti...'))
        Quit = True

    elif command != teleBot_PWD and QuitFlag == True:
        bot.sendMessage(chat_id, str('Password Salah!'))
        QuitFlag = False

    else:
        bot.sendMessage(chat_id, str("Input belum tersedia!"))
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard) 

def detectFace():
    global Id
    global setX
    global setY
    global count1
    global count2
    global imgRGB
    global chat_id
    global faceState1
    global faceState2
    global TimeBetween
    global DetectedFace_Last
    global notDetectedTime_Now
    global notDetectedTime_Last
    global DetectedFace_Tolerance
    global faceResult_Last
    global faceResult_Now
    global waktuPintuTerbuka

    size = [75, 85]
    jumlahWajah = 0

    succes, frame = cam.read()
    succes += succes
    imgRGB = cv2.flip(frame, 1)
    imgGray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.resize(imgGray, (220, 165))
    faces = faceDetector.detectMultiScale(imgGray, 1.2, 3)

    for x1, y1, w1, h1 in faces:
        x2 = int(round(x1 * 2.9, 0))
        y2 = int(round(y1 * 2.9, 0))
        w2 = int(round(w1 * 2.9, 0))
        h2 = int(round(h1 * 2.9, 0))
        cX = int(round(x2+w2/2, 0))
        cY = int(round(y2+h2/2, 0))

        imgRGB = cv2.rectangle(imgRGB, (x2, y2), (x2+w2, y2+h2), (186, 39, 59), 2)
        jumlahWajah = int(str(faces.shape[0]))
        Id, confidence = faceRecognizer.predict(imgGray[y1:y1+h1, x1:x1+w1])
        
        if cX < scanArea[0]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu kiri!'), (15, 50), font, 0.7, (54, 67, 244), 2)
            setY += 2
            kit.servo[1].angle = setY
       
        elif cX > scanArea[2]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu kanan!'), (15, 75), font, 0.7, (54, 67, 244), 2)
            setY -= 2
            kit.servo[1].angle = setY
            
        if cY > scanArea[3]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu bawah!'), (15, 50), font, 0.7, (54, 67, 244), 2)
            setX += 2
            kit.servo[0].angle = setX
            
        elif cY < scanArea[1]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu atas!'), (15, 75), font, 0.7, (54, 67, 244), 2)
            setX -= 2
            kit.servo[0].angle = setX
        
        if confidence >= 80 and confidence <= 100:
            nameID = names[Id]
            confidenceTxt = " {0}%".format(round(confidence))
            
        else:
            nameID = names[0]
            confidenceTxt = " {0}%".format(round(100-confidence))

        if jumlahWajah > 1:
            imgRGB = cv2.putText(imgRGB, str('Wajah lebih dari satu!'), (15, 50), font, 0.7, (54, 67, 244), 2)

        if w1 <= size[0] :
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu jauh!'), (15, 25), font, 0.7, (41, 50, 183), 2)
        
        elif w1 >= size[1]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu dekat!'), (15, 25), font, 0.7, (41, 50, 183), 2)

        else:
            imgRGB = cv2.putText(imgRGB, str(nameID), (x2, y2-5), font, 0.7, (145, 202, 19), 2)
            imgRGB = cv2.putText(imgRGB, str(confidenceTxt), (x2+w2-60, y2+h2-5), font, 0.7, (145, 202, 19), 2)
            
            if count2 < faceCompare:
                detectResult[count2] = names.index(nameID)
                count2 += 1

    cv2.imshow('Face Recognition', imgRGB)
    DetectedFace_Now = jumlahWajah

    if count2 == faceCompare:
        for i in range(totalUser):
            countID[i] = detectResult.count(i)

        faceResult_Now = names[countID.index(max(countID))]

        if faceResult_Last != faceResult_Now or faceState2 == False:
            faceResult_Last = faceResult_Now
            print("Compare Wajah  :", detectResult)
            print("User terdeteksi:", faceResult_Now)
        if DetectedFace_Last == 0 and DetectedFace_Now == 1:
            DetectedFace_Last = DetectedFace_Now
            DetectedTime_Now = getCurrent("second") 
            TimeBetween = Selisih(DetectedTime_Now, notDetectedTime_Now)

            if TimeBetween > DetectedFace_Tolerance or count1 == 0:
                count1 += 1
                faceState1 = True
                faceState2 = True
                print("Deteksi ke     :", count1)
                print("Hari, Tanggal  :", getCurrent("DATE"))
                print("Jam            :", getCurrent("Time"))
                print("")
                sistemPintu("Buka")
                while waktuPintuTerbuka < 10:
                    if GPIO.input(pin_sensorPIR) == 1:
                        print("Anda sudah masuk") 
                        break

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
                
                sistemPintu("Tutup")
                if chat_id == 0:
                    chat_id = 1338050139

                if faceResult_Now == names[0]:
                    txt = 'Wajah tidak dikenali!'
                    bot.sendMessage(chat_id, str(txt))

                else:
                    txt = 'User ' + faceResult_Now + ' masuk'
                    bot.sendMessage(chat_id, str(txt))

                saveImage(imgRGB)
                sendImage(chat_id)

        elif DetectedFace_Last == 1 and DetectedFace_Now == 0:
            DetectedFace_Last = DetectedFace_Now
            notDetectedTime_Now = getCurrent("second")

        elif DetectedFace_Last == 0 and DetectedFace_Now == 0:

            if faceState1 == True:
                faceState1 = False
                notDetectedTime_Now = getCurrent("second")

            if count1 != 0 and faceState2 == True:
                notDetectedTime_Last = getCurrent("second")
                TimeBetween = Selisih(notDetectedTime_Last, notDetectedTime_Now)

            if TimeBetween > DetectedFace_Tolerance and faceState2 == True:
                count2 = 0
                faceState2 = False
                print("Tidak Ada Wajah!")
                txt = 'Tidak ada wajah  terdeteksi dalam 5 detik terakhir'
                bot.sendMessage(chat_id, str(txt))

def motorStart(mode):
    if mode == "FORWARD":
        print("Mode: Forward\n")
        GPIO.output(pin_motorLogic1, 1)
        GPIO.output(pin_motorLogic2, 0)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    elif mode == "REVERSE":
        print("Mode: Reverse\n")
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    elif mode == "CLOSE":
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, 0, 0, 0)

    else:
        print("Parameter 'mode' harus FORWARD atau REVERSE!\n")

def motorStop(forceBreak = 0):
    if forceBreak == 0:
        print("Motor Stop\n")
        motorSpeed(motorMIN, motorZERO, -200, 1)
    elif forceBreak == 1:
        GPIO.output(pin_motorLogic1, 0)
        GPIO.output(pin_motorLogic2, 0)
    
def motorSpeed(begin, end, step, accel):    
    if accel == 0:
        pca.channels[motorPWM_Channel].duty_cycle = motorMIN
        time.sleep(0.02)   
    elif accel == 1:
        for i in range(begin, end, step):
            pca.channels[motorPWM_Channel].duty_cycle = i
            if GPIO.input(pin_pintuBuka) or GPIO.input(pin_pintuTutup) == 1:
                break
            time.sleep(0.02)

def setupPIR():
    print("Menyiapkan Sensor PIR...") 
    time.sleep(0.5)

    while GPIO.input(pin_sensorPIR) == 1:
        print("Sensor PIR belum siap")
        print("Mohon untuk tidak ada pergerakan terlebih dahulu!\n")
        time.sleep(0.5)

    print("Sensor PIR Siap!\n")
    time.sleep(0.5)

def setupPintu():
    print("Memastikan Pintu Tertutup")
    if GPIO.input(pin_pintuTutup) == 0:
        print("Pintu sedang terbuka! Pintu akan ditutup...")
        GPIO.output(pin_solenoid, 1)
        while GPIO.input(pin_pintuTutup) == 0:
            motorStart("CLOSE") 
                  
    motorStop(1)
    print("Pintu sudah tertutup!\n")
    GPIO.output(pin_solenoid, 0)

def sistemPintu(kondisi):
    if kondisi == "Buka":
        print("Pintu dibuka")
        LedIndicator(0, 1, 0) 
        GPIO.output(pin_solenoid, 1)

        while GPIO.input(pin_pintuBuka) == 0:
            motorStart("FORWARD")
        
        print("Pintu terbuka")
        LedIndicator(0, 0, 1) 

    elif kondisi == "Tutup":
        print("Pintu ditutup")
        LedIndicator(0, 1, 0) 

        while GPIO.input(pin_pintuTutup) == 0:
            motorStart("REVERSE")
 
        GPIO.output(pin_solenoid, 0)
        print("Pintu tertutup")
        LedIndicator(1, 0, 0) 
        
    motorStop(1) 

def LedIndicator(merah, kuning, hijau):
    global pin_LedMerah
    global pin_LedKuning
    global pin_LedHijau
    
    GPIO.output(pin_LedMerah, merah)
    GPIO.output(pin_LedKuning, kuning)
    GPIO.output(pin_LedHijau, hijau)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print('Telegram Bot Listening...\n')

try:
    LedIndicator(0, 1, 0)
    setupPIR()
    setupPintu()
    LedIndicator(1, 0, 0)

    while True:
        detectFace()

        if cv2.waitKey(1) & 0xFF == ord('q') or Quit == True:
            break

    cam.release()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    print("Program Stop")

# except:
#     print("Other Error or exception occured!")
    
finally:
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    GPIO.cleanup()
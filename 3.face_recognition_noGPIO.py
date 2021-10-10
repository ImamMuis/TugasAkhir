import os
import cv2
# import time
# import busio
import telepot
import datetime
# import RPi.GPIO as GPIO
# from board import SCL, SDA
# from adafruit_pca9685 import PCA9685
# from adafruit_servokit import ServoKit

telebotAdminID = 1338050139

pin_solenoid    = 14
pin_pintuBuka   = 22
pin_pintuTutup  = 27
pin_sensorPIR   = 17
pin_motorLogic1 = 15
pin_motorLogic2 = 18

faceCompare = 20
DetectedFace_Tolerance = 3
waktuPintuTerbuka = 5 #detik
motorMAX = 2 ** 16 - 1 #65535 (24V)
motorMIN = 13653 # 13653/65535*24= 5V

userDir = 'img_record'
teleBot_PWD = '201802014'
fileUser = 'data/Username.txt'
tokenBot = '2026242681:AAH4o92PExV2rl8Bj0WhU8U5QamfvSnEVQw'

# cam = cv2.VideoCapture(0) # Raspi
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Windows
resolution = 480

ratio = 4 / 3
rgbHeight = resolution
rgbWidth = int(round(rgbHeight * ratio, 0))
cam.set(3, rgbWidth)
cam.set(4, rgbHeight)

servoX_Degree = 90
servoY_Degree = 90
facePosition = [250, 390, 170, 310]

# i2c_bus = busio.I2C(SCL, SDA)
# pca = PCA9685(i2c_bus)
# pca.frequency = 50

# kit = ServoKit(channels=16)
# kit.servo[0].angle = servoX_Degree
# kit.servo[1].angle = servoY_Degree
# kit.servo[0].set_pulse_width_range(500, 2750)
# kit.servo[1].set_pulse_width_range(500, 2750)

with open(fileUser) as user:
    names = user.read().splitlines()

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'data/haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read('data/trainer.xml')

Id = 0
imgRGB = 0
count1 = 0
count2 = 0
chat_id = 0
Quit = False
motorZERO = 0
QuitFlag = False
faceState1 = False
faceState2 = False
TimeBetween = 0.0
motorPWM_Channel = 3
countPintuTerbuka = 0
DetectedFace_Last =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0
command = ''
faceResult_Now = ''
faceResult_Last = ''
totalUser = len(names)
countID = [0] * totalUser
detectResult = [0] * faceCompare

day = {
    'Sun' : 'Minggu',
    'Mon' : 'Senin',
    'Tue' : 'Selasa',
    'Wed' : 'Rabu',
    'Thu' : 'Kamis',
    'Fri' : 'Jumat',
    'Sat' : 'Sabtu',
}

month = {
    'Jan' : 'Januari',
    'Feb' : 'Februari',
    'Mar' : 'Maret',
    'Apr' : 'April',
    'Mei' : 'Mei',
    'Jun' : 'Juni',
    'Jul' : 'Juli',
    'Agt' : 'Agustus',
    'Sep' : 'September',
    'Oct' : 'Oktober',
    'Nov' : 'Nopember',
    'Dec' : 'Desember'
}

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin_sensorPIR, GPIO.IN)
# GPIO.setup(pin_pintuBuka, GPIO.IN)
# GPIO.setup(pin_pintuTutup, GPIO.IN)
# GPIO.setup(pin_solenoid, GPIO.OUT)
# GPIO.setup(pin_motorLogic1, GPIO.OUT)
# GPIO.setup(pin_motorLogic2, GPIO.OUT)

# GPIO.output(pin_solenoid, 0)
# GPIO.output(pin_motorLogic1, 0)
# GPIO.output(pin_motorLogic2, 0)
# time.sleep(0.02)

def Selisih(current, prev):
    num = float(current) - float(prev)
    if num < 0:
        num += 60

    num = round(num, 3)
    return num

def getCurrent(data):
    global day
    global month
    now = datetime.datetime.now()
    
    if data == 'DATE':
        dayNow   = day[now.strftime('%a')]
        monthNow = month[now.strftime('%b')]
        date  = now.strftime('%d')
        year  = now.strftime('%Y')
        value = f'{dayNow}, {date} {monthNow} {year}'

    elif data == 'Date':
        value = now.strftime('%Y-%m-%d.%H.%M.%S')

    elif data == 'TIME':
        value = now.strftime('%H:%M:%S')

    elif data == 'Time':
        Time = now.strftime('%H:%M:%S.')
        sec = str(round(float(str(now).split(':')[-1]), 3))
        value = Time + sec.split('.')[-1]

    elif data == 'second':
        value = str(round(float(str(now).split(':')[-1]), 3))

    else:
        print('Parameter Salah!')

    return value

def saveImage(img):
    date = getCurrent('DATE')
    time = getCurrent('Time')
    waktu = getCurrent('Date')
    img = cv2.putText(img, time, (15, 447), font, 0.5, (54, 67, 244), 2)
    img = cv2.putText(img, date, (15, 462), font, 0.5, (54, 67, 244), 2)
    namaFile = 'Snapshot.' + waktu + '.jpg'
    cv2.imwrite(userDir + '/' + namaFile, img)

def sendImage(chatId):
    file = os.listdir(userDir)
    lastImage = sorted(file, key = lambda x: os.path.splitext(x)[0])
    foto = lastImage[-1]
    file = userDir + '/' + foto
    bot.sendPhoto(chatId, photo=open(file, 'rb'))

def motorSpeed(begin, end, step, accel):    
    if accel == 0:
        # pca.channels[motorPWM_Channel].duty_cycle = motorMIN
        pass

    elif accel == 1:
        for i in range(begin, end, step):
            pass
            # pca.channels[motorPWM_Channel].duty_cycle = i
            # if GPIO.input(pin_pintuBuka) or GPIO.input(pin_pintuTutup) == 1:
            #     break

def motorStart(mode):
    if mode == 'FORWARD':
        print('Mode: Forward')
        # GPIO.output(pin_motorLogic1, 1)
        # GPIO.output(pin_motorLogic2, 0)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    elif mode == 'REVERSE':
        print('Mode: Reverse')
        # GPIO.output(pin_motorLogic1, 0)
        # GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, motorMAX, 200, 1)

    elif mode == 'CLOSE':
        # GPIO.output(pin_motorLogic1, 0)
        # GPIO.output(pin_motorLogic2, 1)
        motorSpeed(motorMIN, 0, 0, 0)

    else:
        print('Parameter "mode" harus FORWARD atau REVERSE!')

def motorStop(forceBreak = 0):
    if forceBreak == 0:
        print('Motor Stop')
        motorSpeed(motorMIN, motorZERO, -200, 1)

    elif forceBreak == 1:
        # GPIO.output(pin_motorLogic1, 0)
        # GPIO.output(pin_motorLogic2, 0)
        pass

def setupPIR():
    print('Menyiapkan Sensor PIR...') 
    # time.sleep(0.02)

    # while GPIO.input(pin_sensorPIR) == 1:
    #     print('Sensor PIR belum siap')
    #     print('Mohon untuk tidak ada pergerakan terlebih dahulu!')
    #     time.sleep(0.5)

    print('Sensor PIR Siap!')
    # time.sleep(0.02)

def setupPintu():
    print('Memastikan Pintu Tertutup')

    # if GPIO.input(pin_pintuTutup) == 0:
    #     print('Pintu sedang terbuka! Pintu akan ditutup...')
    #     GPIO.output(pin_solenoid, 1)
    #     time.sleep(0.5)

    #     while GPIO.input(pin_pintuTutup) == 0:
    #         motorStart('CLOSE') 
                  
    motorStop(1)
    print('Pintu sudah tertutup!')
    # GPIO.output(pin_solenoid, 0)

def sistemPintu(kondisi):
    if kondisi == 'Buka':
        print('Pintu dibuka')
        # GPIO.output(pin_solenoid, 1)

        # while GPIO.input(pin_pintuBuka) == 0:
        #     motorStart('FORWARD')
        
        print('Pintu terbuka')

    elif kondisi == 'Tutup':
        print('Pintu ditutup')

        # while GPIO.input(pin_pintuTutup) == 0:
        #     motorStart('REVERSE')
 
        # GPIO.output(pin_solenoid, 0)
        print('Pintu tertutup')
        
    motorStop(1) 

def servoMove(channel, degree):
    if degree < 0:
        print('Range terlalu kecil!')
        # kit.servo[channel].angle = 0

    elif degree > 180:
        print('Range terlalu besar!')
        # kit.servo[channel].angle = 180
    
    else:
        print(f'Servo {channel} : {degree}°')
        # kit.servo[channel].angle = degree

def teleBot(msg):
    global Quit
    global QuitFlag
    global imgRGB
    global chat_id
    global command
    global teleBot_PWD
    global servoX_Degree
    global servoY_Degree

    chat_id = msg['chat']['id']
    command = msg['text']

    print('From User : ', chat_id)
    print('Command   : ', command)

    show_keyboard = {'keyboard':[	[  'Ambil Foto',     '^',  'Foto Terakhir'], 
                                    [      '<',   'Reset Servo',   '>'     ],
                                    ['Waktu Sekarang',   'v',   'Stop Sistem' ]
                            ]}

    if command == '/start':
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)
        
    elif command == 'Stop Sistem':
        bot.sendMessage(chat_id, 'Masukan PIN untuk stop TeleBot')
        QuitFlag = True

    elif command == teleBot_PWD:
        bot.sendMessage(chat_id, 'Sistem Face Recognition terhenti...')
        Quit = True

    elif command != teleBot_PWD and QuitFlag == True:
        bot.sendMessage(chat_id, 'Password Salah!')
        QuitFlag = False

    elif command == 'Ambil Foto':
        saveImage(imgRGB)
        sendImage(chat_id)

    elif command == 'Foto Terakhir':
        sendImage(chat_id)

    elif command == 'Waktu Sekarang':
        value1 = getCurrent('TIME')
        value2 = getCurrent('DATE')
        txt = f'Time: {value1}\nDate: {value2}'
        bot.sendMessage(chat_id, txt)

    elif command == '^':
        servoY_Degree -= 5
        servoMove(0, servoY_Degree)
        txt = f'Servo Y: {servoY_Degree}°'
        bot.sendMessage(chat_id, txt)

    elif command == 'v':
        servoY_Degree += 5
        servoMove(0, servoY_Degree)
        txt = f'Servo Y: {servoY_Degree}°'
        bot.sendMessage(chat_id, txt)

    elif command == '<':
        servoX_Degree -= 5
        servoMove(1, servoX_Degree)
        txt = f'Servo X: {servoX_Degree}°'
        bot.sendMessage(chat_id, txt)

    elif command == '>':
        servoX_Degree += 5
        servoMove(1, servoX_Degree)
        txt = f'Servo X: {servoX_Degree}°'
        bot.sendMessage(chat_id, txt)
    
    elif command == 'Reset Servo':
        servoX_Degree = 90
        servoY_Degree = 90
        servoMove(1, servoX_Degree)
        servoMove(0, servoY_Degree)
        value1 = f'Servo X: {servoX_Degree}°\n'
        value2 = f'Servo Y: {servoY_Degree}°'
        txt = value1 + value2
        bot.sendMessage(chat_id, txt)

    else:
        bot.sendMessage(chat_id, 'Input belum tersedia!')
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard) 

def detectFace():
    global Id
    global count1
    global count2
    global imgRGB
    global chat_id
    global faceState1
    global faceState2
    global TimeBetween
    global servoY_Degree
    global servoX_Degree
    global faceResult_Now
    global faceResult_Last
    global waktuPintuTerbuka
    global DetectedFace_Last
    global countPintuTerbuka
    global notDetectedTime_Now
    global notDetectedTime_Last
    global DetectedFace_Tolerance

    jumlahWajah = 0
    jarakWajah = [75, 85]
    grayHeight = 165
    grayWidth = int(round(grayHeight * ratio, 0))
    scaling = rgbWidth / grayWidth
    succes, frame = cam.read()

    if succes:
        imgRGB = cv2.flip(frame, 1)
        imgGray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
        imgGray = cv2.resize(imgGray, (grayWidth, grayHeight))
        faces = faceDetector.detectMultiScale(imgGray, 1.2, 3)

        for x1, y1, w1, h1 in faces:
            x2 = int(round(x1 * scaling, 0))
            y2 = int(round(y1 * scaling, 0))
            w2 = int(round(w1 * scaling, 0))
            h2 = int(round(h1 * scaling, 0))
            cX = int(round(x2+w2/2, 0))
            cY = int(round(y2+h2/2, 0))

            imgRGB = cv2.rectangle(imgRGB, (x2, y2), (x2+w2, y2+h2), (186, 39, 59), 2)
            jumlahWajah = int(str(faces.shape[0]))
            Id, confidence = faceRecognizer.predict(imgGray[y1:y1+h1, x1:x1+w1])
            
            if jumlahWajah == 0:
                imgRGB = cv2.putText(imgRGB, 'Tidak ada Wajah', (15, 50), font, 0.7, (54, 67, 244), 2)

            elif jumlahWajah > 1:
                imgRGB = cv2.putText(imgRGB, 'Wajah lebih dari satu!', (15, 50), font, 0.7, (54, 67, 244), 2)
            
            elif jumlahWajah == 1:
                if w1 <= jarakWajah[0] :
                    imgRGB = cv2.putText(imgRGB, 'Wajah terlalu jauh!', (15, 25), font, 0.7, (41, 50, 183), 2)
                
                elif w1 >= jarakWajah[1]:
                    imgRGB = cv2.putText(imgRGB, 'Wajah terlalu dekat!', (15, 25), font, 0.7, (41, 50, 183), 2)

                if cX < facePosition[0]:
                    imgRGB = cv2.putText(imgRGB, 'Wajah terlalu kiri!', (15, 50), font, 0.7, (54, 67, 244), 2)
                    servoX_Degree += 1
                    servoMove(1, servoX_Degree)
            
                elif cX > facePosition[1]:
                    imgRGB = cv2.putText(imgRGB, 'Wajah terlalu kanan!', (15, 75), font, 0.7, (54, 67, 244), 2)
                    servoX_Degree -= 1
                    servoMove(1, servoX_Degree)
                    
                if cY < facePosition[2]:
                    imgRGB = cv2.putText(imgRGB, 'Wajah terlalu atas!', (15, 50), font, 0.7, (54, 67, 244), 2)
                    servoY_Degree -= 1
                    servoMove(0, servoY_Degree)
                    
                elif cY > facePosition[3]:
                    imgRGB = cv2.putText(imgRGB, 'Wajah terlalu bawah!', (15, 75), font, 0.7, (54, 67, 244), 2)
                    servoY_Degree += 1
                    servoMove(0, servoY_Degree)
                
                if confidence >= 80 and confidence <= 100:
                    nameID = names[Id]
                    confidenceTxt = ' {0}%'.format(round(confidence))
                    
                else:
                    nameID = names[0]
                    confidenceTxt = ' {0}%'.format(round(100-confidence))

                imgRGB = cv2.putText(imgRGB, nameID, (x2, y2-5), font, 0.7, (145, 202, 19), 2)
                imgRGB = cv2.putText(imgRGB, confidenceTxt, (x2+w2-60, y2+h2-5), font, 0.7, (145, 202, 19), 2)
                
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
                print('Compare Wajah  :', detectResult)
                print('User terdeteksi:', faceResult_Now)

            if DetectedFace_Last == 0 and DetectedFace_Now == 1:
                DetectedFace_Last = DetectedFace_Now
                DetectedTime_Now = getCurrent('second') 
                TimeBetween = Selisih(DetectedTime_Now, notDetectedTime_Now)

                if TimeBetween > DetectedFace_Tolerance or count1 == 0:
                    if chat_id == 0:
                        chat_id = telebotAdminID

                    count1 += 1
                    faceState1 = True
                    faceState2 = True

                    print('Deteksi ke     :', count1)
                    print('Hari, Tanggal  :', getCurrent('DATE'))
                    print('Jam            :', getCurrent('TIME'))
                    print('')

                    if faceResult_Now == names[0]:
                        saveImage(imgRGB)
                        sendImage(chat_id)

                        txt = 'Wajah tidak dikenali!\n'
                        Date = str('Tanggal : ' + getCurrent('DATE') + '\n')
                        Time = str('Jam : '     + getCurrent('Time') + '\n')
                        txt = txt + Date + Time
                        bot.sendMessage(chat_id, txt)

                    else:
                        sistemPintu('Buka')
                        saveImage(imgRGB)
                        sendImage(chat_id)

                        txt = 'User ' + faceResult_Now + ' masuk\n'
                        Date = str('Tanggal : ' + getCurrent('DATE') + '\n')
                        Time = str('Jam : '     + getCurrent('Time') + '\n')
                        txt = txt + Date + Time
                        bot.sendMessage(chat_id, txt)

                        # while countPintuTerbuka < waktuPintuTerbuka:
                        #     if GPIO.input(pin_sensorPIR) == 1:
                        #         print('Anda sudah masuk') 
                        #         break

                        #     if countPintuTerbuka < 3:
                        #         print('Pintu sudah terbuka, silakan masuk')

                        #     else:
                        #         timerPintu = waktuPintuTerbuka - countPintuTerbuka
                        #         print('Mohon segera masuk')
                        #         print('Pintu akan ditutup dalam waktu ', timerPintu, 'detik')

                        #     countPintuTerbuka += 1   
                        #     time.sleep(1)
                            
                        if countPintuTerbuka == waktuPintuTerbuka:
                            print('Anda tidak segera masuk')

                        countPintuTerbuka = 0
                        sistemPintu('Tutup')

            elif DetectedFace_Last == 1 and DetectedFace_Now == 0:
                DetectedFace_Last = DetectedFace_Now
                notDetectedTime_Now = getCurrent('second')

            elif DetectedFace_Last == 0 and DetectedFace_Now == 0:
                if faceState1 == True:
                    faceState1 = False
                    notDetectedTime_Now = getCurrent('second')

                if count1 != 0 and faceState2 == True:
                    notDetectedTime_Last = getCurrent('second')
                    TimeBetween = Selisih(notDetectedTime_Last, notDetectedTime_Now)

                if TimeBetween > DetectedFace_Tolerance and faceState2 == True:
                    count2 = 0
                    faceState2 = False
                    print('Tidak Ada Wajah!')
                    txt = 'Tidak ada wajah  terdeteksi dalam 5 detik terakhir'
                    bot.sendMessage(chat_id, txt)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print('Telegram Bot Listening...\n')

try:
    setupPIR()
    setupPintu()

    while True:
        detectFace()

        if cv2.waitKey(1) & 0xFF == ord('q') or Quit == True:
            break

except KeyboardInterrupt:
    print('Program Stop')
    
finally:
    cam.release()
    cv2.destroyAllWindows()
    setupPintu()
    motorStop(1) 
    servoMove(0, 90)
    servoMove(0, 90)
    # GPIO.cleanup()
import os
import cv2
import time
# import busio
import telepot
import datetime
import openpyxl 

pin_solenoid    = 14
pin_pintuBuka   = 22
pin_pintuTutup  = 27
pin_sensorPIR   = 17
pin_motorLogic1 = 15
pin_motorLogic2 = 18

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Raspi
resolution = 480
faceCompare = 20
motorMIN = 13653
motorMAX = 2 ** 16 - 1

fps = 25
recordTime = 7.2
servoX_Degree = 90
servoY_Degree = 90
motorPWM_Channel = 3
waktuPintuTerbuka = 5
DetectedFace_Tolerance = 3
telebotAdminID  = 1338050139
facePosition = [250, 390, 170, 310]

userDir = 'img_record'
teleBot_PWD = 'Mkt2k21'
fileUser = 'data/Username.txt'
dataMasuk = 'data/userMasuk.xlsx'
tokenBot = '2077135119:AAF3srU5w3127y0CNkDUJeMGJu2-3aTVQYI'

ratio = 4 / 3
rgbHeight = resolution
rgbWidth = int(round(rgbHeight * ratio, 0))
cam.set(3, rgbWidth)
cam.set(4, rgbHeight)

# i2c_bus = busio.I2C(SCL, SDA)
# pca = PCA9685(i2c_bus)
# pca.frequency = 50

# kit = ServoKit(channels=16)
# kit.servo[0].set_pulse_width_range(500, 2750)
# kit.servo[1].set_pulse_width_range(500, 2750)

with open(fileUser) as user:
    names = user.read().splitlines()

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'data/haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read('data/trainer.xml')

Quit = False
QuitFlag = False
faceState = False
recordFlag = False

imgRGB = 0
chat_id = 0
timeNow = 0
command = ''
videoOut = ''
videoStep = 0
motorZERO = 0
frameRecord = 0
countFaceCompare = 0
DetectedFace_Last =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0
totalUser = len(names)
countID = [0] * totalUser
frameTotal = recordTime * fps
detectResult = [0] * faceCompare
recordTime = (recordTime * fps / 10) + 1

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

    elif data == 'Time':
        Time  = now.strftime('%H:%M:%S.')
        sec   = str(round(float(str(now).split(':')[-1]), 3))
        value = Time + sec.split('.')[-1]

    elif data == 'second':
        value = str(round(float(str(now).split(':')[-1]), 3))

    else:
        print('Parameter Salah!')

    return value

def saveImage(img, date, time):
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
    fileType = file.split('.')[-1]

    if fileType == 'jpg':
        bot.sendPhoto(chatId, photo=open(file, 'rb'))

    elif fileType == 'mp4':
        bot.sendVideo(chatId, video=open(file, 'rb'), 
                      caption='Monitoring Lingkungan')

def recordVideo(img):
    global chat_id
    global command
    global timeNow
    global videoOut
    global videoStep
    global recordFlag
    global frameRecord
    global servoX_Degree

    if videoStep == 0:
        videoStep += 1
        print('Create video')
        timeNow = time.time()
        Date = getCurrent('Date')
        servoX_Degree = 45
        servoMove(1, servoX_Degree)
        videoName = f'{userDir}/Snapshot.{Date}.mp4'
        videoEncode = cv2.VideoWriter_fourcc(*'mp4v')
        videoOut = cv2.VideoWriter(videoName, videoEncode, fps, (640, 480))

    elif videoStep == 1:
        frameRecord += 1

        if frameRecord <= 90:
            servoX_Degree += 1
            servoMove(1, servoX_Degree)

        elif frameRecord > 90:
            servoX_Degree -= 1
            servoMove(1, servoX_Degree)

        if time.time() - timeNow < recordTime:
            Date = getCurrent('DATE')
            Time = getCurrent('Time')
            img = cv2.putText(img, Time, (15, 447), font, 0.5, (54, 67, 244), 2)
            img = cv2.putText(img, Date, (15, 462), font, 0.5, (54, 67, 244), 2)
            videoOut.write(img)

            if frameRecord == frameTotal:
                videoStep += 1
                print('Record done')
                bot.sendMessage(chat_id, 'Perekaman selesai, video sedang dikirim...')

    elif videoStep == 2:
        videoOut.release()
        print('Video saved')
        sendImage(chat_id)
        servoX_Degree = 90
        servoMove(1, servoX_Degree)
        timeNow = 0
        command = ''
        videoStep = 0
        frameRecord = 0
        recordFlag = False

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
    global imgRGB
    global chat_id
    global command
    global QuitFlag
    global recordFlag
    global teleBot_PWD
    global servoX_Degree
    global servoY_Degree

    chat_id = msg['chat']['id']
    command = msg['text']
    print('From User : ', chat_id)
    print('Command   : ', command)

    disableCommnad = ['^', 'v', '<', '>', 'Reset Servo', 
                      'Stop Sistem', 'Rekam Video']

    show_keyboard = {'keyboard':[   ['Ambil Foto', '^', 'Rekam Video'], 
                                    ['<', 'Reset Servo', '>'],
                                    ['History User Masuk', 'v', 'Stop Sistem']
                            ]}

    if command == '/start':
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)
        
    elif command in disableCommnad and recordFlag == True:
        bot.sendMessage(chat_id, 'Video sedang direkam!')

    elif command == 'Stop Sistem':
        QuitFlag = True
        bot.sendMessage(chat_id, 'Masukan PIN untuk stop TeleBot')

    elif command == teleBot_PWD:
        Quit = True
        bot.sendMessage(chat_id, 'Sistem Face Recognition terhenti...')

    elif command != teleBot_PWD and QuitFlag == True:
        QuitFlag = False
        bot.sendMessage(chat_id, 'Password Salah!')

    elif command == 'Ambil Foto':
        Date = getCurrent('DATE')
        Time = getCurrent('Time')
        saveImage(imgRGB, Date, Time)
        sendImage(chat_id)

    elif command == 'Rekam Video':
        recordFlag = True
        bot.sendMessage(chat_id, 'Monitoring Lingkungan')

    elif command == 'History User Masuk':
        bot.sendDocument(chat_id, document=open(dataMasuk, 'rb'))

    elif command == '^':
        servoY_Degree -= 5
        servoMove(0, servoY_Degree)
        telebotText = f'Servo Y: {servoY_Degree}°'
        bot.sendMessage(chat_id, telebotText)

    elif command == 'v':
        servoY_Degree += 5
        servoMove(0, servoY_Degree)
        telebotText = f'Servo Y: {servoY_Degree}°'
        bot.sendMessage(chat_id, telebotText)

    elif command == '<':
        servoX_Degree -= 5
        servoMove(1, servoX_Degree)
        telebotText = f'Servo X: {servoX_Degree}°'
        bot.sendMessage(chat_id, telebotText)

    elif command == '>':
        servoX_Degree += 5
        servoMove(1, servoX_Degree)
        telebotText = f'Servo X: {servoX_Degree}°'
        bot.sendMessage(chat_id, telebotText)
    
    elif command == 'Reset Servo':
        servoX_Degree = 90
        servoY_Degree = 90
        servoMove(1, servoX_Degree)
        servoMove(0, servoY_Degree)
        value1 = f'Servo X: {servoX_Degree}°\n'
        value2 = f'Servo Y: {servoY_Degree}°'
        telebotText = value1 + value2
        bot.sendMessage(chat_id, telebotText)

    elif command == 'My id':
        bot.sendMessage(chat_id, str(chat_id))

    else:
        bot.sendMessage(chat_id, 'Input belum tersedia!')
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard) 

def detectFace():
    global imgRGB
    global command
    global recordFlag

    succes, frame = cam.read()

    if succes:
        imgRGB = cv2.flip(frame, 1)
        cv2.imshow('Save Video', imgRGB)

        if recordFlag == True:
            recordVideo(imgRGB)
            
bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
telebotText  = 'Sistem Face Recognition Berjalan\n'
print(telebotText)

while(True):
    detectFace()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
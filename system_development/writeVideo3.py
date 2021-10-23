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

telebotAdminID  = 1338050139

faceCompare = 20
DetectedFace_Tolerance = 3
waktuPintuTerbuka = 5 #detik
motorMAX = 2 ** 16 - 1 #65535 (24V)
motorMIN = 13653 # 13653/65535*24= 5V

userDir = 'img_record'
teleBot_PWD = 'Mkt2k21'
fileUser = 'data/Username.txt'
dataMasuk = 'data/userMasuk.xlsx'
tokenBot = '2077135119:AAF3srU5w3127y0CNkDUJeMGJu2-3aTVQYI'

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Raspi
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
# kit.servo[0].set_pulse_width_range(500, 2750)
# kit.servo[1].set_pulse_width_range(500, 2750)

with open(fileUser) as user:
    names = user.read().splitlines()

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'data/haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read('data/trainer.xml')

imgRGB = 0
chat_id = 0
Quit = False
holdsec = 3
motorZERO = 0
QuitFlag = False
faceState = False
countFaceCompare = 0
motorPWM_Channel = 3
DetectedFace_Last =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0

command = ''
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

def createVideo():
    timeNow = time.time()
    Date = getCurrent('Date')
    videoName = f'{userDir}/Snapshot.{Date}.mp4'
    videoEncode = cv2.VideoWriter_fourcc(*'mp4v')
    videoOut = cv2.VideoWriter(videoName, videoEncode, 25.0, (640, 480))

    return timeNow, videoOut

def recordVideo(img):
    timeNow, videoOut = createVideo()
    while time.time() - timeNow < 15:
        # dateImg = getCurrent('DATE')
        # timeImg = getCurrent('Time')
        imgRecord = img
        # imgRecord = cv2.putText(imgRecord, timeImg, (15, 447), font, 0.5, (54, 67, 244), 2)
        # imgRecord = cv2.putText(imgRecord, dateImg, (15, 462), font, 0.5, (54, 67, 244), 2)
        videoOut.write(imgRecord)

    imgRecord = 0
    videoOut.release()
    bot.sendMessage(chat_id, 'Video Done!')

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
    bot.sendPhoto(chatId, photo=open(file, 'rb'))

def teleBot(msg):
    global Quit
    global imgRGB
    global chat_id
    global command
    global QuitFlag
    global teleBot_PWD
    global servoX_Degree
    global servoY_Degree

    chat_id = msg['chat']['id']
    command = msg['text']

    print('From User : ', chat_id)
    print('Command   : ', command)

    show_keyboard = {'keyboard':[   ['Ambil Foto', '^', 'Foto Terakhir'], 
                                    ['<', 'Reset Servo', '>'],
                                    ['History User Masuk', 'v', 'Stop Sistem']
                            ]}

    if command == '/start':
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)
        
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
        saveImage(imgRGB)
        sendImage(chat_id)

    elif command == 'Foto Terakhir':
        createVideo()

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

    succes, frame = cam.read()

    if succes:
        imgRGB = cv2.flip(frame, 1)
        cv2.imshow('Save Video', imgRGB)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
telebotText  = 'Sistem Face Recognition Berjalan\n'
print(telebotText)

while True:
    detectFace()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
import cv2
import telepot
import datetime

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
videoCodec = cv2.VideoWriter_fourcc(*'avc1')

frame = 0
duration = 5
videoOut = 0
Quit = False

userDir = 'img_record'
teleBot_PWD = '201802014'
tokenBot = '2026242681:AAH4o92PExV2rl8Bj0WhU8U5QamfvSnEVQw'

def Selisih(current, prev):
    num = float(current) - float(prev)
    if num < 0:
        num += 60
    num = round(num, 3)

    return num

def getCurrent(data):
    now = datetime.datetime.now()
    if data == "Date":
        value = now.strftime("%Y%m%d%H%M%S")

    elif data == "second":
        value = str(round(float(str(now).split(":")[-1]), 3))

    else:
        print("WRONG PARAMETER!")

    return value

def teleBot(msg):
    global Quit
    global frame
    QuitFlag = False

    chat_id = msg['chat']['id']
    command = msg['text']
    
    print("From User : %s" %chat_id)
    print("Command   : %s\n" %command)

    show_keyboard = {'keyboard':[	['Ambil Foto','Foto Terakhir'], 
                                    ['Rekam Video','Stop Sistem ']
                            ]}

    if command == '/start':
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)

    elif command == 'Ambil Foto':
        bot.sendMessage(chat_id, str('Kirim Foto'))

    elif command == 'Foto Terakhir':
        bot.sendMessage(chat_id, str('Foto Terakhir'))

    elif command == 'Rekam Video':
        timeStart = getCurrent("second")
        timeNow = 0
        TimeBetween = 0
        saveVideo()
        while TimeBetween < duration:
            recordVideo(frame)
            timeNow = getCurrent("second")
            TimeBetween = Selisih(timeNow,timeStart)

    elif command == 'Stop Sistem':
        bot.sendMessage(chat_id, str('Masukan PIN untuk stop sistem'))
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

def Webcam():
    global frame
    succes, frame = cam.read()
    succes += succes
    imgRGB = cv2.flip(frame, 1)
    cv2.imshow('Video Record', imgRGB)

def saveVideo():
    global videoOut
    waktu = getCurrent("Date")
    namaFile = 'Snapshot.' + str(waktu) + '.mp4'
    videoOut = cv2.VideoWriter(userDir + '/' + namaFile, videoCodec, 25.0, (640, 480))

def recordVideo(frame):
    videoOut.write(frame)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print('Telegram Bot Listening...\n')

try:
    while True:
        Webcam()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program Stop")

finally:
    cam.release()
    cv2.destroyAllWindows()
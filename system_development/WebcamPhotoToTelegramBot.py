import os
import cv2
import telepot
import datetime


# ipv4_url = 'http://192.168.43.1:8080'
# cam = f'{ipv4_url}/video'
# cam = cv2.VideoCapture(cam)

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 400)
cam.set(4, 225)

DetectedFace_Tolerance = 5
userDir = 'unknown_faces'

teleBot_PWD = '201802014'
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

frame = 0
count = 0
chat_id = 0
quit = False
quitFlag = False
faceState1 = False
faceState2 = False
TimeBetween = 0
DetectedFace_Last =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0

def Selisih(current, prev):
	num = current - prev
	if num < 0:
		num += 60
	num = round(num, 3)

	return num

def getCurrent(data):
	now = datetime.datetime.now()
	if data == "DATE":
		value = now.strftime("%a, %d - %b - %Y")

	elif data == "Date":
		value = now.strftime("%Y%m%d.%H%M%S")

	elif data == "Time":
		value = now.strftime("%H:%M:%S")

	elif data == "second":
		value = round(float(str(now).split(":")[-1]), 3)

	else:
		print("WRONG PARAMETER!")

	return value

def saveImage(frame):
	waktu = getCurrent("Date")
	namaFile = 'DetectedFace.' + str(waktu) + '.jpg'
	cv2.imwrite(userDir + '/' + namaFile, frame)

def sendImage(chat_id):
	lastImage = os.listdir(userDir)
	foto = lastImage[-1]
	file = str(userDir) + '/' + str(foto)
	bot.sendPhoto(chat_id, photo=open(file, 'rb'))

def teleBot(msg):
	global quit
	global frame
	global chat_id
	global command
	global quitFlag
	global teleBot_PWD

	chat_id = msg['chat']['id']
	command = msg['text']

	print("From User : %s" %chat_id)
	print("Command   : %s\n" %command)

	show_keyboard = {'keyboard':[	['Ambil Foto','Foto Terakhir'], 
									['Waktu Sekarang','Stop Bot ']
							]}
	if command == '/start':
		bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)

	elif command == 'Ambil Foto':
		saveImage(frame)
		sendImage(chat_id)

	elif command == 'Foto Terakhir':
		sendImage(chat_id)

	elif command == 'Waktu Sekarang':
		now = datetime.datetime.now()
		value1 = now.strftime("Time: %H:%M:%S\n")
		value2 = now.strftime("Day : %a, %d - %b - %Y\n")
		bot.sendMessage(chat_id, str(value1)+str(value2))

	elif command == 'Stop Bot':
		bot.sendMessage(chat_id, str('Masukan PIN untuk stop TeleBot'))
		quitFlag = True

	elif command == teleBot_PWD:
		bot.sendMessage(chat_id, str('Bot Telegram terhenti...'))
		quit = True

	elif command != teleBot_PWD and quitFlag == True:
		bot.sendMessage(chat_id, str('Password Salah!'))
		quitFlag = False

	else:
		bot.sendMessage(chat_id, str("Input belum tersedia!"))
		bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard) 

def detectFace():
	global count
	global frame
	global chat_id
	global faceState1
	global faceState2
	global TimeBetween
	global DetectedFace_Last
	global notDetectedTime_Now
	global notDetectedTime_Last
	global DetectedFace_Tolerance

	jumlahWajah = 0

	succes, frame = cam.read()
	frame = cv2.flip(frame, 1)
	frame = cv2.resize(frame, (360, 270))
	abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceDetector.detectMultiScale(abuAbu, 1.3 , 5)

	for x, y, w, h in faces:
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		jumlahWajah = int(str(faces.shape[0]))

	DetectedFace_Now = jumlahWajah

	if DetectedFace_Last == 0 and DetectedFace_Now == 1:
		DetectedFace_Last = DetectedFace_Now
		DetectedTime_Now = getCurrent("second")
		TimeBetween = Selisih(DetectedTime_Now, notDetectedTime_Now)

		# print(TimeBetween)

		if TimeBetween > DetectedFace_Tolerance or count == 0:
			print("Wajah Terdeteksi!\n")
			count += 1
			faceState1 = True
			faceState2 = True
			print("Deteksi ke	 :", count)
			print("Hari, Tanggal :", getCurrent("DATE"))
			print("Jam           :", getCurrent("Time"))
			print("")
			
			if chat_id == 0:
				chat_id = 1338050139

			saveImage(frame)
			sendImage(chat_id)
			bot.sendMessage(chat_id, str("Wajah Terdeteksi!"))

	elif DetectedFace_Last == 1 and DetectedFace_Now == 0:
		DetectedFace_Last = DetectedFace_Now
		notDetectedTime_Now = getCurrent("second")

	elif DetectedFace_Last == 0 and DetectedFace_Now == 0:

		if faceState1 == True:
			notDetectedTime_Now = getCurrent("second")
			faceState1 = False

		if count != 0 and faceState2 == True:
			notDetectedTime_Last = getCurrent("second")
			TimeBetween = Selisih(notDetectedTime_Last, notDetectedTime_Now)

		# print(TimeBetween)

		if TimeBetween > DetectedFace_Tolerance and faceState2 == True:
			print("Tidak Ada Wajah!\n")
			msg = 'Tidak ada wajah  terdeteksi dalam 5 detik terakhir'
			bot.sendMessage(chat_id, str(msg))
			faceState2 = False

	cv2.imshow('Face Detection', frame)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print ('Telegram Bot Listening...\n')

try:
	while True:
		detectFace()

		if cv2.waitKey(1) & 0xFF == ord('q') or quit == True:
			break

	cam.release()
	cv2.destroyAllWindows()

except KeyboardInterrupt:
	sys.exit(0)
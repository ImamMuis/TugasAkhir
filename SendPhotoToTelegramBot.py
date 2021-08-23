import os
import cv2
import telepot
import datetime

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam.set(3, 400)
cam.set(4, 225)
DetectedFace_Tolerance = 5
userDir = 'unknown_faces'

tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

frame = 0
count = 0
chat_id = 0
command = ""
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
	if data == "Date":
		value = now.strftime("%Y%m%d.%H%M%S")

	elif data == "Time":
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
	global frame
	global chat_id
	global command

	chat_id = msg['chat']['id']
	command = msg['text']

	print("User from : %s" %chat_id)
	print("Command   : %s\n" %command)

	show_keyboard = {'keyboard':[	
									['Ambil Foto','Foto Terakhir'], 
									['null','Waktu Sekarang']
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
	abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceDetector.detectMultiScale(abuAbu, 1.3 , 5)

	for x, y, w, h in faces:
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		jumlahWajah = int(str(faces.shape[0]))

	DetectedFace_Now = jumlahWajah

	if DetectedFace_Last == 0 and DetectedFace_Now == 1:
		DetectedFace_Last = DetectedFace_Now
		DetectedTime_Now = getCurrent("Time")
		TimeBetween = Selisih(DetectedTime_Now, notDetectedTime_Now)

		# print(TimeBetween)

		if TimeBetween > DetectedFace_Tolerance or count == 0:
			print("Wajah Terdeteksi!\n")
			count += 1
			faceState1 = True
			faceState2 = True
			print("Counter :", count)
			print("Tanggal :", getCurrent("Date"))
			print("")
			
			if chat_id == 0:
				chat_id = 1338050139

			saveImage(frame)
			sendImage(chat_id)

	elif DetectedFace_Last == 1 and DetectedFace_Now == 0:
		DetectedFace_Last = DetectedFace_Now
		notDetectedTime_Now = getCurrent("Time")

	elif DetectedFace_Last == 0 and DetectedFace_Now == 0:

		if faceState1 == True:
			notDetectedTime_Now = getCurrent("Time")
			faceState1 = False

		if count != 0 and faceState2 == True:
			notDetectedTime_Last = getCurrent("Time")
			TimeBetween = Selisih(notDetectedTime_Last, notDetectedTime_Now)

		# print(TimeBetween)

		if TimeBetween > DetectedFace_Tolerance and faceState2 == True:
			print("Tidak Ada Wajah!\n")
			faceState2 = False

	cv2.imshow('Face Detection', frame)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print ('Telegram Bot Listening...\n')

try:
	while True:
		detectFace()

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cam.release()
	cv2.destroyAllWindows()

except KeyboardInterrupt:
	sys.exit(0)
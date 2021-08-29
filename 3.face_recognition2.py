import os
import cv2
import telepot
import datetime
import numpy as np

names = ['Unknown', 'Imam', 'Iis']

faceCompare = 20
DetectedFace_Tolerance = 5

userDir = 'img_record'
teleBot_PWD = '201802014'
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam.set(3, 480)
cam.set(4, 360)

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
quit = False
quitFlag = False
faceState1 = False
faceState2 = False
TimeBetween = 0
DetectedFace_Last =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0

faceResult_Now = ""
faceResult_Last = ""
totalUser = len(names)
countID = [0] * totalUser
detectResult = [None] * faceCompare

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

def saveImage(imgRGB):
	waktu = getCurrent("Date")
	namaFile = 'Snapshot.' + str(waktu) + '.jpg'
	cv2.imwrite(userDir + '/' + namaFile, imgRGB)

def sendImage(chat_id):
	lastImage = os.listdir(userDir)
	foto = lastImage[-1]
	file = str(userDir) + '/' + str(foto)
	bot.sendPhoto(chat_id, photo=open(file, 'rb'))

def teleBot(msg):
	global quit
	global imgRGB
	global chat_id
	global command
	global quitFlag
	global teleBot_PWD

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
		quitFlag = True

	elif command == teleBot_PWD:
		bot.sendMessage(chat_id, str('Sistem Face Recognition terhenti...'))
		quit = True

	elif command != teleBot_PWD and quitFlag == True:
		bot.sendMessage(chat_id, str('Password Salah!'))
		quitFlag = False

	else:
		bot.sendMessage(chat_id, str("Input belum tersedia!"))
		bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard) 

def detectFace():
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

	size = [75, 85]
	jumlahWajah = 0
	idealSize = False

	succes, frame = cam.read()
	imgRGB = cv2.flip(frame, 1)
	imgGray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
	imgGray = cv2.resize(imgGray, (220, 165))
	faces = faceDetector.detectMultiScale(imgGray, 1.2, 3)

	for x1, y1, w1, h1 in faces:
		x2 = round(x1 * 3, 0)
		y2 = round(y1 * 3, 0)
		w2 = round(w1 * 3, 0)
		h2 = round(h1 * 3, 0)

		imgRGB = cv2.rectangle(imgRGB, (x2, y2), (x2+w2, y2+h2), (186, 39, 59), 2)
		jumlahWajah = int(str(faces.shape[0]))
		Id, confidence = faceRecognizer.predict(imgGray[y1:y1+h1, x1:x1+w1])

		if confidence >= 80 and confidence <= 100:
			nameID = names[Id]
			confidenceTxt = " {0}%".format(round(confidence))
			
		else:
			nameID = names[0]
			confidenceTxt = " {0}%".format(round(100-confidence))

		if jumlahWajah > 1:
			imgRGB = cv2.putText(imgRGB, str('Wajah lebih dari satu!'), (25, 25), font, 0.7, (54, 67, 244), 2)

		if w1 <= size[0] :
			imgRGB = cv2.putText(imgRGB, str('Wajah terlalu jauh!'), (5, 25), font, 0.7, (41, 50, 183), 2)
		
		elif w1 >= size[1]:
			imgRGB = cv2.putText(imgRGB, str('Wajah terlalu dekat!'), (5, 25), font, 0.7, (41, 50, 183), 2)

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
				print("Deteksi ke	  :", count1)
				print("Hari, Tanggal  :", getCurrent("DATE"))
				print("Jam            :", getCurrent("Time"))
				print("")

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
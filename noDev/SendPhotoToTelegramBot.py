import os
import cv2
import telepot
import datetime

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam.set(3, 400)
cam.set(4, 225)
DetectedFace_Tolerance = 5
userDir = 'unknown_faces'

teleBot_PWD = '201802014'
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

quit = False
frame = 0
count = 0
chat_id = 0
command = ''

def getCurrentDate():
	now = datetime.datetime.now()
	value = now.strftime('%Y%m%d.%H%M%S')

	return value

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
	global teleBot_PWD

	chat_id = msg['chat']['id']
	command = msg['text']

	print('User from : %s' %chat_id)
	print('Command   : %s\n' %command)

	show_keyboard = {'keyboard':[	
									['Ambil Foto','Foto Terakhir'], 
									['Stop Bot','Waktu Sekarang']
								]}

	if command == '/start':
		bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)

	elif command == 'Ambil Foto':
		now = datetime.datetime.now()
		waktu = now.strftime('%Y%m%d.%H%M%S')
		namaFile = 'DetectedFace.' + str(waktu) + '.jpg'
		cv2.imwrite(userDir + '/' + namaFile, frame)

		sendImage(chat_id)

	elif command == 'Foto Terakhir':
		sendImage(chat_id)

	elif command == 'Stop Bot':
		bot.sendMessage(chat_id, str('Masukan PIN untuk stop Bot'))

	elif command == 'Waktu Sekarang':
		now = datetime.datetime.now()
		value1 = now.strftime('Time: %H:%M:%S\n')
		value2 = now.strftime('Day : %a, %d - %b - %Y\n')
		bot.sendMessage(chat_id, str(value1)+str(value2))
	
	elif command == '201802014':
		bot.sendMessage(chat_id, str('Bot Telegram terhenti...'))
		quit = True

	else:
		bot.sendMessage(chat_id, str('Input belum tersedia!'))
		bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)

def vidShow():
	global frame

	succes, frame = cam.read()
	frame = cv2.flip(frame, 1)
	cv2.imshow('Face Detection', frame)

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print ('Telegram Bot Listening...\n')

try:
	while True:
		vidShow()

		if cv2.waitKey(1) and 0xFF == ord('q') or quit == True:
			break

	cam.release()
	cv2.destroyAllWindows()

except KeyboardInterrupt:
	sys.exit(0)
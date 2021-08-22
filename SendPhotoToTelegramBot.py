from gpiozero import Buzzer, DigitalInputDevice
import telepot
import picamera

sensor = DigitalInputDevice(17, pull_up=True)
buzzer = Buzzer(26)

def handle(msg):
	global telegramText
	global chat_id
	global receiveTelegramMessage

	chat_id = msg['chat']['id']
	telegramText = msg['text']

	print("Message received from " + str(chat_id))

	if telegramText == "/start":
		bot.sendMessage(chat_id, "Welcome to Idris Bot")

	else:
		buzzer.beep(0.1, 0.1, 1)
		receiveTelegramMessage = True
 
def capture():
	print("Capturing photo…")
	camera = picamera.PiCamera()
	camera.capture('./photo.jpg')
	camera.close()
	print("Sending photo to " + str(chat_id))
	bot.sendPhoto(chat_id, photo = open('./photo.jpg', 'rb'))
 
def sensorTrigger():
	global statusText
	global sendTelegramMessage
	global cameraEnable
	global sendPhoto
	statusText = "Sensor is triggered!"
	sendTelegramMessage = True
	if cameraEnable == True:
		sendPhoto = True
		buzzer.beep(0.1, 0.1, 1)

bot = telepot.Bot('1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo')
bot.message_loop(handle)


statusText = ""
sendPhoto = False
cameraEnable = False
sendTelegramMessage = False
receiveTelegramMessage = False
sensor.when_deactivated = sensorTrigger

print("Telegram bot is ready")
buzzer.beep(0.1, 0.1, 2)

try:
	while True:
		if receiveTelegramMessage == True:
			receiveTelegramMessage = False

			statusText = ""

		if telegramText == "ENABLE":
			cameraEnable = True
			statusText = "Camera is enabled"

		elif telegramText == "PHOTO":
			sendPhoto = True
			statusText = "Capturing photo…"

		else:
			statusText = "Command is not valid"

		sendTelegramMessage = True

		if sendTelegramMessage == True:
			sendTelegramMessage = False
			bot.sendMessage(chat_id, statusText)

		if cameraEnable == True and sendPhoto == True:
			cameraEnable = False
			sendPhoto = False
			capture()
			
except KeyboardInterrupt:
	sys.exit(0)
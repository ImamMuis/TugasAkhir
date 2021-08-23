import time
import datetime
import telepot
# from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Received: %s' %command)

    if command == '/start':
        telegram_bot.sendMessage(chat_id, str("Hi Imam!"))

	# value = waktu.strftime("%Y%m%d.%H%M%S")
    elif command == '/time':
    	now = datetime.datetime.now()
    	value1 = now.strftime("Time: %H:%M:%S\n")
    	value2 = now.strftime("Day : %a, %d - %b - %Y\n")

    	telegram_bot.sendMessage(chat_id, str(value1)+str(value2))

    elif command == '/lastPhoto':
        telegram_bot.sendPhoto(chat_id, photo=open('unknown_faces/DetectedFace.20210823.125956.jpg', 'rb'))

    else:
        telegram_bot.sendMessage(chat_id, str("Input Salah!"))


telegram_bot = telepot.Bot('1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo')
telegram_bot.message_loop(action)
print ('Up and Running....')

while 1:
    time.sleep(10)
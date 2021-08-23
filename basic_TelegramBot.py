import time
import datetime
import telepot
# from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
now = datetime.datetime.now()

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Received: %s' %command)

    if command == '/hi':
        # telegram_bot.sendMessage(chat_id, 'testing custom keyboard', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        #         [InlineKeyboardButton(text="btn1", callback_data='I have Nothing To do'),
        #          InlineKeyboardButton(text="btn2", callback_data='0'),
        #          InlineKeyboardButton(text="btn3", callback_data='0'),
        #          InlineKeyboardButton(text="btn4", callback_data='0')],
        #         [InlineKeyboardButton(text="btn1", callback_data='yep')]
        #     ]
        #     ))
        telegram_bot.sendMessage(chat_id, str("Hi Imam!"))

    elif command == '/time':
        telegram_bot.sendMessage(chat_id,
                                 str("Telegram Bot Running at: \n") +
                                 str(now.strftime("Time: %H:%M \n")) +
                                 str(now.strftime("Day  : %a, %d - %b - %Y \n"))
                                 )

    elif command == '/bagianRaspi':
        telegram_bot.sendPhoto(chat_id, photo=open('KomponenRaspi.png', 'rb'))

    elif command == '/GPIORaspi':
        telegram_bot.sendPhoto(chat_id, photo=open('fotoTele/GPIO_Raspi.png', 'rb'))

    elif command == '/logoRaspi':
        telegram_bot.sendPhoto(chat_id, photo=open('D://1. IMAM/1. Libraries/Pictures/RaspiLogo.png', 'rb'))

    else:
        telegram_bot.sendMessage(chat_id, str("Input Salah!"))


telegram_bot = telepot.Bot('1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo')

telegram_bot.message_loop(action)

print ('Up and Running....')

while 1:
    time.sleep(10)
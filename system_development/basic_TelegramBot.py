import time
import datetime
import telepot

Quit = False
teleBot_PWD = '201802014'
tokenBot = '2026242681:AAH4o92PExV2rl8Bj0WhU8U5QamfvSnEVQw'

def teleBot(msg):
    global Quit
    QuitFlag = False

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
        bot.sendMessage(chat_id, str('Kirim Foto'))

    elif command == 'Foto Terakhir':
        bot.sendMessage(chat_id, str('Foto Terakhir'))

    elif command == 'Waktu Sekarang':
        now = datetime.datetime.now()
        value1 = now.strftime("Time: %H:%M:%S\n")
        value2 = now.strftime("Day : %a, %d - %b - %Y\n")
        bot.sendMessage(chat_id, str(value1)+str(value2))

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

bot = telepot.Bot(tokenBot)
bot.message_loop(teleBot)
print('Telegram Bot Listening...\n')

try:
    while 1:
        time.sleep(1)
        if Quit == True:
            break

except KeyboardInterrupt:
    print("Program Stop")
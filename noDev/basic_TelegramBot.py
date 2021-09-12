import time
import telepot
import datetime

Quit = False
QuitFlag = False

teleBot_PWD = '201802014'
tokenBot = '1461219516:AAHcyhA_4NIdF5uNQrDIkhsQ0nTpaT_rjZo'

def getCurrent(data):
    now = datetime.datetime.now()
    if data == "DATE":
        value = now.strftime("%a, %d - %b - %Y")

    elif data == "Date":
        value = now.strftime("%Y%m%d%H%M%S")

    elif data == "Time":
        value = now.strftime("%H:%M:%S")

    elif data == "second":
        value = str(round(float(str(now).split(":")[-1]), 3))

    else:
        print("WRONG PARAMETER!")

    return value

def teleBot(msg):
    global Quit
    global QuitFlag
    global teleBot_PWD

    chat_id = msg['chat']['id']
    command = msg['text']

    print("From User : %s" %chat_id)
    print("Command   : %s\n" %command)

    show_keyboard = {'keyboard':[	['Ambil Foto','Foto Terakhir'], 
                                    ['Waktu Sekarang','Stop Sistem ']
                            ]}

    if command == 'Stop Sistem':
        bot.sendMessage(chat_id, str('Masukan PIN untuk stop TeleBot'))
        QuitFlag = True

    elif command == teleBot_PWD:
        bot.sendMessage(chat_id, str('Sistem Face Recognition terhenti...'))
        Quit = True

    elif command != teleBot_PWD and QuitFlag == True:
        bot.sendMessage(chat_id, str('Password Salah!'))
        QuitFlag = False
    
    elif command == '/start':
        bot.sendMessage(chat_id, 'Silakan pilih perintah:', reply_markup=show_keyboard)

    elif command == 'Ambil Foto':
        bot.sendMessage(chat_id, str('Hasil tangkapan webcam...'))

    elif command == 'Foto Terakhir':
        bot.sendMessage(chat_id, str('Foto terakhir...'))

    elif command == 'Waktu Sekarang':
        value1 = getCurrent("Time")
        value2 = getCurrent("DATE")
        bot.sendMessage(chat_id, str('Pukul: ' + value1 + '\n')+
                                 str('Tanggal: ' + value2 + '\n'))

    elif command == 'Stop Sistem':
        bot.sendMessage(chat_id, str('Masukan PIN untuk stop TeleBot'))
        QuitFlag = True

    elif command == teleBot_PWD:
        bot.sendMessage(chat_id, str('Sistem Telegram Bot terhenti...'))
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

while True:
    time.sleep(1)
    
    if Quit == True:
        break
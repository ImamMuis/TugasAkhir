
import datetime
def Selisih(current, prev):
    num = float(current) - float(prev)
    if num < 0:
        num += 60

    num = round(num, 3)
    return num

def getCurrent(data):
    global day
    global month
    now = datetime.datetime.now()
    
    if data == 'DATE':
        dayNow   = day[now.strftime('%a')]
        monthNow = month[now.strftime('%b')]
        date  = now.strftime('%d')
        year  = now.strftime('%Y')
        value = f'{dayNow}, {date} {monthNow} {year}'

    elif data == 'Date':
        value = now.strftime('%Y-%m-%d.%H.%M.%S')

    elif data == 'TIME':
        value = now.strftime('%H:%M:%S')

    elif data == 'Time':
        Time = now.strftime('%H:%M:%S.')
        sec = str(round(float(str(now).split(':')[-1]), 3))
        value = Time + sec.split('.')[-1]

    elif data == 'second':
        value = str(round(float(str(now).split(':')[-1]), 3))

    else:
        print('Parameter Salah!')

    return value

def delayTime(holdsec):
	count = 0
	for i in range(2):
		count = i
		if count == 0:
			timeLast = getCurrent('second')
			timeNow = getCurrent('second')
			timeBetween = Selisih(timeNow, timeLast)

		else:
			while timeBetween < holdsec:
				timeNow = getCurrent('second')
				timeBetween = Selisih(timeNow, timeLast)
				print(timeBetween)

delayTime(0.5)
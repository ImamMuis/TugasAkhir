import datetime

day = {
    'Sun' : 'Minggu',
    'Mon' : 'Senin',
    'Tue' : 'Selasa',
    'Wed' : 'Rabu',
    'Thu' : 'Kamis',
    'Fri' : 'Jumat',
    'Sat' : 'Sabtu',
}

month = {
    'Jan' : 'Januari',
    'Feb' : 'Februari',
    'Mar' : 'Maret',
    'Apr' : 'April',
    'Mei' : 'Mei',
    'Jun' : 'Juni',
    'Jul' : 'Juli',
    'Agt' : 'Agustus',
    'Sep' : 'September',
    'Oct' : 'Oktober',
    'Nov' : 'Nopember',
    'Dec' : 'Desember'
}

def getCurrent(data):
    global day
    global month
    now = datetime.datetime.now()

    if data == 'DATE':
        day   = day[now.strftime('%a')]
        month = month[now.strftime('%b')]
        date  = now.strftime('%d')
        year  = now.strftime('%Y')
        value = f'{day}, {date} {month} {year}'

    elif data == 'Date':
        value = now.strftime('%Y%m%d%H%M%S')

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
date = getCurrent('DATE')
print(date)
import openpyxl 
import datetime

dataMasuk = 'data/userMasuk.xlsx'

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
        dayNow   = day[now.strftime('%a')]
        monthNow = month[now.strftime('%b')]
        date  = now.strftime('%d')
        year  = now.strftime('%Y')
        value = f'{dayNow}, {date} {monthNow} {year}'

    elif data == 'Time':
        Time = now.strftime('%H:%M:%S.')
        sec = str(round(float(str(now).split(':')[-1]), 3))
        value = Time + sec.split('.')[-1]

    else:
        print('Parameter Salah!')

    return value

def saveToExcel(user, dates, time):
    wb = openpyxl.load_workbook(dataMasuk) 
    sheet = wb.active 
    maxRow = sheet.max_row
    count1 = maxRow
    day = dates.split(',')[0]
    date = dates.split(',')[1]
    newdata = [[count1, user, day, date, time]]
    
    for row in newdata:
        sheet.append(row)
    
    wb.save(dataMasuk)
    return count1

Date = getCurrent('DATE')
Time = getCurrent('Time')
pendeteksian = saveToExcel('Imam', Date, Time)
print(pendeteksian)
import cv2
import time
import datetime

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

    elif data == 'Time':
        Time  = now.strftime('%H:%M:%S.')
        sec   = str(round(float(str(now).split(':')[-1]), 3))
        value = Time + sec.split('.')[-1]

    elif data == 'second':
        value = str(round(float(str(now).split(':')[-1]), 3))

    else:
        print('Parameter Salah!')

    return value

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Raspi
userDir = 'img_record'
Date = getCurrent('Date')
videoName = f'{userDir}/Snapshot.{Date}.mp4'
videoEncode = cv2.VideoWriter_fourcc(*'mp4v')
videoOut = cv2.VideoWriter(videoName, videoEncode, 20.0, (640, 480))
timeNow = time.time()
count = 0
while(True):
    succes, frame = cam.read()
    if succes:
        imgRGB = cv2.flip(frame, 1)
        cv2.imshow('Save Video', imgRGB)

        if time.time() - timeNow < 5:
            count += 1
            videoOut.write(imgRGB)
            print(count)

        else:
            count = 0
            videoOut.release()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
videoOut.release()
cv2.destroyAllWindows()
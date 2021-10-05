import cv2
import datetime

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
videoCodec = cv2.VideoWriter_fourcc(*'avc1')

videoOut = 0
userDir = 'img_record'

def getCurrent():
    now = datetime.datetime.now()
    value = now.strftime("%Y%m%d%H%M%S")
    return value

def videoRecord():
    global videoOut
    waktu = getCurrent()
    namaFile = 'Snapshot.' + str(waktu) + '.mp4'
    videoOut = cv2.VideoWriter(userDir + '/' + namaFile, videoCodec, 25.0, (640, 480))
    
try:
    videoRecord()
    while True:
        succes, frame = cam.read()
        # videoRecord(frame)
        videoOut.write(frame)
        imgRGB = cv2.flip(frame, 1)
        cv2.imshow('Video Record', imgRGB)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program Stop")

finally:
    cam.release()
    cv2.destroyAllWindows()
import cv2
import datetime
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 400)
cam.set(4, 225)
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

kondisiSebelum  =  0
kondisiSekarang =  0
prevDetectTime  =  0
currentDetectTime =  0
count = 0
selisih = 0

def detectFace():
    jumlahWajah = 0

    succes, frame = cam.read()
    frame = cv2.flip(frame, 1)
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuAbu, 1.3, 4)

    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        jumlahWajah = str(faces.shape[0])

    cv2.imshow('Face Detection', frame)
    return jumlahWajah

def timeNow():
    now = str(datetime.datetime.now())
    now = round(float(now.split(":")[-1]), 3)
    return now
        
def useless():
    if kondisiSebelum == 0 and kondisiSekarang == 1:
        count += 1
        kondisiSebelum = 1
        currentDetectTime = timeNow()
        selisih = currentDetectTime - prevDetectTime
        if selisih > 5:
            print(" Deteksi ke-", count, ": Ada Wajah!")
            prevDetectTime = currentDetectTime
    
    elif kondisiSekarang == 0 and selisih > 5:
        print(" Deteksi ke-", count, ": Tidak ada Wajah!")

    elif kondisiSebelum == 1 and kondisiSekarang == 0:
        count += 1
        kondisiSebelum = 0
        currentDetectTime = timeNow()
        selisih = currentDetectTime - prevDetectTime
        if selisih > 5:
            print(" Deteksi ke-", count, ": Tidak ada Wajah!")
            prevDetectTime = currentDetectTime

limitDetect = 5

while True:
    currentDetectTime = timeNow()
    kondisiSekarang = int(detectFace())
    selisih = abs(round(currentDetectTime - prevDetectTime, 3))
    selisih %= 10

    if kondisiSekarang == 1 and selisih > limitDetect:
        print("Ada Wajah!")
        prevDetectTime = currentDetectTime

    elif kondisiSekarang == 0 and selisih > limitDetect:
        print("Tidak ada Wajah!")
        prevDetectTime = currentDetectTime


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

import cv2
import datetime

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 400)
cam.set(4, 225)

cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

count = 0
selisih = 0
prevDetectFace  =  0
prevDetectTime  =  0
currentDetectFace =  0
currentDetectTime =  0

def detectFace():
    jumlahWajah = 0

    succes, frame = cam.read()
    frame = cv2.flip(frame, 1)
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)

    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        jumlahWajah = str(faces.shape[0])

    cv2.imshow('Face Detection', frame)

    return jumlahWajah

def timeNow():
    # Fungsi untuk mengambil detik terkini
    now = str(datetime.datetime.now())
    now = round(float(now.split(":")[-1]), 3)

    return now

while True:
    currentDetectFace = int(detectFace())
    currentDetectTime = timeNow()
    selisih = abs(round((currentDetectTime - prevDetectTime) % 10, 3))

    if prevDetectFace == 0 and currentDetectFace == 1:
        count += 1
        prevDetectFace = 1
        currentDetectTime = timeNow()
        selisih = abs(round((currentDetectTime - prevDetectTime) % 10, 3))

        if selisih > 5:
            print("Ada Wajah!\n")
            prevDetectTime = currentDetectTime

        print("Counter deteksi ke-", count)
        print("Waktu terdeteksi  :", currentDetectTime)
        print("Akhir terdeteksi  :", prevDetectTime)
        print("Selisih deteksi   :", selisih)
        print("")

    elif prevDetectFace == 1 and currentDetectFace == 0 and selisih > 5:
        count += 1
        prevDetectFace = 0
        currentDetectTime = timeNow()
        prevDetectTime = currentDetectTime
        
        print("Tidak Ada Wajah!\n")
        print("Counter deteksi ke-", count)
        print("Waktu terdeteksi  :", currentDetectTime)
        print("Akhir terdeteksi  :", prevDetectTime)
        print("Selisih deteksi   :", selisih)
        print("")


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
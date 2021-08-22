import cv2
import datetime
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 400)
cam.set(4, 225)
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

count = 0
selisih = 0
kondisiSebelum  =  0
kondisiSekarang =  0

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

while True:
    kondisiSekarang = int(detectFace())

    if kondisiSekarang == 1 and kondisiSebelum == 0:
        print("Ada Wajah!")
        kondisiSebelum = 1

    elif kondisiSekarang == 0 and kondisiSebelum == 1:
        print("Tidak ada Wajah!")
        kondisiSebelum = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
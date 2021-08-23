import cv2
import datetime

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 400)
cam.set(4, 225)
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

count = 0
faceState1 = False
faceState2 = False

DetectedFace_Last  =  0
notDetectedTime_Now = 0
notDetectedTime_Last = 0

DetectedFace_Tolerance = 5
def detectFace():
    jumlahWajah = 0

    succes, frame = cam.read()
    frame = cv2.flip(frame, 1)
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuAbu, 1.3 , 5)

    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        jumlahWajah = str(faces.shape[0])
    cv2.imshow('Face Detection', frame)

    return jumlahWajah

def getCurrent(data):
    now = datetime.datetime.now()
    if data == "Date":
        value = now.strftime("%Y-%m-%d %H:%M:%S")

    elif data == "Time":
        value = round(float(str(now).split(":")[-1]), 3)

    else:
        print("WRONG PARAMETER!")

    return value

def Selisih(current, prev):
    num = current - prev

    num = round( abs(num) % 10, 3)

    return num

while True:
    DetectedFace_Now = int(detectFace())

    if DetectedFace_Last == 0 and DetectedFace_Now == 1:
        DetectedFace_Last = DetectedFace_Now
        DetectedTime_Now = getCurrent("Time")
        TimeBetween = Selisih(DetectedTime_Now, notDetectedTime_Now)
        
        if TimeBetween > DetectedFace_Tolerance or count == 0:
            print("Wajah Terdeteksi!\n")
            count += 1
            faceState1 = True
            faceState2 = True
            print("Counter :", count)
            print("Tanggal :", getCurrent("Date"))
            print("")

    elif DetectedFace_Last == 1 and DetectedFace_Now == 0:
        DetectedFace_Last = DetectedFace_Now
        notDetectedTime_Now = getCurrent("Time")

    elif DetectedFace_Last == 0 and DetectedFace_Now == 0:

        if faceState1 == True:
            notDetectedTime_Now = getCurrent("Time")
            faceState1 = False

        notDetectedTime_Last = getCurrent("Time")
        TimeBetween = Selisih(notDetectedTime_Last, notDetectedTime_Now)

        if TimeBetween > DetectedFace_Tolerance and faceState2 == True:
            print("Tidak Ada Wajah!\n")
            faceState2 = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
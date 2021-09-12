# Import library OpenCV
import os
import cv2
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam.set(3, 640)
cam.set(4, 480)

faceID  = 4
faceSample = 30

userDir = 'dataset'
count1 = 0
count2 = 0
faceIDFlag = True
allFile = os.listdir(userDir)
totalUser = len(allFile)
allID = [0] * totalUser
font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

for file in allFile:
    allID[count2] = int(file.split(".")[1])
    count2 += 1

allID = list(dict.fromkeys(allID))

while True:
    if faceID in allID:
        print("User", faceID, "sudah ada!")
        print("Nomor User terdaftar:", allID)
        print("Coba nomor User lain\n")
        break

    elif faceIDFlag == True:
        print("Perekaman data wajah User: ", faceID)
        faceIDFlag = False
        
    jumlahWajah = 0
    succes, frame = cam.read()
    imgRGB = cv2.flip(frame, 1)
    imgGray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(imgGray, 1.3, 5)

    for x, y, w, h in faces:
        imgRGB = cv2.rectangle(imgRGB, (x, y), (x+w, y+h), (186, 39, 59), 2)
        jumlahWajah = int(str(faces.shape[0]))

        if jumlahWajah == 1:
            count1 += 1
            namaFile = 'User.' + str(faceID) + '.' + str(count1) + '.jpg'
            cv2.imwrite(userDir + '/' + namaFile, imgGray[y:y+h, x:x+w])

    text = 'Perekaman ke: ' + str(count1) + '/' + str(faceSample)
    imgRGB = cv2.putText(imgRGB, str(text), (10, 25), font, 0.7, (54, 67, 244), 2)
    cv2.imshow('Pengambilan Dataset Wajah', imgRGB)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    elif count1 >= faceSample:
        break

cam.release()
cv2.destroyAllWindows()

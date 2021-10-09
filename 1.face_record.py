import os
import cv2

newUser = input('Masukkan nama user baru: ')

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
resolution = 480 #pixel

ratio = 4 / 3
rgbHeight = resolution
rgbWidth = int(round(rgbHeight * ratio, 0))
cam.set(3, rgbWidth)
cam.set(4, rgbHeight)

count1 = 0
count2 = 0
faceSample = 30
faceIDFlag = True
userDir = 'dataset'
cascadePath = 'data/haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

with open('Username.txt', 'r') as user :
    names = user.read()

if newUser in names:
    print('Nama user sudah ada!')
    print('Coba nama user lain!\n')
    faceIDFlag = False

elif '\n\n' in names:
    print('Penambahan user baru: ', newUser)
    names = names.replace('\n\n', '\n' + newUser + '\n')

    with open('Username.txt', 'w') as user:
        user.write(names)

else:
    print('Penambahan user baru: ', newUser)
    with open('Username.txt', 'a') as user:
            user.write(newUser + '\n')

with open('Username.txt', 'r') as user:
    names = user.read().splitlines()
    faceID = names.index(newUser)

while True:
    if faceIDFlag == True:
        print("Perekaman data wajah User", faceID)
        jumlahWajah = 0
        succes, frame = cam.read()
        
        if succes:
            imgRGB  = cv2.flip(frame, 1)
            imgGray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
            imgGray = cv2.resize(imgGray, (rgbWidth, rgbHeight))
            faces = faceDetector.detectMultiScale(imgGray, 1.2, 3)

            for x, y, w, h in faces:
                imgRGB = cv2.rectangle(imgRGB, (x, y), (x+w, y+h), (0, 255, 0), 2)
                jumlahWajah = int(str(faces.shape[0]))
                
                if jumlahWajah == 1:
                    count1 += 1
                    namaFile = 'User.' + str(faceID) + '.' + str(count1) + '.jpg'
                    cv2.imwrite(userDir + '/' + namaFile, imgGray[y:y+h, x:x+w])

            cv2.imshow('Pengambilan Dataset Wajah', imgRGB)

    elif faceIDFlag == False:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    elif count1 >= faceSample:
        break

cam.release()
cv2.destroyAllWindows()
import cv2

cam = cv2.VideoCapture(0)
ratio = 0.75
rgbWidth = 640
rgbHeight = int(rgbWidth * ratio)
cam.set(3, rgbWidth)
cam.set(4, rgbHeight)

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

kondisiSebelum  =  0
kondisiSekarang =  0

def detectFace():
    jumlahWajah = 0
    grayWidth = 220
    grayHeight = int(grayWidth * ratio)
    scaling = rgbWidth / grayWidth
    
    succes, frame = cam.read()
    imgRGB = cv2.flip(frame, 1)
    imgGray = cv2.resize(imgRGB, (grayWidth, grayHeight))
    imgGray = cv2.cvtColor(imgGray, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(imgGray, 1.2, 3)

    for x1, y1, w1, h1 in faces:
        x2 = int(round(x1 * scaling, 0))
        y2 = int(round(y1 * scaling, 0))
        w2 = int(round(w1 * scaling, 0))
        h2 = int(round(h1 * scaling, 0))

        imgRGB = cv2.rectangle(imgRGB, (x2, y2), (x2+w2, y2+h2), (186, 39, 59), 2)
        jumlahWajah = int(str(faces.shape[0]))

        if jumlahWajah > 1:
            imgRGB = cv2.putText(imgRGB, str('Wajah lebih dari satu!'), (15, 50), font, 0.7, (54, 67, 244), 2)

    cv2.imshow('Face Detection', imgRGB)
    
    return jumlahWajah

try:
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

except KeyboardInterrupt:
    print("Program Stop")

finally:    
    cam.release()
    cv2.destroyAllWindows()
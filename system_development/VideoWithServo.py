import cv2
import time

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ratio = 0.75
rgbWidth = 480
rgbHeight = int(round(rgbWidth * ratio))
cam.set(3, rgbWidth)
cam.set(4, rgbHeight)

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'data/haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

def detectFace():
    jumlahWajah = 0
    grayWidth = 220
    grayHeight = int(round(grayWidth * ratio))
    scaling = rgbWidth / grayWidth
    
    succes, frame = cam.read()
    if succes:
        imgRGB = cv2.flip(frame, 1)
        imgGray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
        imgGray = cv2.resize(imgGray, (grayWidth, grayHeight))
        faces = faceDetector.detectMultiScale(imgGray, 1.2, 3)

        for x1, y1, w1, h1 in faces:
            x2 = int(round(x1 * scaling, 0))
            y2 = int(round(y1 * scaling, 0))
            w2 = int(round(w1 * scaling, 0))
            h2 = int(round(h1 * scaling, 0))

            imgRGB = cv2.rectangle(imgRGB, (x2, y2), (x2+w2, y2+h2), (186, 39, 59), 2)
            jumlahWajah = int(str(faces.shape[0]))

            if jumlahWajah > 1:
                imgRGB = cv2.putText(imgRGB, str('Wajah lebih dari satu!'), (15, 25), font, 0.7, (54, 67, 244), 2)
        else:
            print(0)

    cv2.imshow('Face Detection', imgRGB)

try:
    while True:
        detectFace()

        time.sleep(0.04)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program Stop")

finally:    
    cam.release()
    cv2.destroyAllWindows()
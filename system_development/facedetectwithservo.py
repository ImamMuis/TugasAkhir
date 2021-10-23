import cv2
from adafruit_servokit import ServoKit

cam = cv2.VideoCapture(0)
ratio = 0.75
rgbWidth = 640
rgbHeight = int(rgbWidth * ratio)
cam.set(3, rgbWidth)
cam.set(4, rgbHeight)

setX = 90
setY = 90
scanArea = [154, 154, 486, 326]

kit = ServoKit(channels=16)
kit.servo[0].angle = setX
kit.servo[1].angle = setY
kit.servo[0].set_pulse_width_range(500, 2750)
kit.servo[1].set_pulse_width_range(500, 2750)

font = cv2.FONT_HERSHEY_SIMPLEX
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

def detectFace():
    global setX
    global setY
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
        x2 = round(x1 * 3, 0)
        y2 = round(y1 * 3, 0)
        w2 = round(w1 * 3, 0)
        h2 = round(h1 * 3, 0)
        cX = int(round(x2+w2/2, 0))
        cY = int(round(y2+h2/2, 0))
        
        imgRGB = cv2.rectangle(imgRGB, (x2, y2), (x2+w2, y2+h2), (186, 39, 59), 2)

        if cX < scanArea[0]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu kiri!'), (15, 25), font, 0.7, (54, 67, 244), 2)
            setY += 2
            kit.servo[1].angle = setY
       
        elif cX > scanArea[2]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu kanan!'), (15, 75), font, 0.7, (54, 67, 244), 2)
            setY -= 2
            kit.servo[1].angle = setY
            
        if cY > scanArea[3]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu bawah!'), (15, 100), font, 0.7, (54, 67, 244), 2)
            setX += 2
            kit.servo[0].angle = setX
            
        elif cY < scanArea[1]:
            imgRGB = cv2.putText(imgRGB, str('Wajah terlalu atas!'), (15, 50), font, 0.7, (54, 67, 244), 2)
            setX -= 2
            kit.servo[0].angle = setX
            
#     imgRGB = cv2.rectangle(imgRGB, (scanArea[0], scanArea[1`]), (scanArea[2], scanArea[3]), (186, 39, 59), 2)
    cv2.imshow('Face Detection', imgRGB)

try:
    while True:
        CAM()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    print("\nProgram Stop")
    
finally:
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
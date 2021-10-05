
import cv2

cam = cv2.VideoCapture(0)
videoCodec = cv2.VideoWriter_fourcc(*'avc1')
file = str(userDir) + '/' + str(foto)
videoOut = cv2.VideoWriter('videoOutput.mp4', videoCodec, 25.0, (640, 480))

def saveImage(img):
    waktu = getCurrent("Date")
    namaFile = 'Snapshot.' + str(waktu) + '.jpg'
    cv2.imwrite(userDir + '/' + namaFile, img)

while True:
    succes, frame = cam.read()
    videoOut.write(frame)
    imgRGB = cv2.flip(frame, 1)
    cv2.imshow('Video Record', imgRGB)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
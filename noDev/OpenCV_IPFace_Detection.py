import cv2

ipv4_url = 'http://192.168.43.1:8080'
cam = f'{ipv4_url}/video'
cam = cv2.VideoCapture(cam)

cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

def CAM():
	succes, frame = cam.read()
	frame = cv2.flip(frame, 1)
	frame = cv2.resize(frame, (540, 405))
	abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)

	for x, y, w, h in faces:
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow('Face Detection', frame)

while True:
	test = CAM()

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
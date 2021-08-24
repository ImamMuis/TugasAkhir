import cv2
import numpy as np

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 720)
cam.set(4, 360)

cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read('data_training/trainer.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0
names = ['Unknown','Imam','Iis']

while True:

	succes, frame = cam.read()
	frame = cv2.flip(frame, 1)
	abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces  = faceDetector.detectMultiScale(abuAbu, 1.2, 3)

	for x,y,w,h in faces:
		frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
		id, confidence = faceRecognizer.predict(abuAbu[y:y+h, x:x+w])

		if confidence >= 80 and confidence <= 100:
			nameID = names[id]
			confidenceTxt = " {0}%".format(round(confidence))

		else:
			nameID = names[0]
			confidenceTxt = " {0}%".format(round(100-confidence))

		cv2.putText(frame, str(nameID), (x,y-5), font, 0.9, (255,255,255), 2)
		cv2.putText(frame, str(confidenceTxt), (x+w-60,y+h-5), font ,0.7, (255,255,0), 2)

	cv2.imshow('Face Recognition', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
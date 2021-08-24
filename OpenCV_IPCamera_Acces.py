import cv2

ipv4_url = 'http://192.168.43.1:8080'
cam = f'{ipv4_url}/video'
cam = cv2.VideoCapture(cam)

while True:
	succes, frame = cam.read()
	frame = cv2.flip(frame, 1)
	frame = cv2.resize(frame, (360, 270))

	cv2.imshow('Face Detection', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
import os
import cv2

# Uncomment jika pakai webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 720)
cam.set(4, 360)

# Uncomment jika pakai ipcamera
# ipv4_url = 'http://192.168.43.1:8080'
# cam = f'{ipv4_url}/video'
# cam = cv2.VideoCapture(cam)

faceID  = 1
faceSample = 200
userDir = 'dataset'

count1 = 1
count2 = 0
faceIDFlag = True
allFile = os.listdir(userDir)
totalUser = len(allFile)
allID = [0] * totalUser
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
		print("Coba nomor User lain")
		break

	elif faceIDFlag == True:
		print("Perekaman data wajah User", faceID)
		faceIDFlag = False

	jumlahWajah = 0

	succes, frame = cam.read()
	frame  = cv2.flip(frame, 1)
	abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)

	for x, y, w, h in faces:
		frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		jumlahWajah = int(str(faces.shape[0]))
		if jumlahWajah == 1:
			count1 += 1
			namaFile = 'User.' + str(faceID) + '.' + str(count1) + '.jpg'
			cv2.imwrite(userDir + '/' + namaFile, abuAbu[y:y+h, x:x+w])

	cv2.imshow('Pengambilan Dataset Wajah', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	elif count1 == faceSample:
		break

cam.release()
cv2.destroyAllWindows()
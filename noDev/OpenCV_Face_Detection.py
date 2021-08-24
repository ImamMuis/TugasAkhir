# Import library OpenCV
import cv2

# Memulai Video dari webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Mengatur ukuran lebar video ke 480 pixel
cam.set(3, 400)

# Mengatur ukuran tinggi video ke 360 pixel
cam.set(4, 225)

# File untuk pendeteksian wajah
# dengan  Haarcascade Frontal Face
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

def CAM():
	# Memulai membaca video
	succes, frame = cam.read()

	# Flip video
	frame = cv2.flip(frame, 1)

	# Konversi gambar ke abu-abu
	abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Mendeteksi wajah dari variabel abuAbu
	faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)

	for x, y, w, h in faces:
		# Membuat rectangle di area wajah
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	# Membuat window hasil tangkapan kamera
	cv2.imshow('Face Detection', frame)

# Start perulangan menggunakan while
while True:
	test = CAM()

	# Tekan q untuk stop window
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Stop hasil tangkapan kamera
cam.release()

# Tutup semua window yang berjalan
cv2.destroyAllWindows()
# Import library OpenCV
import cv2

# Memulai Video dari webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Mengatur ukuran lebar video ke 480 pixel
cam.set(3, 400)

# Mengatur ukuran tinggi video ke 360 pixel
cam.set(4, 225)


# Start perulangan menggunakan while
while True:

	# Memulai membaca video
	succes, frame = cam.read()

	# Membuat window hasil tangkapan kamera
	cv2.imshow('Face Detection', frame)
	
	# Tekan q untuk stop window
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Stop hasil tangkapan kamera
cam.release()

# Tutup semua window yang berjalan
cv2.destroyAllWindows()
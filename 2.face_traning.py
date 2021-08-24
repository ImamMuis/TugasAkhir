# Import library OpenCV, OS, numpy dan PIL
import cv2
import os
import numpy as np
from PIL import Image

# File untuk mendeteksi wajah
# dengan  Haarcascade Frontal Face
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

# Pengenalan Wajah menggunakan LBPH
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

# Nama folder sampel wajah
userDir = 'dataset'

# Fungsi untuk mengambil gambar dan label   
def getImagesLabel(path):

	# Mengambil data path setiap file sampel wajah
	imagePaths  = [os.path.join(path, f) for f in os.listdir(path)]

	# Variabel penyimpanan data sampel wajah
	faceSamples = []

	# Variabel penyimpanan data id wajah
	faceIDs     = []

	# Perulangan untuk memproses keselurahan sampel wajah
	for imagePath in imagePaths:

		# Buka gambar lalu convert ke abu-abu
		PIL_img   = Image.open(imagePath).convert('L')

		# Convert data gambar menjadi array numpy
		img_numpy = np.array(PIL_img, 'uint8')

		# Mengetahui nomor id pada file sampel wajah
		faceID    = int(os.path.split(imagePath)[-1].split(".")[1])
		print(faceID)

		# Mendeteksi sampel wajah dari data numpy
		faces = faceDetector.detectMultiScale(img_numpy)
		
		for x, y, w, h in faces:
			# Menyatukan tiap sampel wajah
			faceSamples.append(img_numpy[y:y+h, x:x+w])

			# Menyatukan tiap tiap id
			faceIDs.append(faceID)

	# Return semua sampel wajah dan id
	return faceSamples, faceIDs

# 2 variabel untuk traning pengelanan wajah 
# dari hasil return fungsi getImagesLabel
faces, IDs = getImagesLabel(userDir)

# Training data wajah
faceRecognizer.train(faces, np.array(IDs))

# Simpan data dalam bentuk file trainer.yml
faceRecognizer.write('data_training/trainer.xml')
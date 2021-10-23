""" 
Proyek Akhir :  PENERAPAN FACE RECOGNITION UNTUK SISTEM
                KEAMANAN PINTU RUANGAN BERBASIS
                KECERDASAN BUATAN 
Grup         :  7
Anggota      :  - Iis Lisnawati (Mekanikal & Elektrikal)
                - Imam Muis Hamzah Harahap (Pemrograman Sistem)
Cara pakai   :  Jalankan file kemudian tunggu sampai proses training selesai
"""

import os
import cv2
import numpy as np
from PIL import Image

root = ''
userDir = root + 'dataset'
cascadePath = root + 'data/haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

def getImagesLabel(path):
	imagePaths  = [os.path.join(path, f) for f in os.listdir(path)]
	faceSamples = []
	faceIDs     = []
	for imagePath in imagePaths:
		PIL_img   = Image.open(imagePath).convert('L')
		img_numpy = np.array(PIL_img, 'uint8')
		faceID    = int(os.path.split(imagePath)[-1].split(".")[1])
		print(faceID)
		faces = faceDetector.detectMultiScale(img_numpy)
		for x, y, w, h in faces:
			faceSamples.append(img_numpy[y:y+h, x:x+w])
			faceIDs.append(faceID)
	return faceSamples, faceIDs

faces, IDs = getImagesLabel(userDir)
faceRecognizer.train(faces, np.array(IDs))
faceRecognizer.write(root + 'data/trainer.xml')
print('Training Dataset selesai!')
# Import library OpenCV dan numpy
import cv2
import numpy as np

# Memulai Video dari webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Atur ukuran lebar video ke 720 pixel
cam.set(3, 720)

# Atur ukuran tinggi video ke 360 pixel
cam.set(4, 360)

# File untuk pendeteksian wajah
# dengan  Haarcascade Frontal Face
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

# Pengenalan wajah dengan LBPH
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

# Membaca file hasil training data sampel wajah
faceRecognizer.read('data_training/trainer.xml')

# Font untuk teksi di window
font = cv2.FONT_HERSHEY_SIMPLEX

# Variabel untuk menyimpan nomor id hasil pengenalan wajah
id = 0

# Nama-nama untuk wajah
names = ['Unknown','Imam','Iis']

# Start perulangan menggunakan while
while True:

    # Memulai membaca video
    succes, frame = cam.read()

    # Flip video
    frame = cv2.flip(frame, 1)

    # Konversi gambar ke abu-abu
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Mendeteksi wajah dari variabel abuAbu
    faces  = faceDetector.detectMultiScale(abuAbu, 1.2, 3)

    for x,y,w,h in faces:
        # Membuat rectangle di area wajah
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0), 2)

        # Membandingkan sampel wajah hasil traning 
        # dengan hasil tangkapan kamera
        id, confidence = faceRecognizer.predict(abuAbu[y:y+h,x:x+w])

        # Jika prediksi lebih dari 80 dan kurang dari 100
        if confidence >= 80 and confidence <= 100:

            # Variabel nameID akan menyimpan nama dari indeks array
            # variabel names sesuai nilai return variabel id
            nameID = names[id]

            # Variabel untuk menyimpan hasil Akurasi
            confidenceTxt = " {0}%".format(round(confidence))

        else:
            # Jika wajah terdeteksi tetapi tidak dikenali maka 
            # variabel nameID akan menerima string "Unknown" dari 
            # indeks ke 0 variabel names
            nameID = names[0]

            # Variabel untuk menyimpan hasil Akurasi
            confidenceTxt = " {0}%".format(round(100-confidence))

        # Print Nama Wajah pada window
        cv2.putText(frame,str(nameID),(x,y-5),font,
                    0.9, (255,255,255), 2)

        # Print nilai Akurasi pada window
        cv2.putText(frame,str(confidenceTxt),(x+w-60,y+h-5),font,
                    0.7, (255,255,0), 2)

    # Membuat window hasil tangkapan kamera
    cv2.imshow('Face Recognition', frame)

    # Tekan q untuk stop window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop hasil tangkapan kamera
cam.release()

# Tutup semua window yang berjalan
cv2.destroyAllWindows()
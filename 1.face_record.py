# Import library OpenCV
import cv2

# Memulai Video dari webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

 # Mengatur ukuran lebar video ke 720 pixel
cam.set(3, 720)

# Mengatur ukuran tinggi video ke 360 pixel
cam.set(4, 360)

# File untuk pendeteksian wajah
# dengan  Haarcascade Frontal Face
cascadePath = 'haarcascade_frontalface_default.xml'
faceDetector = cv2.CascadeClassifier(cascadePath)

# Nama folder sampel wajah
userDir = 'dataset'

# Penomoran Wajah, satu id untuk satu orang
faceID  = 1

# counter sampel wajah
count   = 0

faceSample = 200

# Start perulangan menggunakan while
while True:

    # Memulai membaca video
    succes, frame = cam.read()

    # Flip video
    frame  = cv2.flip(frame, 1)

    # Konversi gambar ke abu-abu
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Mendeteksi wajah dari variabel abuAbu
    faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)

    for x, y, w, h in faces:
        # Membuat rectangle untuk wajah
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # Increment untuk sampel wajah
        count += 1
 
        # Nama file sampel wajah
        namaFile = 'User.'+str(faceID)+'.'+str(count)+'.jpg'

        # Simpan file sampel wajah dan di crop
        cv2.imwrite(userDir+'/'+namaFile, abuAbu[y:y+h,x:x+w])

    # Membuat window hasil tangkapan kamera
    cv2.imshow('Pengambilan Dataset Wajah', frame)

    # Tekan q untuk stop video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Jika sampel gambar wajah sudah lebih dari 200, stop pengambilan gambar
    elif count >= faceSample:

        break

# Stop hasil tangkapan kamera
cam.release()

# Tutup semua window yang berjalan
cv2.destroyAllWindows()
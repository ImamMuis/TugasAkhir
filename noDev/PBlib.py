# Library untuk menggunakan GPIO Raspberry
import RPi.GPIO as GPIO

# Memakai GPIO mode BCM
GPIO.setmode(GPIO.BCM)

# Fungsi untuk mendeteksi kondisi Limit Switch
# Parameter: pinBuka dan pinTutup
# pinBuka: Limit Switch mendeteksi Pintu telah terbuka
# pinTutup: Limit Switch mendeteksi Pintu telah tertutup
def L_Switch(pinBuka, pinTutup):

	# Mengatur GPIO untuk Limit Switch sebagai Input
    GPIO.setup(pinBuka, GPIO.IN)
    GPIO.setup(pinTutup, GPIO.IN)
    
    # Mengecek adanya input pada limit switch
    # nilai 0: tidak ada input
    # nilai 1: terdapat input
    buka = GPIO.input(pinBuka)
    tutup = GPIO.input(pinTutup)
    
    # Mengembalikan nilai input
    return buka, tutup
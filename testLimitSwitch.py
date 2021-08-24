import time
import PBlib
import RPi.GPIO as GPIO

pinLS_Buka = 22
pinLS_Tutup = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinLS_Buka, GPIO.IN)
GPIO.setup(pinLS_Tutup, GPIO.IN)

try: 
	while True:
		buka = GPIO.input(pinLS_Buka)
		tutup = GPIO.input(pinLS_Buka)

		if buka == True:
			print("Pintu terbuka, ", count)
			time.sleep(0.02)

		elif tutup == True:
			print("Pintu tertutup, ", count)
			time.sleep(0.02)

		else:
			print("Tombol tidak ditekan, ", count)
			time.sleep(0.02)

		count += 1

except KeyboardInterrupt:
	print("Program Stop")

except:
	print("Other Error or exception occured!")

finally:
	GPIO.cleanup()
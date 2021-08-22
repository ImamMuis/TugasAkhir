import time
import datetime

while True:
	now = datetime.datetime.now()
	currentDateTime = int(now.strftime("%S"))
	print(currentDateTime)
	time.sleep(1)
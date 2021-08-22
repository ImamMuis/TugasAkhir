import datetime
import time

Time = 0

def lastdigits(nums):
	num %= 10
	print(abs(num))

def timeNow():
	now = datetime.datetime.now()
	# FORMAT: YY.MM.DD.H:M:S
	currentDateTime = int(now.strftime("%S"))

	return currentDateTime
	# print(currentDateTime)

def timeNow2():
	now = str(datetime.datetime.now())
	now = round(float(now.split(":")[-1]), 3)
	return now

Time = timeNow2()
print(Time)

# while True:
# 	Time = timeNow2()
# 	print(Time)
	# time.sleep(0.01)
import time
import datetime

Time = 0
def lastdigits(num):
	# num %= 10
	print(round(abs(num % 10), 3))

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

list1 = [1, 0, 1, 0, 1]
list2 = [1, 0, 1, 0, 1]

if (list1 == list2):
	print("YES!")

# lastdigits(123.456)
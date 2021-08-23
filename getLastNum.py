import time
import datetime

# Time = 0
# def lastdigits(num):
# 	# num %= 10
# 	print(round(abs(num)%10, 3))

# def timeNow():
# 	now = datetime.datetime.now()
# 	# FORMAT: YY.MM.DD.H:M:S
# 	currentDateTime = int(now.strftime("%S"))

# 	return currentDateTime
# 	# print(currentDateTime)

# def timeNow2():
# 	now = str(datetime.datetime.now())
# 	now = round(float(now.split(":")[-1]), 3)

# 	return now

# class getCurrent:
#     """docstring for get"""
# 	def __init__(self):
# 	    now = str(datetime.datetime.now())
# 		self.now = now

# 	def Date(self):
# 		DATE = now.strftime("%Y-%m-%d %H:%M:%S")
# 		self.DATE = DATE

# 		return 

# 	def Time(self):
# 	    TIME = round(float(now.split(":")[-1]), 3)
# 		self.TIME = TIME
# 		return 

def getCurrent(data):
    now = datetime.datetime.now()
    if data == "Date":
	    value = now.strftime("%Y-%m-%d %H:%M:%S")

    elif data == "Time":
	    value = round(float(str(now).split(":")[-1]), 3)

    else:
        print("WRONG PARAMETER!")

    return value

tanggal = getCurrent("Date")
waktu = getCurrent("Time")

print(tanggal)
print(waktu)

# waktu = getCurrent()

# print(waktu.DATE())
# print(waktu.TIME())

# list1 = [1, 0, 1, 0, 1]
# list2 = [1, 0, 1, 0, 1]



# if (list1 == list2):
# 	print("YES!")

# lastdigits(-123.456)
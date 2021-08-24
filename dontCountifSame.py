import os

faceID = 1

count2 = 0
userDir = 'dataset'
allFile = os.listdir(userDir)
totalUser = len(allFile)
allID = [0] * totalUser

for file in allFile:
	allID[count2] = int(file.split(".")[1])
	count2 += 1

allID = list(dict.fromkeys(allID))

while  True:
	if faceID  in allID:
		print("User", faceID, "sudah ada!")
		print("User terdaftar:", allID)
		print("Coba nomor User lain")
		break
	else:
		print("Perekaman data wajah User", faceID)
		break
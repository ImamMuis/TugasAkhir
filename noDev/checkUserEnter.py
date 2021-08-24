userMasuk = 

dataUser = ['Unknown', 'Imam', 'Iis']

for i in range(len(dataUser)):
	if userMasuk == i:
		userMasukEnter = dataUser[userMasuk]
		break

if userMasuk == 0:
	print("Wajah tidak dikenali!")

else:
	print("User", userMasukEnter, "Masuk")
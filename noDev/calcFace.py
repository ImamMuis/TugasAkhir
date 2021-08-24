
names = ['Unknown','Imam', 'Imam2', 'Imam3']
totalUser = len(names)
countID = [0] * totalUser

detectResult = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 

				1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
				1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 

				2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
				2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
				2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 

				3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
				3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
				3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
				3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
			]

for i in range(totalUser):
	countID[i] = detectResult.count(i)
	print("User", names[i], ":", countID[i])

bigCount = names[countID.index(max(countID))]
print("User terdeteksi:", bigCount)
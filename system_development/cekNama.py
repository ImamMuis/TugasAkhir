import time
fileUser = 'data/Username.txt'

nameResult = 'Hawd'

with open(fileUser) as user:
    names = user.read().splitlines()

if nameResult in names[1:]:
	print(nameResult)
print(time.time())
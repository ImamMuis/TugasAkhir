import os
file = os.listdir('/home/pi/[master]/img_record')
lastImage = sorted(file,key=lambda x: os.path.splitext(x)[0])
print(lastImage)
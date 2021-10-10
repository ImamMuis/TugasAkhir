import os
directory = 'img_record'

for filename in os.listdir(directory):
    count = 0
    changeName = [0] * 14
    oldName = directory + '/' + filename
    filename = str(filename.split('.')[-2])
    for huruf in filename:
        changeName[count] = str(huruf)
        count += 1

    changeName.insert(4, '-')
    changeName.insert(7, '-')
    changeName.insert(10, '.')
    changeName.insert(13, '.')
    changeName.insert(16, '.')
    
    changeName = ''.join(str(v) for v in changeName)
    newName = directory + '/Snapshot.' + str(changeName) + '.jpg'
    print(newName)
    os.rename(oldName, newName)
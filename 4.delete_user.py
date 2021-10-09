import os

deleteUser = input('Masukkan nama user yang ingin dihapus: ')
userID = 0
jumlahGambar = 30
userDir = 'dataset'

with open('Username.txt', 'r') as user:
    names = user.read().splitlines()

    if deleteUser not in names:
        print('User', deleteUser, 'Tidak ada!')
        print('Cek kembali user yang ingin di hapus')

    else:
        deleteId = names.index(deleteUser)

        for num in range(1, jumlahGambar+1):
            file = userDir + '/' + 'User.' + str(deleteId) + '.' + str(num) + '.jpg'
            os.remove(file)

with open('Username.txt', 'r') as user :
    names = user.read()
    names2 = names.splitlines()

    if deleteUser in names2:
        print('Penghapusan User', deleteUser)
        names = names.replace(deleteUser, '')

        with open('Username.txt', 'w') as user:
            user.write(names)

with open('Username.txt', 'r') as user:
    names = user.read().splitlines()
    names.reverse()

    while names[0] == '':
        names.remove('')

    names.reverse()

with open('Username.txt', 'w') as user:
    for name in names:
        user.write('%s\n' %name)
""" 
Proyek Akhir :  PENERAPAN FACE RECOGNITION UNTUK SISTEM
                KEAMANAN PINTU RUANGAN BERBASIS
                KECERDASAN BUATAN 
Grup         :  7
Anggota      :  - Iis Lisnawati (Mekanikal & Elektrikal)
                - Imam Muis Hamzah Harahap (Pemrograman Sistem)
Cara pakai   :  Jalankan file kemudian ketikkan nama user yang ingin dihapus
"""

import os

deleteUser = input('Masukkan nama user yang ingin dihapus: ')
userID = 0
jumlahGambar = 30
root = '/home/pi/1.TugasAkhir/'
userDir = root + 'dataset'
fileUser = root + 'data/Username.txt'

with open(fileUser) as user:
    names = user.read().splitlines()

    if deleteUser not in names:
        print('User', deleteUser, 'Tidak ada!')
        print('Cek kembali user yang ingin di hapus')

    else:
        deleteId = names.index(deleteUser)

        for num in range(1, jumlahGambar+1):
            file = userDir + '/' + 'User.' + str(deleteId) + '.' + str(num) + '.jpg'
            os.remove(file)

with open(fileUser) as user :
    names = user.read()
    names2 = names.splitlines()

    if deleteUser in names2:
        print('Penghapusan User', deleteUser)
        names = names.replace(deleteUser, '')

        with open(fileUser, 'w') as user:
            user.write(names)

with open(fileUser) as user:
    names = user.read().splitlines()
    names.reverse()

    while names[0] == '':
        names.remove('')

    names.reverse()

with open(fileUser, 'w') as user:
    for name in names:
        user.write('%s\n' %name)
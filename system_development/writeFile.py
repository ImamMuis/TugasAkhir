newUser = input('Masukkan nama user baru: ')

with open('Username.txt', 'r') as user :
    names = user.read()

if newUser in names:
    print('Nama user sudah ada!')
    print('Coba nama user lain!\n')

elif '\n\n' in names:
    print('Penambahan user baru: ', newUser)
    names = names.replace('\n\n', '\n' + newUser + '\n')

    with open('Username.txt', 'w') as user:
        user.write(names)

else:
    print('Penambahan user baru: ', newUser)
    with open('Username.txt', 'a') as user:
        user.write(newUser + '\n')
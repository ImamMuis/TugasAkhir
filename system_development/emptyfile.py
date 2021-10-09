with open('Username.txt', 'r') as user:
    names = user.read().splitlines()
    names.reverse()

    while names[0] == '':
        names.remove('')

    names.reverse()

with open('Username.txt', 'w') as user:
    for name in names:
        user.write('%s\n' %name)
with open('Username.txt', 'r') as user:
    names = user.read().splitlines()
    print(names)
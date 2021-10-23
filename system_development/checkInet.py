import time
import socket

def internetConnected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True

    except socket.error:
        return False

while True:
    if internetConnected():
        print('Terkoneksi dengan internet')
        break

    else:
        print('Internet tidak terkoneksi!')
        time.sleep(2)
        print('Mencoba mengoneksikan dengan internet kembali')
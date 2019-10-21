from __future__ import print_function

import socket


def main():
    client()


def client():
    s = socket.socket()
    port = 12345
    s.connect(('0.0.0.0', port))

    send_file(s)

    s.send('Here I am!'.encode())
    print(s.recv(1024))
    s.close()


def send_file(s):
    f = open("mytext.txt", 'rb')
    l = f.read(1024)
    while l:
        s.send(l)
        print('Sent ', repr(l))
        l = f.read(1024)

    print(s.recv(1024))
    f.close()


if __name__ == '__main__':
    main()
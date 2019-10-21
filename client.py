from __future__ import print_function

import socket


def main():
    client()


def client():
    s = socket.socket()
    port = 12345
    s.connect(('0.0.0.0', port))
    s.send('Here I am!'.encode())
    print(s.recv(1024))
    s.close()


if __name__ == '__main__':
    main()
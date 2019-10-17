from __future__ import print_function

import socket


def main():
    client()


def client():
    s = socket.socket()
    port = 12345
    s.connect(('127.0.0.1', port))
    print(s.recv(1024))
    s.close()


if __name__ == '__main__':
    main()
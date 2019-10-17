from __future__ import print_function

import socket


def main():
    s = socket.socket()

    port = 12345





def server():
    s = socket.socket()
    port = 12345
    s.bind(('', port))
    print("Socker binded to {}".format(port))
    # 5 here means that 5 connections are kept waiting if the server is busy
    s.listen(5)
    while True:
        c, addr = s.accept()

        print("Got connection from {}".format(addr))

        c.send(bytes('Thanks man\n', encoding='utf8'))

        c.close()


def connect_to_google():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = socket.gethostbyname('www.google.com')
    port = 80
    s.connect((host_ip, port))
    print(s)


if __name__ == '__main__':
    main()
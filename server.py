from __future__ import print_function

import os
import socket
from Crypto.Cipher import AES

buffer_size = 20000
key = "00112233445566778899aabbccddeeff"


def main():
    server()


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

        # Encryption

        f =open("tmp.txt",'wb')

        while True:
            data = c.recv(buffer_size)

            if not data:
                break

            print("Received", data)
            data = pad_data(data)

            iv = os.urandom(16)
            aes = AES.new(key, AES.MODE_CBC, iv)

            encd = aes.encrypt(data)
            # print("Encrypting",encd)

            to_send = iv + encd
            print("Writing ecrypted data", to_send)

            f.write(to_send)

        f = open("mytext.txt", mode='rb')
        l = f.read(buffer_size)

        while l:
            c.send(l)

        print('Done sending')

        c.close()


def pad_data(data):
    remainder = len(data) % 16
    if remainder != 0:
        data += bytes(' ' * (16 - remainder), encoding='utf-8')
    return data


if __name__ == '__main__':
    main()

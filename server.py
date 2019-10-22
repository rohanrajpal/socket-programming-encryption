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
    s.bind(('0.0.0.0', port))
    print("Socker binded to {}".format(port))
    # 5 here means that 5 connections are kept waiting if the server is busy
    s.listen(5)
    while True:
        c, addr = s.accept()

        print("Got connection from {}".format(addr))

        # Encryption

        iv = os.urandom(16)
        aes = AES.new(key, AES.MODE_CBC, iv)

        data = c.recv(buffer_size)
        remainder = len(data) % 16

        print(data)
        if remainder != 0:
            data += bytes(' ' * (16 - remainder), encoding='utf-8')

        encd = aes.encrypt(data)
        to_send = iv + encd
        c.send(to_send)

        print('Done sending')

        c.close()


if __name__ == '__main__':
    main()

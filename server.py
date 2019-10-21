from __future__ import print_function

import os
import socket
import random
import struct
from Crypto import Random
from Crypto.Cipher import AES


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
        # print(c.recv(1024))

        infile = 'tempfile.txt'

        with open(infile) as fout:
            fout.write(c.recv(1024))

        encfile = 'enctext.txt'

        # Encryption
        key = "00112233445566778899aabbccddeeff"
        iv = os.urandom(16)
        # print(len(iv))
        # print(len(key))
        # iv = Random.new().read(16)
        aes = AES.new(key, AES.MODE_CBC, iv)

        # fsz = os.path.getsize(infile)
        sz = 2048

        with open(encfile, 'wb') as fout:
            with open(infile) as fin:
                while True:
                    data = fin.read(sz)
                    n = len(data)
                    if n == 0:
                        break
                    elif n % 16 != 0:
                        data += ' ' * (16 - n % 16)  # <- padded with spaces
                    encd = aes.encrypt(data)
                    fout.write(encd)



        print('Done sending')

        c.close()


if __name__ == '__main__':
    main()

from __future__ import print_function

import os
import socket
from math import ceil
from Crypto.Cipher import AES

buffer_size = 32
key = "00112233445566778899aabbccddeeff"


def get_num(b):
    s = b.decode("utf-8")
    print("fsize",s)
    return int(s)

def main():
    server()

def num_pkt(size):
    return int(ceil(size/buffer_size))

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

        #receiving file size
        fsize = c.recv(buffer_size)
        print("len_data",len(fsize))
        fsize = get_num(fsize)
        #expected no. of packets 
        num_exp = num_pkt(fsize)


        # while True:


        for i in range(num_exp):
            data = c.recv(buffer_size)
            data = pad_upto_buf(data)
            print("len_data_recvd",len(data))
            
            # if not data:
            #     break
            print("Received", data)
            iv = os.urandom(16)            
            aes = AES.new(key, AES.MODE_CBC, iv)                    
            data = pad_data(data)
            encd = aes.encrypt(data)
            # print("Encrypting",encd)

            to_send = iv + encd
            print("len_send",len(to_send))
            print("Writing ecrypted data", to_send)

            f.write(to_send)
        print("d")   
        f = open("tmp.txt", mode='rb')
        

        val_to_send = buffer_size + 16
        if buffer_size%16 != 0:
            val_to_send += 16 - (buffer_size%16)

        print(str(val_to_send) + " " + "val to send")   

        # l = f.read(buf_size+16)
        l = f.read(val_to_send)

        while l:
            print(str(len(l)) + " Actually sending")
            c.send(l)
            # l = f.read(buf_size+16)
            l = f.read(val_to_send)

        print('Done sending')

        c.close()


def pad_data(data):
    remainder = len(data) % 16
    if remainder != 0:
        data += bytes(' ' * (16 - remainder), encoding='utf-8')
    return data

def pad_upto_buf(data):
    data += bytes(' ' * (buffer_size - len(data)), encoding='utf-8')
    return data    


if __name__ == '__main__':
    main()

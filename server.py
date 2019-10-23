from __future__ import print_function

import os
import socket
from math import ceil
from Crypto.Cipher import AES

buffer_size = 32
key = "00112233445566778899aabbccddeeff"


def get_num(b):
    s = b.decode("utf-8")
    print("fsize", s)
    return int(s)


def main():
    server()


def num_pkt(size):
    return int(ceil(size / buffer_size))


def server():
    s = socket.socket()
    port = 1234
    s.bind(('', port))
    print("Socker binded to {}".format(port))
    # 5 here means that 5 connections are kept waiting if the server is busy
    s.listen(5)
    while True:
        c, addr = s.accept()

        print("Got connection from {}".format(addr))

        # Encryption
        f = open("tmp.txt", 'wb')

        # receiving file size
        fsize = c.recv(buffer_size)
        # print("len_data", len(fsize))
        fsize = get_num(fsize)
        # expected no. of packets
        num_exp = num_pkt(fsize)


        expected_frame = 0
        next_frame_to_send = 1

        alt_bit_buffer = 2

        for i in range(num_exp):
            data = c.recv(buffer_size + alt_bit_buffer).decode()
            # print("Received with ack", data)
            ack = data[:2]
            # print("Got ack",ack,type(ack[0]),ack[1],"Length",len(ack))

            if ack[0] == str(expected_frame):
                # print("In 1")
                expected_frame = 1 - expected_frame
            if ack[1] == str(next_frame_to_send):
                # print("In 2")
                next_frame_to_send = 1 - next_frame_to_send


            sending_Ack = str(next_frame_to_send) + str(1 - expected_frame)
            # print("Sending back ack", sending_Ack)
            c.send(bytes(sending_Ack, encoding='utf-8'))

            # Remove the ack headers
            data = bytes(data[2:],encoding='utf-8')

            data = pad_upto_buf(data)
            # print("len_data_recvd", len(data))

            print("Received", data)
            iv = os.urandom(16)
            aes = AES.new(key, AES.MODE_CBC, iv)
            data = pad_data(data)
            encd = aes.encrypt(data)

            to_send = iv + encd
            # print("len_send", len(to_send))
            # print("Writing ecrypted data", to_send)

            f.write(to_send)


        # print("d")
        f = open("tmp.txt", mode='rb')

        val_to_send = buffer_size + 16
        if buffer_size % 16 != 0:
            val_to_send += 16 - (buffer_size % 16)

        # print(str(val_to_send) + " " + "val to send")

        l = f.read(val_to_send)

        while l:
            # print(str(len(l)) + " Actually sending")
            c.send(l)
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

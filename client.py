import os
import socket
from math import ceil
from Crypto.Cipher import AES

buffer_size = 32
key = "00112233445566778899aabbccddeeff"


def main():
    client()


def client():
    s = socket.socket()
    port = 1234
    s.connect(('', port))

    send_file(s)

    s.close()


def get_fsize(fname):
    statinfo = os.stat(fname)
    sz = statinfo.st_size
    return sz


def file_size(fname):
    sz = str(get_fsize(fname))
    l = len(sz)
    sz += (' ' * (buffer_size - l))
    print("sz", sz)
    sz = bytes(sz, encoding='utf-8')
    return sz


def pad_data(data):
    remainder = len(data) % 16
    # print(data)
    if remainder != 0:
        data += bytes(' ' * (16 - remainder), encoding='utf-8')
    return data


def num_pkt(size):
    return int(ceil(size / buffer_size))


def num_pkts_file(fname):
    return num_pkt(get_fsize(fname))


def send_file(s):
    fname = "mytext.txt"
    f = open(fname, mode='rb')

    fsize = file_size(fname)
    print("In client, file size is: " + str(fsize))
    s.send(fsize)

    l = f.read(buffer_size)

    next_frame_to_send = 0
    expected_frame = 0
    while l:
        # print("Sending",next_frame_to_send,1-expected_frame)

        ack_send = str(next_frame_to_send) + str(1 - expected_frame)
        to_send = bytes(ack_send, encoding='utf-8') + l

        s.send(to_send)
        # print('Sent data', repr(l))
        alt_bit_buffer = 2
        ack = s.recv(alt_bit_buffer).decode()

        # print("Ack is", ack,ack[0],ack[1])
        if ack[0] == str(expected_frame):
            expected_frame = 1 - expected_frame
        # else:
        #     print("Aborting",print(ack))
            # exit()
        if ack[1] == str(next_frame_to_send):
            next_frame_to_send = 1-next_frame_to_send
        # else:
        #     assert False
        l = f.read(buffer_size)

    # print("done")

    cnt_pkt = num_pkts_file(fname)
    # print(cnt, cnt_pkt)
    # print("^Num packets")

    for i in range(cnt_pkt):
        len_exp = 16 + buffer_size
        if buffer_size % 16 != 0:
            len_exp += 16 - (buffer_size % 16)

        # print("len_exp", len_exp)
        recd_data = s.recv(len_exp)

        # print("lcrd", len(recd_data))

        iv = recd_data[:16]
        # print("len", len(iv))

        aes = AES.new(key, AES.MODE_CBC, iv)

        decd = aes.decrypt(pad_data(recd_data[16:]))

        print(decd[:buffer_size].decode("utf-8", "ignore"), end='')

        # print("\n^Fin")

    f.close()


if __name__ == '__main__':
    main()

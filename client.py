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
    port = 12345
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
    sz +=(' '*(buffer_size-l))
    print("sz",sz)
    sz = bytes(sz, encoding='utf-8')
    return sz


def pad_data(data):
    remainder = len(data) % 16
    # print(data)
    if remainder != 0:
        data += bytes(' ' * (16 - remainder), encoding='utf-8')
    return data

def num_pkt(size):
    return int(ceil(size/buffer_size))

def num_pkts_file(fname):
    return num_pkt(get_fsize(fname))

def send_file(s):

    fname = "mytext.txt"
    f = open(fname, mode='rb')

    fsize = file_size(fname)
    print("In client, file size is: " + str(fsize))
    #sending file size
    s.send(fsize)

    l = f.read(buffer_size)

    cnt=0
    
    while l:
        # if cnt > 2:
        #     break
        cnt += 1
        s.send(l)
        print('Sent data', repr(l))
        l = f.read(buffer_size)
        # s.send(l)
    print("done")
    cnt_pkt = num_pkts_file(fname)
    print(cnt,cnt_pkt)
    print("^Num packets")
    # while True:
    for i in range(cnt_pkt):
        # len_exp = 16 + buffer_size + 16 - (buffer_size % 16)
        len_exp = 16 + buffer_size 
        if buffer_size%16 != 0:
            len_exp += 16 - (buffer_size%16)

        print("len_exp",len_exp)
        recd_data = s.recv(len_exp)
        
        print("lcrd",len(recd_data))

        iv = recd_data[:16]
        print("len",len(iv))

        #Check
        aes = AES.new(key, AES.MODE_CBC, iv)

        decd = aes.decrypt(pad_data(recd_data[16:]))
        # print(recd_data)
        # print(recd_data[16:])
        # print("decd",decd)
        print(decd[:buffer_size].decode("utf-8","ignore"),end='')
        # print(decd[:buffer_size].decode(),end='')
        print("\n^Fin")


    f.close()


if __name__ == '__main__':
    main()

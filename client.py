import socket
from Crypto.Cipher import AES

key = "00112233445566778899aabbccddeeff"


def main():
    client()


def client():
    s = socket.socket()
    port = 12345
    s.connect(('', port))

    send_file(s)

    s.close()


def pad_data(data):
    remainder = len(data) % 16
    # print(data)
    if remainder != 0:
        data += bytes(' ' * (16 - remainder), encoding='utf-8')
    return data


def send_file(s):
    buffer_size = 20
    f = open("mytext.txt", mode='rb')
    l = f.read(buffer_size)

    cnt=0
    while l:
        # if cnt > 2:
        #     break
        cnt += 1
        s.send(l)
        # print('Sent data', repr(l))
        l = f.read(buffer_size)
        # s.send(l)

    while True:
        recd_data = s.recv(16 + buffer_size + 16 - (buffer_size % 16))

        if recd_data is None:
            break
        # print(len(recd_data))
        iv = recd_data[:16]
        aes = AES.new(key, AES.MODE_CBC, iv)

        decd = aes.decrypt(pad_data(recd_data[16:]))
        # print(recd_data)
        # print(recd_data[16:])
        print(decd[:buffer_size].decode(),end='')


    f.close()


if __name__ == '__main__':
    main()

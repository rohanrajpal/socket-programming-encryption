import socket
from Crypto.Cipher import AES

key = "00112233445566778899aabbccddeeff"

def main():
    client()


def client():
    s = socket.socket()
    port = 12345
    s.connect(('0.0.0.0', port))

    send_file(s)

    s.send('Here I am!'.encode())
    s.close()


def send_file(s):
    f = open("mytext.txt",mode='rb')

    buffer_size = 20000

    l = f.read(buffer_size)
    s.send(l)

    recd_data = s.recv(buffer_size)

    iv = recd_data[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)

    decd = aes.decrypt(recd_data[16:])
    print(decd)

    f.close()


if __name__ == '__main__':
    main()
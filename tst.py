import os
import socket
from math import ceil
from Crypto.Cipher import AES


key = "00112233445566778899aabbccddeeff"

iv = os.urandom(16)            
aes = AES.new(key, AES.MODE_CBC, iv)                    
# data = pad_data(data)
data = "This is a test string"
print(len(data))
encd = aes.encrypt(data)
print(len(encd))
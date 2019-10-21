# from Crypto.Cipher import AES
from Crypto.Cipher import AES
from Crypto import Random
key = b'Sixteen byte key'
IV = Random.new().read(16)
cipher = AES.new(key, AES.MODE_CBC, IV)

# nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)
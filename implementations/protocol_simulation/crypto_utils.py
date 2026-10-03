from Crypto.Cipher import AES
import base64
import hashlib

BLOCK_SIZE = 16

def pad(data: bytes):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes):
    pad_len = data[-1]
    return data[:-pad_len]

def aes_encrypt(msg, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)

    data = msg.encode()            # convert first
    padded = pad(data)             # pad BYTES

    encrypted = cipher.encrypt(padded)

    return base64.b64encode(encrypted).decode()

def aes_decrypt(enc, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)

    decoded = base64.b64decode(enc)
    decrypted = cipher.decrypt(decoded)

    unpadded = unpad(decrypted)

    return unpadded.decode()

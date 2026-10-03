from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(message, key):
    key_bytes = key[:32].encode()  # 256-bit AES key
    iv = b'0000000000000000'       # demo IV
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return encrypted

def aes_decrypt(ciphertext, key):
    key_bytes = key[:32].encode()
    iv = b'0000000000000000'
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()

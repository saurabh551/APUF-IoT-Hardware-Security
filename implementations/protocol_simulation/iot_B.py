import socket
import pandas as pd
import hashlib

from crypto_utils import aes_decrypt

HOST = "127.0.0.1"
PORT = 5000

crp_db = pd.read_csv("final_enrollment_crp.csv")


def get_response(ch):
    row = crp_db[crp_db['Challenge'] == ch]
    return int(row['Response'].values[0])


print("\n==========================================")
print(" IoT-B waiting for authentication request ")
print("==========================================")

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

conn, _ = server.accept()

# receive CB + timestamp
CB, timestamp = eval(conn.recv(4096).decode())

# generate RB
RB = [get_response(c) for c in CB]

# send RB
conn.send(str(RB).encode())

# receive RA
RA = eval(conn.recv(4096).decode())

# session key generation
print("\n============= SESSION KEY =================")

sk_material = ""

for ra in RA:
    sk_material += str(ra)

for rb in RB:
    sk_material += str(rb)

sk_material += str(timestamp)

SK = hashlib.sha256(sk_material.encode()).hexdigest()

print("[IoT-B] Session Key:")
print(SK)

# receive encrypted message
enc_msg = conn.recv(4096).decode()

if not enc_msg:
    print("❌ No encrypted message received")
    conn.close()
    exit()

print("\n========= SECURE COMMUNICATION =========")

print("[IoT-B] Encrypted Message:")
print(enc_msg)

msg = aes_decrypt(enc_msg, SK)

print("\n[IoT-B] Decrypted Message:")
print(msg)

print("\n✅ Secure Communication Established")

conn.close()

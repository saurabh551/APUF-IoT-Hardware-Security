import socket
import pandas as pd
import hashlib
import time

from server import process_m1, verify
from crypto_utils import aes_encrypt

HOST = "127.0.0.1"
PORT = 5000

crp_db = pd.read_csv("final_enrollment_crp.csv")


def get_response(ch):
    row = crp_db[crp_db['Challenge'] == ch]
    return int(row['Response'].values[0])


# m1
CA, CB, timestamp = process_m1()

# m4 generate RA
RA = [get_response(c) for c in CA]

print("\n==================== m4 ====================")
print("[m4] IoT-A → Server : Responses RA")
print(RA)

# connect to IoT-B
client = socket.socket()
client.connect((HOST, PORT))

# send CB
client.send(str((CB, timestamp)).encode())

# receive RB
RB = eval(client.recv(4096).decode())

print("\n==================== m5 ====================")
print("[m5] IoT-B → Server : Responses RB")
print(RB)

# verify
auth_A, auth_B = verify(CA, RA, CB, RB, timestamp)

if not (auth_A and auth_B):
    print("\n❌ Mutual Authentication FAILED")
    client.close()
    exit()

print("\n✅ Mutual Authentication SUCCESS")

# m6
print("\n==================== m6 ====================")
print("[m6] Server → IoT-A : RB forwarded")

# send RA
client.send(str(RA).encode())

# m7
print("\n==================== m7 ====================")
print("[m7] Server → IoT-B : RA forwarded")

# session key generation
print("\n============= SESSION KEY =================")

sk_material = ""

for ra in RA:
    sk_material += str(ra)

for rb in RB:
    sk_material += str(rb)

sk_material += str(timestamp)

SK = hashlib.sha256(sk_material.encode()).hexdigest()

print("[IoT-A] Session Key:")
print(SK)

# secure communication
print("\n========= SECURE COMMUNICATION =========")

msg = "Hello from IoT-A 🔐"

enc = aes_encrypt(msg, SK)

print("[IoT-A] Plain Text:")
print(msg)

print("\n[IoT-A] Encrypted Message:")
print(enc)

client.send(enc.encode())

client.close()

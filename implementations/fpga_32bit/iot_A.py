# iot_A.py
# IoT-A device (CSV-based 7-CRP authentication)

import time
import hashlib
import json
from server import process_m1_message
from iot_B import send_m3
from crypto_utils import aes_encrypt, aes_decrypt
from fpga_puf_uart import FPGA_PUF

# =====================
# Configuration
# =====================
ID_A = "DeviceA"
ID_B = "DeviceB"
TIMEOUT = 2  # seconds

# =====================
# Initialize FPGA UART
# =====================
fpga = FPGA_PUF()

# =====================
# m1: IoT-A → Server
# =====================
timestamp = str(time.time())
m1 = {
    "ID_A": ID_A,
    "ID_B": ID_B,
    "Timestamp": timestamp
}

print("\n[IoT-A] Sending m1 to Server:")
print(json.dumps(m1, indent=4))

start_time = time.time()
m2 = process_m1_message(m1)
elapsed = time.time() - start_time

if m2 is None or elapsed > TIMEOUT:
    print("\n[IoT-A] ERROR: Timeout waiting for m2")
    exit(0)

print(f"[IoT-A] m2 received in {elapsed:.2f} seconds")

# =====================
# Receive challenges + expected responses
# =====================
challenges = m2["Challenges"]
expected_responses = m2["ExpectedResponses"]

print("\n[IoT-A] Received 7 challenges:")
print(challenges)

# =====================
# Get LIVE responses from FPGA
# =====================
responses_A = []
for ch in challenges:
    resp = fpga.get_response(ch)
    if resp is None:
        print("[IoT-A] FPGA response TIMEOUT")
        fpga.close()
        exit(0)
    responses_A.append(resp)

print("[IoT-A] ResponsesA:")
print(responses_A)

# =====================
# IoT-B Authentication
# =====================
m4, m5 = send_m3(challenges, expected_responses)

# Fill responses into m5
m5["ResponsesA"] = responses_A

# =====================
# Session Key Generation
# =====================
sk_input = "".join(challenges) \
         + "".join(map(str, m5["ResponsesA"])) \
         + "".join(map(str, m5["ResponsesB"]))

SK = hashlib.sha256(sk_input.encode()).hexdigest()
print("\n[IoT-A] Session Key (7-CRP SK):", SK)

# =====================
# m6: Secure Communication
# =====================
message = "Hello from IoT-A (7-CRP Auth)"
encrypted = aes_encrypt(message, SK)

print("\n[m6] Encrypted message:")
print(encrypted)

decrypted = aes_decrypt(encrypted, SK)
print("\n[m6] Decrypted message on IoT-B:")
print(decrypted)

# =====================
# Cleanup
# =====================
fpga.close()

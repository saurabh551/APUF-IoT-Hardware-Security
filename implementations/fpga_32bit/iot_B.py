# iot_B.py
# IoT-B device (CSV-based authentication, live FPGA)

import time
import json
from fpga_puf_uart import FPGA_PUF
from server import process_m3_message

# =====================
# Initialize FPGA UART
# =====================
fpga = FPGA_PUF()

def send_m3(challenges, expected_responses):
    ID_B = "DeviceB"
    ID_A = "DeviceA"
    timestamp = str(time.time())

    # Get LIVE responses from FPGA
    responses_B = []
    for ch in challenges:
        resp = fpga.get_response(ch)
        if resp is None:
            print("[IoT-B] FPGA response TIMEOUT")
            fpga.close()
            exit(0)
        responses_B.append(resp)

    print("\n[IoT-B] Generated 7 responses:")
    print(responses_B)

    # Construct m3
    m3 = {
        "ID_B": ID_B,
        "ID_A": ID_A,
        "Challenges": challenges,
        "ResponsesB": responses_B,
        "ExpectedResponses": expected_responses,
        "Timestamp": timestamp
    }

    print("\n[IoT-B] Sending m3 to Server:")
    print(json.dumps(m3, indent=4))

    # Server verifies using CSV
    m4, m5 = process_m3_message(m3)
    return m4, m5

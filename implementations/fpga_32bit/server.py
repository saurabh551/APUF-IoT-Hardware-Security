# server.py
# CSV-based 7-challenge authentication for 32-bit APUF

import pandas as pd
import time

NUM_CHALLENGES = 7
MAJORITY_THRESHOLD = 4

# ============================
# Load enrolled CRPs (CSV)
# ============================
crp_db = pd.read_csv("final_enrollment_crp.csv")
print("[Server] CRP Database Loaded:", len(crp_db))


# ============================
# m1 Handler (IoT-A → Server)
# ============================
def process_m1_message(m1):
    print("\n[Server] m1 received from IoT-A:")
    print(m1)

    # Randomly select 7 challenges from enrolled CSV
    selected = crp_db.sample(NUM_CHALLENGES)

    challenges = selected["Challenge"].astype(str).tolist()
    expected_responses = selected["Response"].astype(int).tolist()

    print("\n[Server] Selected 7 challenges from CSV:")
    print(challenges)

    # m2 message
    m2 = {
        "Status": "CHALLENGE_SENT",
        "Challenges": challenges,
        "ExpectedResponses": expected_responses,
        "Timestamp": str(time.time())
    }

    print("\n[Server] Sending m2 to IoT-A:")
    print(m2)

    return m2


# ============================
# m3 Handler (IoT-B → Server)
# ============================
def process_m3_message(m3):
    print("\n[Server] m3 received from IoT-B:")
    print(m3)

    challenges = m3["Challenges"]
    responses_B = m3["ResponsesB"]
    expected_responses = m3["ExpectedResponses"]

    match_count = 0
    for r_fpga, r_csv in zip(responses_B, expected_responses):
        if r_fpga == r_csv:
            match_count += 1

    print(f"[Server] Match count: {match_count}/{len(challenges)}")

    if match_count >= MAJORITY_THRESHOLD:
        status = "ACCEPTED"
        print("[Server] Authentication SUCCESS")
    else:
        status = "REJECTED"
        print("[Server] Authentication FAILED")

    # m4: authentication result
    m4 = {
        "Status": status,
        "MatchCount": match_count
    }

    # m5: data for session key
    m5 = {
        "Challenges": challenges,
        "ResponsesA": None,              # filled by IoT-A
        "ResponsesB": responses_B
    }

    print("\n[Server] Sending m4 and m5:")
    print(m4)
    print(m5)

    return m4, m5

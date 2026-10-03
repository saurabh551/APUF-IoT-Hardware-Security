import pandas as pd
import random
import time

crp_db = pd.read_csv("final_enrollment_crp.csv")

THRESHOLD = 5
TIME_WINDOW = 10  # seconds


def get_response(ch):
    row = crp_db[crp_db['Challenge'] == ch]
    return int(row['Response'].values[0])


def select_challenges(n=7):
    return crp_db.sample(n)['Challenge'].tolist()


# m1 → m2 & m3
def process_m1():
    timestamp = time.time()

    CA = select_challenges()
    CB = select_challenges()

    print("\n==================== m1 ====================")
    print("[m1] IoT-A → Server : Authentication Request")
    print(f"Timestamp : {timestamp}")

    print("\n==================== m2 ====================")
    print("[m2] Server → IoT-A : Challenge Set CA")
    print(CA)

    print("\n==================== m3 ====================")
    print("[m3] Server → IoT-B : Challenge Set CB")
    print(CB)

    return CA, CB, timestamp


# verification
def verify(CA, RA, CB, RB, recv_timestamp):

    current_time = time.time()

    print("\n================ VERIFICATION ================")

    # replay attack check
    if abs(current_time - recv_timestamp) > TIME_WINDOW:
        print("❌ Timestamp Expired!")
        return False, False

    print("✅ Timestamp Valid")

    exp_A = [get_response(c) for c in CA]
    exp_B = [get_response(c) for c in CB]

    match_A = sum(1 for e, r in zip(exp_A, RA) if e == r)
    match_B = sum(1 for e, r in zip(exp_B, RB) if e == r)

    print(f"IoT-A Match Count : {match_A}/7")
    print(f"IoT-B Match Count : {match_B}/7")

    auth_A = match_A >= THRESHOLD
    auth_B = match_B >= THRESHOLD

    if auth_A:
        print("✅ IoT-A VERIFIED")
    else:
        print("❌ IoT-A FAILED")

    if auth_B:
        print("✅ IoT-B VERIFIED")
    else:
        print("❌ IoT-B FAILED")

    return auth_A, auth_B

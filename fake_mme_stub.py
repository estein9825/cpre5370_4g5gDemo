import socket

BIND_IP = "10.53.1.100"
PORT = 36412

# Replace this with a valid hex dump of a previously captured S1SetupResponse
S1_SETUP_RESPONSE_HEX = "20110025000003003d400a03807372736d6d6530310069000b000000f11000000100001a00574001ff"


def is_s1setup_request(data):
    """
    Very basic decoder: checks if the incoming S1AP PDU is an initiatingMessage
    with procedureCode == 17 (S1SetupRequest)
    """
    if len(data) < 20:
        return False

    # Find procedureCode value from the message.
    # This is a very rough approach and assumes:
    # - The S1AP PDU starts at byte 0
    # - The procedureCode is stored in the TLV after offset ~12–16
    try:
        # Locate `procedureCode`, usually at byte 2–4 of the actual payload
        # Here we search for byte value 0x11 (17 decimal) — S1SetupRequest
        return b'\x11' in data[:40]
    except:
        return False

def run_fake_mme():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BIND_IP, PORT))
    print(f"🕵 Fake MME listening on {BIND_IP}:{PORT} 🕵")

    while True:
        data, addr = sock.recvfrom(2048)
        # print(f"👀 Received S1 message from {addr}, {len(data)} bytes 👀")

        if is_s1setup_request(data):
            print("    👀 Detected S1SetupRequest 👀")
            response = bytes.fromhex(S1_SETUP_RESPONSE_HEX)
            sock.sendto(response, addr)
            print("    🏃‍♂️ Sent S1SetupResponse 🏃‍♂️")
        # else:
            # print("    [x] Ignored non-S1SetupRequest")

if __name__ == "__main__":
    run_fake_mme()

import socket

FAKE_AMF_HOST = "10.55.1.100"
FAKE_AMF_PORT = 38412  # NGAP port

def start_fake_amf():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((FAKE_AMF_HOST, FAKE_AMF_PORT))
        s.listen()
        print(f"🕵 [FAKE-AMF] Listening on {FAKE_AMF_HOST}:{FAKE_AMF_PORT} 🕵")

        conn, addr = s.accept()
        with conn:
            print(f"👀 [FAKE-AMF] Connection from {addr} 👀")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                print(f"📡 [FAKE-AMF] Received ({len(data)} bytes): {data.hex()} 📡")
            print("[FAKE-AMF] Connection closed")

if __name__ == "__main__":
    start_fake_amf()

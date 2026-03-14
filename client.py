import socket
import json
import struct
from utils import encode_message, decode_message
import threading
import random


def client(host, port, method, a, b):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((host, port))

        while True:
            try:
                # Send Request
                data = {}

                data["method"] = method
                data["params"] = [a, b]

                req = encode_message(data)
                
                conn.send(req)

                #Receive Response

                response = json.loads(decode_message(conn).decode())

                print(f"Result: {response["result"]}")
                print(f"Error: {response["error"]}")

                
            except KeyboardInterrupt:
                print("Stopped...")
                break

def worker(host, ports, methods):
    while True:
        port = random.choice(ports)
        method = random.choice(methods)

        a = random.randint(1, 100)
        b = random.randint(1, 100)

        client(host, port, method, a, b)

def main():
    host = "127.0.0.1"
    ports = [5000, 5001, 5002, 5003]
    methods = ["add", "sub", "mul", "div"]

    threads = []

    for _ in range(10):   # 10 parallel clients
        t = threading.Thread(
            target=worker,
            args=(host, ports, methods)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
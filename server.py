import socket
import struct
import json
from utils import decode_message, encode_message
import multiprocessing

def add(a,b):
    a = int(a)
    b = int(b)
    return int(a+b)

def sub(a,b):
    a = int(a)
    b = int(b)
    return int(a-b)

def mul(a,b):
    a = int(a)
    b = int(b)
    return int(a*b)

def div(a,b):
    a = int(a)
    b = int(b)
    return int(a/b)

function_catalog ={
    "add":add,
    "sub":sub,
    "mul":mul,
    "div":div
}

def server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        print("Address:", addr)

        while True:
            try:
                # Receive Request
                data = decode_message(conn)

                if not data:
                    break

                message = json.loads(data.decode())
                print(message)
                 
                method = message["method"]
                params = message["params"]

                

                # Send Response
                response = {}
                try:
                    result = function_catalog[method](*params)
                    response["result"] = result
                    response["error"] = None
                except Exception as err:
                    response["result"] = None
                    response["error"] = str(err)
                
                print(response)

                conn.send(encode_message(response))
                
            except KeyboardInterrupt:
                print("Stopping....")
                break

        conn.close()

def main():
    host = "127.0.0.1"
    ports = [5000, 5001, 5002, 5003]

    processes = []

    for port in ports:
        p = multiprocessing.Process(target=server, args=(host, port))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
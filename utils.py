import json
import struct
import socket


def recv_exact(conn, n):
    data = b''
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            return None
        data += chunk
    return data

def encode_message(data:dict):

    data_byte = json.dumps(data).encode()

    data_len = len(data_byte)

    header = struct.pack('!I', data_len)

    return header + data_byte

def decode_message(conn:socket.socket):

    header = recv_exact(conn, 4)

    if len(header) < 4:
        print("Invalid Header")
        return None

    length  = struct.unpack('!I', header)[0]

    data = recv_exact(conn, int(length))

    return data
    
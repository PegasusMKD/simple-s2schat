import socket
from old import ServerUnavailable
import pickle

class Client:

    def __init__(self, server_address, port, header_size):
        self.server_address = server_address
        self.port = port
        self.header_size=header_size

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            server_exists = sock.connect_ex((self.server_address, self.port))
            if server_exists != 0:
                raise ServerUnavailable.ServerUnavailable
            while True:
                full_msg = b""
                new_msg = True
                while True:
                    data = sock.recv(16)
                    if new_msg:
                        print(f"new message length: {data[:self.header_size]}")
                        msglen = int(data[:self.header_size])
                        new_msg = False

                    full_msg += data

                    if len(full_msg) - self.header_size == msglen:
                        print("full_msg received")
                        dataObj = pickle.loads(full_msg[self.header_size:])
                        print(dataObj)
                        new_msg = True
                        full_msg = b""

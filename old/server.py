import socket
import pickle


class Server:

    def __init__(self, server_address, port, header_size):
        self.server_address = server_address
        self.port = port
        self.header_size=header_size



    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.server_address, self.port))
            sock.listen(5)
            while True:
                conn, addr = sock.accept()
                print("Connected by", addr)

                msg = pickle.dumps([1,2,3,4,5,6])
                msg = bytes(f"{len(msg):<{self.header_size}}", 'utf-8') + msg

                conn.send(msg)

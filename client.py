import socket
from ServerUnavailable import ServerUnavailable
import errno
import msvcrt

class Client:

    def __init__(self, address, port, header_size):
        self.address = address
        self.port = port
        self.header_size = header_size

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        available = self.sock.connect_ex((self.address, self.port))
        if not available:
            raise ServerUnavailable

    def run(self):
        dataToSend = ''
        startingInput = True
        while dataToSend != "quit":
            try:
                try:
                    headerToDisplay = self.sock.recv(self.header_size)
                    if len(headerToDisplay) == self.header_size:
                        dataToDisplay = self.sock.recv(int(headerToDisplay.decode('utf-8')))
                        if dataToDisplay:
                            print(dataToDisplay.decode('utf-8'), flush=True)
                            msvcrt.putch(b" ")
                            msvcrt.putch(b">")
                            msvcrt.putch(b">")
                            msvcrt.putch(b" ")
                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK and e.errno != 10057:
                        print(e)
                        raise e


                if startingInput:
                    msvcrt.putch(b" ")
                    msvcrt.putch(b">")
                    msvcrt.putch(b">")
                    msvcrt.putch(b" ")
                    startingInput = False


                if msvcrt.kbhit() and not startingInput:
                    key = msvcrt.getche().decode('utf-8')

                    if key == '\b':
                        dataToSend = dataToSend[:-1]
                        # TODO: Fix problems with delete (on console display only!)
                    else:
                        dataToSend += key

                    if dataToSend and key == '\r':
                        headerToSend = f"{len(dataToSend):<{self.header_size}}".encode('utf-8')
                        dataToSendServer = headerToSend + dataToSend.encode('utf-8')
                        self.sock.send(dataToSendServer)
                        dataToSend = ''
                        startingInput = True

            except KeyboardInterrupt as e:
                raise e

        self.sock.close()
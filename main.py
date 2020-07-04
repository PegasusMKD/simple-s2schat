from client import Client
from server import Server

import sys

# TODO: Add headers to client and server :) (DONE)
# TODO: Implement nice cmd display of the messages (have it be actually real-time) (Functionally works, only problem is console output)
# TODO: Start implementing UPnP

address = "localhost"
port = 1235
header_size = 10

def main():
    try:
        print("Attempting to start as client...")
        _client = Client(address, port, header_size)
        _client.run()

    except KeyboardInterrupt:
        sys.exit()

    except:
        print("Starting you as the server...")
        _server = Server(address, port, header_size)

        main()


if __name__ == '__main__':
    main()
from old import client, server

addr = "127.0.0.1"
port = 8000
header_size=10

def tryClient():
    _client = client.Client(addr, port, header_size)
    _client.run()

try:
    print("Starting client...")
    tryClient()

except:
    print("Server down.\nStarting as background server...")
    _server = server.Server(addr, port, header_size)
    _server.run()

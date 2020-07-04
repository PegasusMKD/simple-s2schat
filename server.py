import asyncio, threading

class Server:

    def __init__(self, address, port, header_size):
        self.address = address
        self.port = port
        self.header_size = header_size
        self.clients = []
        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()

    async def getAsyncClients(self):
        i = 0
        while i < len(self.clients):
            yield self.clients[i]
            i+=1


    async def handler(self, reader, writer):
        if writer not in self.clients:
            self.clients.append(writer)

        dataReceived = ''
        while dataReceived != 'quit':
            headerReceived = await reader.read(self.header_size)
            if not len(headerReceived):
                try:
                    self.clients.remove(writer)
                    continue
                except ValueError:
                    continue

            dataReceived = await reader.read(int(headerReceived.decode("utf-8").strip()))

            if not dataReceived:
                continue

            async for client in self.getAsyncClients():
                client.write(headerReceived + dataReceived)
                await client.drain()

        writer.close()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(asyncio.start_server(self.handler, self.address, self.port))
        loop.run_forever()
import asyncio
import json


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        out_list = json.loads(data.decode())
        for item in out_list:
            print(item)

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


async def as_input():
    return input("What do?")


async def main(loop):
    while True:
        p_input = await as_input()
        message = json.dumps({"player_id": 1, "player_input": p_input})
        coro = loop.create_connection(
            lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888)
        await coro

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

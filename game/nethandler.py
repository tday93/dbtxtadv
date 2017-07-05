import asyncio
import json


class GameServer(asyncio.Protocol):

    def __init__(self, game):
        self.game = game
        super().__init__()

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = json.loads(data)
        reply = json.dumps(self.game.player_input(message))

        self.transport.write(reply.encode())

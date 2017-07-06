import urwid
import asyncio
import json


class ClientUI(urwid.Frame):

    PALLETE = [('reversed', urwid.BLACK, urwid.LIGHT_GRAY),
               ('normal', urwid.LIGHT_GRAY, urwid.BLACK),
               ('error', urwid.LIGHT_RED, urwid.BLACK),
               ('green', urwid.DARK_GREEN, urwid.BLACK),
               ('blue', urwid.LIGHT_BLUE, urwid.BLACK),
               ('magenta', urwid.DARK_MAGENTA, urwid.BLACK), ]

    def __init__(self):
        """
        flow widget above body (or None)
        self.header
        box widget for body
        self.body
        flow widget for below body (or None)
        self.footer = None
        """
        self.header = urwid.Text("TITLE")
        self.body = ListView()
        self.input = Input()
        self.c_caption = "What Do?"
        foot = urwid.Pile([urwid.AttrMap(urwid.Text(self.c_caption),
                                         'reversed'),
                           urwid.AttrMap(self.input, 'normal')])
        super().__init__(urwid.AttrWrap(self.body, 'normal'),
                         urwid.AttrWrap(self.header, 'reversed'),
                         foot)
        urwid.connect_signal(self.input, 'line_entered', self.on_line_entered)
        self.focus_position = 'footer'
        self.protocol = self.get_protocol(self)

    def loop(self):
        self.eloop = urwid.MainLoop(self)
        self.eloop.run()

    def on_line_entered(self, line):
        message = {"player_id": 1, "player_input": line}
        asyncio.ensure_future(self.send_to_server(message))
        self.aloop.run_forever()

    async def send_to_server(self, message):
        await self.protocol.send_message(message)

    def output(self, line, style=None):
        line = (style, line)
        self.body.add(line)

    def get_protocol(self, game):
        loop = asyncio.get_event_loop()
        self.aloop = loop
        coro = loop.create_connection(lambda: GameClientProtocol(loop, game),
                                      '127.0.0.1', 8888)
        _, proto = loop.run_until_complete(coro)
        return proto


class ListView(urwid.ListBox):

    def __init__(self, body=urwid.SimpleListWalker([]), max_size=500):
        super().__init__(body)
        self.max_size = max_size

    def add(self, line):
        was_on_end = self.get_focus()[1] == len(self.body)-1
        if self.max_size and len(self.body) > self.max_size:
            del self.body[0]
        self.body.append(urwid.Text(line))
        last = len(self.body)-1
        if was_on_end:
            self.set_focus(last, 'above')


class Input(urwid.Edit):

    signals = ['line_entered']

    def __init__(self, got_focus=None):
        super().__init__()

    def keypress(self, size, key):
        if key == 'enter':
            line = self.edit_text.strip()
            if line:
                urwid.emit_signal(self, 'line_entered', line)
            self.edit_text = u''
        else:
            urwid.Edit.keypress(self, size, key)


class GameClientProtocol(asyncio.Protocol):
    def __init__(self, loop, game):
        self.transport = None
        self.game = game
        self.loop = loop
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        asyncio.ensure_future(self._send_messages())

    def connection_made(self, transport):
        self.transport = transport
        self._ready.set()

    async def _send_messages(self):
        await self._ready.wait()
        while True:
            data = await self.queue.get()
            self.transport.write(json.dumps(data).encode())

    async def send_message(self, message):
        await self.queue.put(message)

    def data_received(self, data):
        message = json.loads(data.decode())
        self.game.output(message)
        self.loop.stop()

    def connection_lost(self, exc):
        self.loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: GameClientProtocol(loop),
                                  '127.0.0.1', 8888)

    c = ClientUI()
    c.loop()

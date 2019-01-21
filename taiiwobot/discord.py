import discord
from . import util

class Discord():
    def __init__(self, config):
        self.callbacks = []
        self.send_queue = []
        self.client = discord.Client()
        email = "Livecoding@llort.gq"
        password = "2Yl¼ñ_v{+Ö@#<YIh7oBæ2<r.I<M{¢fIMís5(.ÑA9^N0bB]z[609B0v\\Uú0}4Ð?p3"
        # message handler
        @self.client.event
        async def on_message(message):
            util.callback(self.callbacks["MESSAGE"], message)

        # moronic programming handler
        @self.client.event
        async def on_ready():
            while True:
                asyncio.sleep(1)
                for target, message in self.send_queue:
                    self.send_queue.remove((target, message))
                    await self.client.send_message(target, message)
        print ("hello")
        self.client.loop.create_task(self.connect(email, password))
        
    async def connect(self, email, password):
        while True:
            print("starting")
            await asyncio.sleep(1)
            await self.client.start(email, password)
    
    def msg(self, target, message):
        self.send_queue.append((target, message))

    # decoration handler
    def on(self, *commands):
        print("creating task")
        def handler(f):
            for command in commands:
                if command == "message":
                    self.add_callback(f, "MESSAGE")
                elif command == "join":
                    self.add_callback(f, "JOIN")
                elif command == "leave":
                    self.add_callback(f, "PART")
                elif command == "quit":
                    self.add_callback(f, "QUIT")
                elif command == "ping":
                    self.add_callback(f, "PING")
                elif command == "sent":
                    self.add_callback(f, "SENT")
        return handler


    # Adds a callback for every message recieved
    def add_callback(self, callback, *commands):
        for command in commands:
            if command not in self.callbacks:
                self.callbacks[command] = []
            self.callbacks[command].append(callback)

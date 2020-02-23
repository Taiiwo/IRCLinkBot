import socket
import time
import re

from . import util

class IRC:
    def __init__(self, config):
        missing_keys = util.missing_keys(["user", "nick", "host"], config)
        if missing_keys:
            quit("[E] Missing args: %s" % (', ').join(missing_keys))
        ssl = config['ssl'] if 'ssl' in config else True
        defaults = {
            "ident": "TaiiwoBot",
            "real_name": "TaiiwoBot",
            "ssl": ssl,
            "port": 6697 if ssl else 6667,
            "recv_amount": 256,
            "locale": "utf-8",
            "connection_timeout": 300
        }
        defaults.update(config)
        self.config = defaults
        self.callbacks = {
            "SENT": []
        }
        self.recv_log = []
        self.last_pulse = None

        self.login()

    def login(self):
        util.debug("[-] Connecting to server...")
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.config['connection_timeout'])
        while True:
            try:
                print(self.config['host'])
                self.connection.connect((self.config['host'], self.config['port']))
                if self.config['ssl']:
                    import ssl
                    self.connection = ssl.wrap_socket(self.connection)
                break
            except socket.timeout:
                util.debug("[E] Could not connect to server, trying again...")
                util.debug("[i] Check connection information if error persists")
                self.connection.close()
                time.sleep(5)
        self.send("NICK %s\r\n" % self.config['nick'])
        self.send("USER %s * %s %s\r\n" % (
            self.config['ident'],
            self.config['user'],
            self.config['real_name']
        ))
        if 'password' in self.config:
            self.msg("nickserv", "identify %s" % (self.config['password']))
        # check the server is alive forever
        util.thread(self.ECG)
        for channel in self.config['autojoin']:
            self.join(channel)
        # listen forever
        self.listen()

    def send(self, string):
        bytes = string.encode(self.config['locale'], 'ignore')
        self.connection.send(bytes)
        for callback in self.callbacks['SENT']:
            util.callback(callback, string)

    def msg(self, target, message):
        if type(message) == str:
            message = message.splitlines()
        for line in message:
            line = re.sub("[\r\n]+", " ", line)
            if line != "":
                self.send("PRIVMSG %s :%s\r\n" % (target, message))

    def join(self, channel):
        if channel[0] != "#":
            channel = "#" + channel
        self.send("JOIN %s\r\n" % channel)
        util.debug("[-] Joining %s" % channel)

    def on(self, *commands):
        def handler(f):
            for command in commands:
                if command == "message":
                    self.add_callback(f, "PRIVMSG")
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

    def recv(self):
        while True:
            recv = self.connection.recv(self.config['recv_amount'])
            # convert to str, stripping unknown unicode characters
            recv = recv.decode(self.config['locale'], "ignore")
            self.last_pulse = time.time()
            self.recv_log.append([recv, self.last_pulse])
            yield recv

    def listen(self):
        for block in self.recv():
            # if the server stops responding, it sends us a blank string
            if not block:
                self.reconnect()
                break
            for message in block.splitlines():
                message = self.format_message(message)
                if message: print(message)
                if message and message['command'] in self.callbacks:
                    util.callback(
                        self.callbacks[message['command']],
                        message
                    )

    # Monitors the pulse of the connection, and restarts if it dies
    def ECG(self):
        if not self.last_pulse:
            self.last_pulse = time.time()
        while True:
            if time.time() - self.last_pulse > 300:
                self.reconnect()
                break
            time.sleep(10)

    def format_message(self, raw_message):
        m = re.match(
            "^:([^!]*)!~?([^@]*)@([^\s]*)\s([^\s]*)\s([^\s:]*)\s?:?(.*)",
            raw_message
        )
        if m is None:
            return False
        return {
            "nick": m.group(1),
            "ident": m.group(2),
            "host": m.group(3),
            "command": m.group(4),
            "target": m.group(5),
            "message": m.group(6),
            "raw_message": raw_message,
            "timestamp": time.time()
        }
    def reconnect(self):
        self.connection.close()
        self.login()

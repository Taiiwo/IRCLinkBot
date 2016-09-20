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
        self.message_callbacks = []
        self.block_callbacks = []
        self.join_callbacks = []
        self.sent_callbacks = []
        self.recv_log = []

        self.login()

    def login(self):
        util.debug("[-] Connecting to server...")
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.config['connection_timeout'])
        while 1:
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
        # listen forever
        util.thread(self.listen)
        # check the server is alive forever
        util.thread(self.ECG)
        for channel in self.config['autojoin']:
            self.join(channel)

    def send(self, string):
        bytes = string.encode(self.config['locale'], 'ignore')
        self.connection.send(bytes)
        util.callback(self.sent_callbacks, string)

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
        util.callback(self.join_callbacks, channel)

    # Adds a callback for every message recieved
    def add_message_callback(self, callback):
        self.message_callbacks.append(callback)

    # Adds a callback for each channel joined
    def add_join_callback(self, callback):
        self.join_callbacks.append(callback)

    # Adds a callback for each message sent
    def add_sent_callback(self, callback):
        self.sent_callback.append(callback)

    # Adds a callback for every block of lines recieved
    def add_block_callback(self, callback):
        self.block_callbacks.append(callback)

    def recv(self):
        while 1:
            recv = self.connection.recv(self.config['recv_amount'])
            # convert to str, stripping unknown unicode characters
            recv = recv.decode(self.config['locale'], "ignore")
            print(recv)
            self.last_pulse = time.time()
            self.recv_log.append([recv, self.last_pulse])
            yield recv

    def listen(self):
        for block in self.recv():
            # if the server stops responding, it sends us a blank string
            if block == "":
                self.reconnect()
                break
            util.callback(self.block_callbacks, block)
            for message in block.splitlines():
                message = self.format_message(message)
                util.callback(self.message_callbacks, message)

    # Monitors the pulse of the connection, and restarts if it dies
    def ECG(self):
        try:
            self.last_pulse
        except AttributeError:
            self.last_pulse = time.time()
        while 1:
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

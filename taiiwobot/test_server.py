import socket
import time
import re

from . import util

"""
 * Server for testing plugins
"""
class TestServer:
    def __init__(self, config):
        missing_keys = util.missing_keys([], config)
        if missing_keys:
            quit("[E] Missing args: %s" % (', ').join(missing_keys))
        defaults = {
            "user": "TaiiwoTest",
            "nick": "TaiiwoTest"
        }
        defaults.update(config)
        self.config = defaults
        self.callbacks = {
            "SENT": []
        }
        # a list of callbacks waiting for responses to specific users in specific locations
        # format {"location:username": [time_set, callback_function, timeout]}
        self.message_callbacks = {}

    def start(self):
        # listen forever
        self.listen()

    def msg(self, target, message, embed=None, reactions=tuple(), user=None, callback=None):
        print("%s>%s: %s"% (self.config["user"], target, message))

    def join(self, channel):
        if channel[0] != "#":
            channel = "#" + channel
        self.send("JOIN %s\r\n" % channel)
        util.debug("[-] Joining %s" % channel)

    def on(self, *commands):
        def handler(f):
            for command in commands:
                if command == "message":
                    self.add_callback(f, "message")
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

    # removes an even handler
    def off(self, f, command):
        if command in self.callbacks:
            self.callbacks[command].remove(f)

    def trigger(self, event, *data):
        if event in self.callbacks:
            try:
                util.callback(self.callbacks[event], *data)
            except util.RuntimeError as e:
                print(e.text)

    # Adds a callback for every message recieved
    def add_callback(self, callback, *commands):
        for command in commands:
            if command not in self.callbacks:
                self.callbacks[command] = []
            self.callbacks[command].append(callback)

    def menu(self, target, user, question, answers=None, ync=None, cancel=False):
        self.msg("JohnTester", "This would be a menu: %s\nanswers: %s\nync: %s" % (
            question, answers, ync
        ))

    def prompt(self, target, user, prompt, handler, cancel=False, timeout=60.0):
        self.msg("JohnTester", "This would be a prompt: %s" % (
            prompt
        ))
        self.message_callbacks[target + ":" + user] = [time.time(), handler, timeout]

    def listen(self):
        while True:
            message = input("JohnTester: ")
            message = self.format_message(message)
            # for each message callback
            for callback_id, callback in self.message_callbacks.copy().items():
                # are we waiting for this message?
                if callback_id == message.target + ":" + message.author_id:
                    # run the message callback
                    callback[1](message)
                    del self.message_callbacks[callback_id]
                    break
                timeout = callback[2] if len(callback) > 2 else 60.0
                # check if the message callback is too old
                if time.time() - callback[0] > timeout:
                    # remove the message callback
                    del self.message_callbacks[callback_id]
            self.trigger("message", message)

    def format_message(self, raw_message):
        return util.Message(
            nick="JohnTester",
            username="JohnTester",
            author_id="JohnTester",
            target="TaiiwoTest",
            host="JohnHost",
            type="message",
            content=raw_message,
            raw_message=raw_message,
            timestamp=time.time(),
            ident="JohnIdent"
        )

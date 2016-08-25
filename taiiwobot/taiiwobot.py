import os
import time
import importlib.machinery
from . import util, irc, config

class TaiiwoBot:
    def __init__(self):
        # get the config
        self.config = config.get_config()
        # connect to IRC
        self.irc = irc.IRC(self.config['server_config'])
        # add our message handler
        self.irc.add_message_callback(self.message_handler)
        # A list of message callbacks
        self.on_message_callbacks = []

    def load_plugins(self):
        # get all the plugins from the plugin folder
        plugins = []
        for root, dirs, files in os.walk('plugins'):
            for file in files:
                # import the plugin as a library
                plugin = importlib.machinery.SourceFileLoader('Plugin',os.path.join(root,file)).load_module()
                # initialize the plugin
                plugin.Plugin(self)
        return plugins

    # Handlers for IRC events

    def message_handler(self, message):
        for callback in self.on_message_callbacks:
            callback(message)

    # Decorators

    def on_message():
        def add_callback(f):
            self.on_message_callbacks.append(f)
        return add_callback

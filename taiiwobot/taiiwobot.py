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
                if file[-3:] == ".py":
                    plugin = __import__(os.path.join(root, file[:-3]).replace('/', '.'))
                    plugin = getattr(plugin, file[:-3])
                    plugins.append(plugin.Plugin(self.irc))
        return plugins

    # Handlers for IRC events

    def message_handler(self, message):
        if message:
            for plugin in self.plugin_list:
                plugin.on_message(message)

    # Decorators

    def on_message():
        def add_callback(f):
            self.on_message_callbacks.append(f)
        return add_callback

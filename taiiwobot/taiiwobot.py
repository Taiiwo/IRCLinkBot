import os
import importlib.machinery
from . import util, irc, config

class TaiiwoBot:
    def __init__(self):
        self.config = config.get_config()
        self.irc = irc.IRC(self.config['server_config'])
        self.plugin_list = self.load_plugins()
        self.irc.add_message_callback(self.message_handler)

    def load_plugins(self):
        plugins = []
        for root, dirs, files in os.walk('plugins'):
            for file in files:
                if file[-3:] == ".py":
                    plugin = __import__(os.path.join(root, file[:-3]).replace('/', '.'))
                    plugin = getattr(plugin, file[:-3])
                    plugins.append(plugin.Plugin(self.irc))
        return plugins

    def message_handler(self, message):
        if message:
            for plugin in self.plugin_list:
                plugin.on_message(message)

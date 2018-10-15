import os
import time
import importlib.machinery
from . import util, config

class TaiiwoBot:
    def __init__(self, server, config):
        self.server = server
        self.config = config
        self.on = server.on
        self.msg = server.msg
        self.util = util
        # load our plugins
        self.plugins = self.load_plugins()
        # run the blocking function
        self.server.start()


    def load_plugins(self):
        # get all the plugins from the plugin folder
        plugins = []
        for root, dirs, files in os.walk('plugins'):
            for file in files:
                if file[-3:] == ".py":
                    plugin = __import__(
                        os.path.join(root, file[:-3]).replace('/', '.')
                    )
                    plugin = getattr(plugin, file[:-3])
                    plugin = plugin.Plugin(self)
                    plugins.append(plugin)
        return plugins

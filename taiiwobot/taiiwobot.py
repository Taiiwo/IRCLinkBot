import os
import time
from . import util, config

class TaiiwoBot:
    def __init__(self, server, config):
        self.server = server
        self.config = config
        self.on = server.on
        # load our plugins
        # note, we don't actually need to do anything with them as they add their own callbacks to stuff
        self.load_plugins()

    def load_plugins(self):
        # get all the plugins from the plugin folder
        plugins = []
        for root, dirs, files in os.walk('plugins'):
            for file in files:
                if file[-3:] == ".py":
                    plugin = __import__(
                        os.path.join(root, file[:-3]).replace('/', '.')
                    )
                    plugin.Plugin()
                    #module = getattr(plugin, file[:-3])
        return plugins
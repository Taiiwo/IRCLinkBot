import os
import time
import importlib.machinery
<<<<<<< HEAD
from . import util, config, plugin
=======
from . import util, config
>>>>>>> dc83748e2cbac802a5b33d8c442e93a5e791d745

class TaiiwoBot:
    def __init__(self, server, config):
        self.server = server
        self.config = config
        # expose server functions
        self.on = server.on
        self.msg = server.msg
        self.menu = server.menu
        self.prompt = server.prompt
        self.util = util
        # load our plugins
        self.plugins = self.load_plugins()
        # run the blocking function
        self.server.start()

    def load_plugins(self):
        # get all the plugins from the plugin folder
        plugins = []
        for root, dirs, files in os.walk('plugins'):
            # for each py file in the plugins folder
            for file in files:
                if file[-3:] == ".py":
                    # import it
                    plugin = __import__(
                        os.path.join(root, file[:-3]).replace('/', '.').replace("\\", ".")
                    )
                    plugin = getattr(plugin, file[:-3])
<<<<<<< HEAD
                    # find all the plugin classes
                    for attr in dir(plugin):
                        # ignore the _ attrs for safety
                        if attr[0] == "_":
                            continue
                        # if the attr is a unintitialized class
                        if isinstance(getattr(plugin, attr), type):
                            # if the class is based on the plugin class
                            if getattr(plugin, attr).__bases__[0] == plugin.Plugin:
                                # init the class and add it to the plugin list
                                plugins.append(getattr(plugin, attr)(self))
                                break
=======
                    plugin = plugin.Plugin(self)
                    plugins.append(plugin)
>>>>>>> dc83748e2cbac802a5b33d8c442e93a5e791d745
        return plugins

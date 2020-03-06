import os
import inspect

from taiiwobot.plugin import Plugin


class Reload(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "reload", "Reloads a plugin's code for dev purposes", [], self.reload
        ).listen()

    def reload(self, message, query):
        for plugin in self.bot.plugins:
            if type(plugin).__name__.lower() == query.lower():
                # unload plugin
                plugin_name = type(plugin).__name__
                plugin.unload()
                self.bot.plugins.remove(plugin)
                self.bot.msg(message.target, "Plugin unloaded..")
                # load the plugin
                for root, dirs, files in os.walk('plugins'):
                    # for each py file in the plugins folder
                    for file in files:
                        if file[-3:] == ".py" and file[:-3].lower() == query.lower():
                            # import it
                            namespace = {}
                            with open(os.path.join(root, file)) as plugin_file:
                                code = compile(
                                    plugin_file.read(),
                                    os.path.join(root, file),
                                    "exec"
                                )
                                exec(code, namespace)
                            plugin = namespace[plugin_name]
                            # init the class and add it to the plugin list
                            self.bot.plugins.append(plugin(self.bot))
                            self.bot.msg(message.target, "Plugin loaded!")
                            return

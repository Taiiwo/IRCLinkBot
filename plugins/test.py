from taiiwobot.plugin import PluginBase

class Plugin(PluginBase):
    def on_message(self, message):
        print(message)


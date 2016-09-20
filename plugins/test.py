from taiiwobot.plugin import PluginBase

class Plugin(PluginBase):
    @self.bot.on_message()
    def on_message(message):
        print("message")

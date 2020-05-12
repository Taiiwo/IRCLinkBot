from taiiwobot.plugin import Plugin

class Help(Plugin):
    def __init__(self, bot):
        self.bot = bot

        self.bl = ["template", "example", "reload"]

        self.interface = bot.util.Interface(
            "help", # command name
            # plugin description
            "Displays help info on how to use the bot", [],
            self.help # main function
        ).listen() # sets the on message callbacks and parses messages

    def help(self, message, *args):
        plugin_list = ""
        for plugin in self.bot.plugins:
            if not hasattr(plugin, "interface"):
                continue
            interface = plugin.interface
            if interface.name in self.bl:
                continue
            plugin_list += "%s%s - %s\n" % (
                interface.prefix,
                interface.name,
                interface.desc,
            )

        self.bot.msg(
            message.target,
            self.bot.server.code_block(
                "Bot Help menu\n"
                + "-------------\n"
                + "Below is a list of all the commands available. Type '<command> help' "
                + "for more information on a specific command, including subcommands "
                + "and flag info. Flag values with spaces in can be submitted like '--flag=\"flag value\"'. "
                + "Args in [] are optional, Args in <> are mandatory.\n\n"
                + plugin_list
            ),
        )

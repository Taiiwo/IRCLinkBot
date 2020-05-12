from taiiwobot.plugin import Plugin

class Test(Plugin):
    def __init__(self, bot):
        print("test plugin init")
        self.bot = bot
        self.interface = bot.util.Interface(
            "test",
            "This command does some action",
            [
                "o output Specifies the location of the output file 1",
                "f force Forces the action 0",
                "q quiet Does the action quietly 0"
            ],
            self.some_func,
            subcommands=[
                bot.util.Interface(
                    "add",
                    "adds some stuff",
                    [
                        "f force Force adding the thing 0"
                    ],
                    self.add
                )
            ]
        ).listen()

    def some_func(self, message, output="output", force=False, quiet=False):
        print("test running")
        self.bot.msg(message.target, "%s %s %s" % (output, force, quiet))

    def add(self, force=False):
        pass

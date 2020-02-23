from taiiwobot.plugin import Plugin

class Test(Plugin):
    def __init__(self, bot):
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
                    "say",
                    "says some stuff",
                    [
                        "f force Force adding the thing 0"
                    ],
                    self.say
                )
            ]
        ).listen()

    def some_func(self, message, output="output", force=False, quiet=False):
<<<<<<< HEAD
        print(message.target)
=======
>>>>>>> dc83748e2cbac802a5b33d8c442e93a5e791d745
        self.bot.prompt(message.target, message.author_id,
            "This is an example prompt: ",
            lambda m: self.bot.msg(message.target, "Hello, " + m.content)
        )

    def say(self, message, *things, force=False):
        print("weed")
        self.bot.msg(message.target, " ".join(things))

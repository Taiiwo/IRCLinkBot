from taiiwobot.plugin import Plugin

class Example(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "example", # plugin name
            "This is a demo plugin you can use to learn how plugins work", # plugin description
            [ # Flags: <short form> <long form> <description> <1=string or 0=bool>
            # these will be loaded as kwargs to your main function
                "o output Specifies the location of the output file 1",
                "f force Forces the action 0",
                "q quiet Does the action quietly 0"
            ],
            self.some_func, # main function
            subcommands=[ # list of subcommands
                bot.util.Interface(
                    "sub", # invoked with $template sub <args/flags>
                    "says some stuff", # subcommand description
                    [ # subcommand flags
                        "f force Force adding the thing 0"
                    ],
                    self.say # subcommand function
                )
            ]
        ).listen() # sets the on message callbacks and parses messages

    # flags are parsed and passed to the assigned function like so:
    # *args catches all uncaught command arguments as an array.
    def some_func(self, message, *args, output="output", force=False, quiet=False):
        # asks the user for some text, runs the handler function with
        # their response
        self.bot.prompt(message.target, message.author_id,
            "This is an example prompt: ",
            lambda m: self.bot.msg(message.target, "Hello, " + m.content)
        )

    def say(self, message, *things, force=False):
        # sends a message to the channel it came from
        self.bot.msg(message.target, " ".join(things))

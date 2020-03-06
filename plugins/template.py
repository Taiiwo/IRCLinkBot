from taiiwobot.plugin import Plugin

class Template(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "template", # command name
            # plugin description
            "This is a template plugin you can use to base you own plugins off.",
            [ # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main, # root function
            subcommands=[ # list of subcommands
                bot.util.Interface(
                    "sub", # invoked with $template sub <args/flags>
                    "says some stuff", # subcommand description
                    [], # subcommand flags
                    self.sub # subcommand function
                )
            ]
        ).listen() # sets the on message callbacks and parses messages

    def main(self, message, *args, output="output"): # include your root flags here
        # asks the user for some text, runs the handler function with
        # their response
        self.bot.prompt(message.target, message.author_id,
            "This is an example prompt: ",
            lambda m: self.bot.msg(message.target, "Hello, " + m.content)
        )

    def sub(self, message, *things, force=False): # include sub flags here
        # sends a message to the channel it came from
        self.bot.msg(message.target, " ".join(things))

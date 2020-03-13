from taiiwobot.plugin import Plugin

import lib.cicada.cicada
from lib.cicada.cicada.gematria import Latin, Runes, Number

cicada = lib.cicada.cicada
Gematria = cicada.gematria.Gematria


class Gematria(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.lp = cicada.LiberPrimus()
        self.interface = bot.util.Interface(
            "gm",  # command name
            # plugin description
            "translates runes and latin using the Gematria Primus.",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main,  # root function
            subcommands=[  # list of subcommands
                bot.util.Interface(
                    "runes",  # invoked with $template sub <args/flags>
                    "Translates string to runes Args: <string>",  # subcommand description
                    [
                        "n numeric From numeric form 0",
                        "a atbash Perform atbash 0",
                    ],  # subcommand flags
                    self.runes,  # subcommand function
                ),
                bot.util.Interface(
                    "latin",  # invoked with $template sub <args/flags>
                    "Translates string to latin Args: <string>",  # subcommand description
                    [
                        "n numeric From numeric form 0",
                        "a atbash Perform atbash 0",
                    ],  # subcommand flags
                    self.latin,  # subcommand function
                ),
            ],
        ).listen()  # sets the on message callbacks and parses messages

    def main(self, message, *args):  # include your root flags here
        self.interface.help(message.target, self)

    def runes(self, message, *args, numeric=False, atbash=False):
        string = " ".join(args)
        if numeric:
            input = Number(string)
        else:
            input = Latin(string)

        if atbash:
            alpha = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
            runes = input.to_runes().substitute(alpha, alpha[::-1])
        else:
            runes = input.to_runes().text
        self.bot.msg(message.target, self.bot.server.code_block(runes))

    def latin(self, message, *args, numeric=False, atbash=False):
        string = " ".join(args)
        if numeric:
            input = Number(string).to_runes()
        else:
            input = Runes(string)

        if atbash:
            alpha = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
            latin = Runes(input.substitute(alpha, alpha[::-1])).to_latin().text
        else:
            latin = input.to_latin().text
        self.bot.msg(message.target, self.bot.server.code_block(latin))

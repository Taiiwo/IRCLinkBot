from taiiwobot.plugin import Plugin

import lib.cicada.cicada

cicada = lib.cicada.cicada
Gematria = cicada.gematria.Gematria


class LiberPrimus(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.lp = cicada.LiberPrimus()
        self.interface = bot.util.Interface(
            "lp",  # command name
            # plugin description
            "Retrieves and translates pages of the Liber Primus. Args: <page_number>",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                "l latin returns the page in latin form 0",
                "n number returns the page in number form 0",
                "b book Select book 1 or 2 1",
            ],
            self.page,  # root function
            subcommands=[  # list of subcommands
                bot.util.Interface(
                    "page",  # invoked with $template sub <args/flags>
                    "Retrieves and translates pages of the Liber Primus. Args: <page_number>",
                    [
                        "l latin returns the page in latin form 0",
                        "n number returns the page in number form 0",
                        "b book Select book 1 or 2 1",
                    ],  # subcommand flags
                    self.page,  # subcommand function
                )
            ],
        ).listen()  # sets the on message callbacks and parses messages

    def main(self, message, *args):  # include your root flags here
        self.interface.help(message.target, self)

    def page(self, message, page_number, *args, latin=False, number=False, book="2"):
        if book.isnumeric():
            book = int(book)
        else:
            raise self.bot.util.RuntimeError(
                "Invalid book number", message.target, self
            )
        if page_number.isnumeric():
            page_number = int(page_number) - 1
        else:
            raise self.bot.util.RuntimeError(
                "Invalid page number", message.target, self
            )
        if (
            page_number < 0
            or (page_number > 14 and book == 1)
            or (page_number > 56 and book == 2)
        ):
            print(page_number)
            raise self.bot.util.RuntimeError(
                "Invalid page number", message.target, self
            )
        page = self.lp.pages[(16 if book == 2 else 0) + int(page_number)]
        if latin:
            page = page.to_latin()
        if number:
            page = page.to_number()
        self.bot.msg(message.target, self.bot.server.code_block(page.text))

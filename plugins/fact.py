from taiiwobot.plugin import Plugin

import requests
from bs4 import BeautifulSoup


class Fact(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "fact",  # command name
            # plugin description
            "Dispenses a random fact",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main,  # root function
            subcommands=[],
        ).listen()  # sets the on message callbacks and parses messages

    def main(self, message, *args, output="output"):  # include your root flags here
        html = requests.get("http://randomfunfacts.com/").text
        selector = "strong > i"
        soup = BeautifulSoup(html, "html.parser")
        fact = soup.select(selector)[0].getText()
        self.bot.msg(message.target, fact)

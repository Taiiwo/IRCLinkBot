from taiiwobot.plugin import Plugin

import requests
import random
import time
from bs4 import BeautifulSoup


class WYR(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.reacted = time.time() - 60
        self.interface = bot.util.Interface(
            "wyr",  # command name
            # plugin description
            "Random 'Would you rather' question",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main,  # root function
            subcommands=[],  # list of subcommands
        ).listen()  # sets the on message callbacks and parses messages

    def set_reacted(self, r):
        if r["reactor"] != self.bot.server.me():
            self.reacted = time.time() - 60

    def main(self, message, *args, output="output"):  # include your root flags here
        i = 0
        if time.time() - self.reacted < 60:
            print(time.time() - self.reacted)
            self.bot.msg(
                message.target, "You must react before requesting more questions!"
            )
            return
        while i < 10:
            i += 1
            # this website conveniently puts the whole question in the page title
            rand = str(random.randint(255150, 256442))
            print(rand)
            r = requests.get("http://www.rrrather.com/view/" + rand)
            # get page title
            soup = BeautifulSoup(r.content, "html.parser")
            title = soup.find("title")
            if len(r.history) > 1:
                print(title, r.history)
                continue
            self.reacted = time.time()
            self.bot.msg(
                message.target,
                title.string,
                reactions=[["1⃣", self.set_reacted], ["2⃣", self.set_reacted],],
                user=message.author,
            )
            return
        self.bot.msg(
            message.target,
            "There seems to be something wrong with the API. Please try again later.",
        )

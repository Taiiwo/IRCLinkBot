from taiiwobot.plugin import Plugin

import requests
import random
import time
import json


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
        wyr = json.loads(requests.get("http://www.rrrather.com/botapi").text)
        question = " ".join([wyr["title"], wyr["choicea"], "or", wyr["choiceb"] + "?"])
        self.reacted = time.time()
        self.bot.msg(
            message.target,
            question,
            reactions=[["1⃣", self.set_reacted], ["2⃣", self.set_reacted],],
        )

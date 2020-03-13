from taiiwobot.plugin import Plugin

import requests
import json


class CicadaWiki(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "uc",  # command name
            # plugin description
            "Searches a query on the UncoveringCicada wiki.",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main,  # root function
            subcommands=[],
        ).listen()  # sets the on message callbacks and parses messages

    def main(self, message, *args):  # include your root flags here
        query = "%20".join(args)
        wikiajson = requests.get(
            "http://uncovering-cicada.wikia.com/api/v1/Search/List?query=" + query
        ).text
        wikiaobj = json.loads(wikiajson)
        title = wikiaobj["items"][0]["title"]
        tiny = self.bot.util.maketiny(wikiaobj["items"][0]["url"])
        self.bot.msg(message.target, title + " - " + tiny)

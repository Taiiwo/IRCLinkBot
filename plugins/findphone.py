from taiiwobot.plugin import Plugin

import re
import requests
import json


class FindPhone(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "findphone",  # command name
            # plugin description
            "Looks up a phone number on the OpenCNAM Database. Args: <phone_number>",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main,  # root function
            subcommands=[],
        ).listen()  # sets the on message callbacks and parses messages

    def main(self, message, number, *args):  # include your root flags here
        if re.match("\d{9,11}", number):
            try:
                jsonres = requests.get(
                    "https://api.opencnam.com/v2/phone/+"
                    + str(number)
                    + "?format=json&account_sid=ACe3213058aed64072b21c1aad690d10f5&auth_token=AU8d8f41d2a4ae42b09cd9356dc71db3b4"
                ).text
            except:
                self.bot.msg(message.target, "No information found")
                return
            parsedjson = json.loads(jsonres)
            toSend = "CallerID: %s; Last Updated: %s; Date Created: %s;" % (
                parsedjson["name"],
                parsedjson["updated"],
                parsedjson["created"],
            )
            self.bot.msg(message.target, self.bot.server.code_block(toSend))
        else:
            self.bot.msg(
                message.target,
                "That doesn't look like a valid phone number. Please match `\d{9,11}`",
            )

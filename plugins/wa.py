import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import html
import re
from taiiwobot.plugin import Plugin


class WA(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "wa",
            "Searches wolfram alpha. Args: <search_query>",
            ["q quiet responds with only one line of output 0"],
            self.wa,
        ).listen()

    def wa(self, message, *args, quiet=False):
        # URL escape query
        query = {"input": " ".join(args), "appid": "QPEPAR-TKWEJ3W7VA"}
        baseUrl = "http://api.wolframalpha.com/v2/query?"
        response = requests.get(baseUrl, params=query).text
        soup = BeautifulSoup(response, "html.parser")
        pods = soup.queryresult.findAll("pod")
        if pods and len(pods) >= 2:  # if we got an answer
            answers = []
            # Iterate the results
            for pod in pods:
                # Grab plaintext of the result
                answer = pod.subpod.plaintext.string
                if answer == None:
                    continue
                # Strip html entities from the response
                answer = html.unescape(str(answer))
                for match in re.finditer(r"\\:([a-f|A-F|0-9]{4})", answer):
                    # Replace it with its corresponding Unicode character
                    try:
                        answer = answer.replace(
                            match.group(0), unichr(int(match.group(1), 16))
                        )
                    except:
                        pass
                answers.append(answer)
            # Prepare these answers for IRC
            ircAnswersString = ""
            lines = "\n".join(answers).splitlines()
            postShortLink = False
            if len(lines) > 5:
                lines = lines[:5]
                postShortLink = True
            if quiet:
                lines = lines[:2]
                postShortLink = False
            for line in lines:
                if len(line) > 430:
                    ircAnswersString += "".join(line[:427]) + "...\n"
                else:
                    ircAnswersString += line + "\n"
            self.bot.msg(message.target, self.bot.server.code_block(ircAnswersString))
            if postShortLink:
                shortLink = self.bot.util.maketiny(
                    "http://www.wolframalpha.com/input/?"
                    + urlencode({"i": " ".join(args)})
                )
                self.bot.msg(message.target, "More: " + shortLink)
        else:
            """
            # We didn't get an answer, make cleverbot reply instead
            # Construct the string that makes the cleverbot plugin respond
            cleverBotFlag = self.bot.server.name + ": "
            # emulate how cleverbot would have been run if invoked normally
            message.content = message.content.replace("$wa ", cleverBotFlag)
            self.bot.server.trigger("message", message)
            """
            self.bot.msg(message.target, "No data available.")

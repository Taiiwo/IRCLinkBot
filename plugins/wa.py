import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
import html
import re
from taiiwobot.plugin import Plugin


class WA(Plugin):
    def __init__(self, bot):
        self.bot = bot

        self.conversations = {}

        self.interface = bot.util.Interface(
            "wa",
            "Searches wolfram alpha. Args: <search_query>",
            ["q quiet responds with only one line of output 0"],
            self.wa,
            subcommands=[
                bot.util.Interface(
                    "report",
                    "Generates a visual report on the query",
                    [],
                    self.report
                )
            ]
        ).listen()

    def api(self, query, baseurl="http://api.wolframalpha.com/v2/query?"):
        query.update({"appid": "QPEPAR-TKWEJ3W7VA"})
        return requests.get(baseurl, params=query)

    def wa(self, message, *args, quiet=False):
        query = {"i": " ".join(args)}
        if message.target in self.conversations:
            query.update(self.conversations[message.target])
        baseUrl = "http://api.wolframalpha.com/v1/conversation.jsp?"
        response = json.loads(self.api(query, baseurl=baseUrl).text)

        if "error" in response:
            if message.target in self.conversations:
                # delete the conversation id and try again
                del self.conversations[message.target]
                return self.wa(message, *args)
            return self.bot.msg(message.target, response["error"])
        self.bot.msg(message.target, response["result"])
        self.conversations[message.target] = {
            "conversationid": response["conversationID"]
        }
        if "s" in response:
            self.conversations[message.target]["s"] = response["s"]
        elif "s" in self.conversations[message.target]:
            del self.conversations[message.target]["s"]

    def report(self, message, *args, quiet=False):
        # URL escape query
        query = {"input": " ".join(args), "appid": "QPEPAR-TKWEJ3W7VA"}
        baseUrl = "http://api.wolframalpha.com/v2/query?"
        response = requests.get(baseUrl, params=query).text
        soup = BeautifulSoup(response, "html.parser")
        pods = soup.queryresult.findAll("pod")
        if pods and len(pods) >= 2:  # if we got an answer
            answers = []
            images = []
            # Iterate the results
            for pod in pods:
                # Grab plaintext of the result
                answer = pod.subpod.plaintext.string
                if answer == None:
                    images.append([pod["title"], pod.subpod.img["src"]])
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
                answers.append([pod["title"], answer])
            # create an embed
            embed = self.bot.server.embed(
                title=answers[0][1],
                url="https://www.wolframalpha.com/input/?i=" + "%20".join(args),
                desc=answers[1][1],
                author_name="Wolfram Alpha",
                author_icon="https://writings.stephenwolfram.com/data/uploads/2018/12/wolfram-alpha-spikey-current-logo.png",
                author_link="https://wolframalpha.com",
                color="ff6c00",
                fields=[[f[0], "\n".join([", ".join(l.split("|")[:3]) for l in f[1].split("\n")[:4]]).strip(","), True] for f in sorted(answers[2:], key=lambda a:len(a[1]))]
            )
            self.bot.msg(message.target, " ", embed=embed)
            for image in images:
                self.bot.msg(message.target, "%s: %s" % (image[0], self.bot.util.maketiny(image[1])))
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

import feedparser
import pymongo
import time

class Plugin():
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "rss",
            "Posts RSS updates to a channel",
            [],
            self.root,
            subcommands=[
                bot.util.Interface(
                    "add",
                    "Adds an RSS feed to listen to. Usage: $rss add [flags] <url>",
                    [
                        "p ping Which users to ping for each update 1"
                    ],
                    self.add
                )
            ],
        ).listen()

        self.db = self.bot.util.get_db()
        self.feeds_col = self.db["rss_feeds"]
        self.default_settings = {
            "title": "$title",
            "desc": "$description",
            "footer": "published at $published",
            "url": "$link",
            "color": "0xbade83"
        }

    def root(self, message):
        #self.bot.msg(message.target, "%s %s %s" % (output, force, quiet))
        self.interface.help(message.target, self)

    def add(self, message, url=None, ping=""):
        if not url:
            raise self.bot.util.RuntimeError(
                "Missing argument: url. Usage: $rss add [flags] <url>",
                message.target, self
            )
        pings = [ping]
        target = message.target
        target = target if type(target) == str else target.id
        existing_feed = self.feeds_col.find_one({"url": url})
        if url[:7] not in ["https:/", "http://"]:
            raise self.bot.util.RuntimeError(
                "`url` must be a valid URL meaning it must start with http:// "
                "or https://",
                message.target, self
            )
        feed_sample = feedparser.parse(feed)
        if existing_feed:
            for destination in existing_feed["destinations"]:
                if target in destination["targets"]:
                    raise self.bot.util.RuntimeError(
                        "That feed is already being tracked in this channel! "
                        "To edit the way that feed is managed, type: `%s edit`"
                        "To remove that feed, type `%s remove <url>`" %
                        (self.prefix + self.name, self.prefix + self.name),
                        message.target, self
                    )
            feed = existing_feed
        else:
            feed = {
                "url": url,
                # TODO: potentially add a better way of identifying entries uniquely
                "unique_key": feed_sample["entries"][-1]["title"],
                "destinations": []
            }
        destination = {
            "target": target,
            "pings": pings,
            "keys": self.default_settings
        }
        format_key = lambda t: " ".join(feed_sample["entries"][-1][k[1:]]
                if k[0] == "$" else k for k in destination["keys"][t].split())
        # show the user a sample of the feed
        self.bot.msg(
            message.target,
            " ".join(destination["pings"]),
            embed=self.server.embed(
                title=format_key("title"),
                desc=format_key("desc"),
                footer=format_key("footer"),
                url=format_key("url"),
                color=format_key("color")
            )
        )
        def yes():
            feed["destinations"].append(destination)
            self.feeds_col.insert_one(feed)

        self.bot.menu(message.target, message.author,
            "Does this look okay?",
            ync=[yes, lambda:self.edit(message,url), lambda: None]
        )

    def loop(self):
        while True:
            for feed in self.feeds_col.find({}):
                f = feedparser.parse(feed["url"])
                # find out where the new entries start
                i = 0
                for entry in f["entries"]:
                    if feed["unique_key"] == entry["title"]:
                        break
                    i += 1
                # if there are no new entries
                if i+1 == len(f["entries"]):
                    # no new articles, go to next feed
                    continue
                elif i+1 > len(f["entries"]):
                    # we didn't find our title at all. Post all articles
                    i = -1
                # for each new entry
                for entry in f["entries"][i+1:]:
                    for destination in feed["destinations"]:
                        keys = self.default_settings \
                                if destination["keys"] == "default" \
                                else destination["keys"]
                        # turns a key format into value string
                        format_key = lambda t: " ".join(entry[k[1:]]
                                if k[0] == "$" else k for k in keys[t].split())
                        self.bot.msg(
                            destination["target"],
                            " ".join(destination["pings"]),
                            embed=self.server.embed(
                                title=format_key("title"),
                                desc=format_key("desc"),
                                footer=format_key("footer"),
                                url=format_key("url"),
                                color=format_key("color")
                            )
                        )

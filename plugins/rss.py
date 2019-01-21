import feedparser
import pymongo
import time
import re

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
                        "t target The target channel the feed updates will appear in 1",
                        "p pings Which users to ping for each update. Comma and/or space separated. 1",
                        'c conditions Filter keys with a regex. Eg: `-c="title:weather"` to only post entries with "weather" in the title 1'
                    ],
                    self.add
                ),
                bot.util.Interface(
                    "remove",
                    "Removes an RSS feed from the target channel. Usage $rss remove [flags] <url>",
                    [
                        "t target The target channel to delete the feeds from 1"
                    ],
                    self.delete
                ),
                bot.util.Interface(
                    "edit",
                    "Edits the way a feed is managed. Usage $rss edit [flags] <url>",
                    [
                        "t target The channel that contains the feed to be edited 1",
                        "d display Show the edit display menu 0"
                    ],
                    self.edit
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
            "thumbnail": None,
            "author_name": "$feed:title",
            "author_link": "$feed:link",
            "author_icon": None,
            "color": "0xbade83"
        }
        self.bot.util.thread(self.loop)

    def root(self, message):
        #self.bot.msg(message.target, "%s %s %s" % (output, force, quiet))
        self.interface.help(message.target, self)

    def add(self, message, url=None, target="", pings="", conditions=""):
        if not url:
            raise self.bot.util.RuntimeError(
                "Missing argument: url. Usage: $rss add [flags] <url>",
                message.target, self
            )
        # parse the input values
        pings = pings.replace(",", " ").split()
        conditions = re.split(r";\s?", conditions)
        conditions2 = []
        for condition_string in conditions:
            p = condition_string.split(":")
            conditions2.append({p[0]: p[1:]})
        conditions = conditions2
        target = target if target else message.target
        target = target if type(target) == str else target.id
        existing_feed = self.feeds_col.find_one({"url": url})
        if url[:7] not in ["https:/", "http://"]:
            raise self.bot.util.RuntimeError(
                "`url` must be a valid URL meaning it must start with http:// "
                "or https://",
                message.target, self
            )
        feed_sample = feedparser.parse(url)
        if len(feed_sample["entries"]) < 1:
            raise self.bot.util.RuntimeError(
                "This does not appear to be a valid feed. "
                "Feeds must have at least 1 entry.", message.target, self
            )
        if existing_feed:
            for destination in existing_feed["destinations"]:
                if target == destination["target"]:
                    raise self.bot.util.RuntimeError(
                        "That feed is already being tracked in this channel! "
                        "To edit the way that feed is managed, type: `%s edit`"
                        "To remove that feed, type `%s remove <url>`" %
                        (self.interface.prefix + self.interface.name,
                        self.interface.prefix + self.interface.name),
                        message.target, self
                    )
            feed = existing_feed
        else:
            feed = {
                "url": url,
                # TODO: potentially add a better way of identifying entries uniquely
                "unique_key": feed_sample["entries"][0]["title"],
                "destinations": []
            }
        destination = {
            "target": target,
            "pings": pings,
            "keys": "default",
            "conditions": conditions
        }
        entry = feed_sample["entries"][0]
        entry.update({"feed:"+k:v for k, v in feed_sample.items()})
        # post a sample of the feed
        self.post_entry(destination, entry)
        # callback function for if the user hits "yes" in the following menu
        def yes():
            # the user decided the feed looked good
            if existing_feed:
                # edit the existing feed
                self.feeds_col.update(existing_feed, {"$push": {
                    "destinations": destination
                }})
            else:
                # insert a new feed into the db
                feed["destinations"].append(destination)
                self.feeds_col.insert_one(feed)
        # ask the user if it needs editing
        self.bot.menu(message.target, message.author_id,
            "Does this look okay?",
            ync=[yes, lambda:self.edit(message,url), lambda: None]
        )

    def delete(self, message, url=None, target=None):
        if not url:
            raise self.bot.util.RuntimeError(
                "Missing argument: url. Usage: $rss delete [flags] <url>",
                message.target, self
            )
        target = target if target else message.target
        target = target if type(target) == str else target.id
        feed = self.feeds_col.find_one({"url": url})
        # if this is the only place the feed is used
        if len(feed["destinations"]) == 1:
            # remove the whole feed
            self.feeds_col.remove(feed)
        else:
            # delete this destination
            self.feeds_col.update(feed, {"$pull":{
                "destination": {"target": target}
            }})

    def edit(self, message, url=None, target=None, display=False):
        # sanitize user input
        if not url:
            raise self.bot.util.RuntimeError(
                "Missing argument: url. Usage: $rss delete [flags] <url>",
                message.target, self
            )
        target = target if target else message.target
        target = target if type(target) == str else target.id
        # get the feed
        feed = self.feeds_col.find_one({"url": url})
        if not feed:
            raise self.bot.util.RuntimeError(
                "That feed is not currently being tracked. If you meant to add"
                "it use $rss add <url>", message.target, self
            )
        # get the destination
        destination = [f for f in feed["destinations"] if f["target"] == target][0]
        # which menu is being requested
        if display:
            # build a set of example entry variables to choose from
            sample_feed = feedparser.parse(feed["url"])
            sample_entry = sample_feed["entries"][0]
            del sample_feed["entries"]
            sample_entry.update({"feed:"+k:v for k, v in sample_feed.items()})
            keys = self.default_settings if destination["keys"] == "default" \
                    else destination["keys"]
            msg = "```\n" \
                "Each feed entry has the following data available:\n\n" \
                "%s\n" \
                "```" % "\n".join(["[%s] - %s" % (k, v) for k,v in sample_entry.items()
                        if type(v) == str])
            print(message.target, msg)
            self.bot.msg(message.target, msg)

        else:
            # ask which property to be edited
            self.bot.menu(message.target, message.author_id,
                "What aspect of this feed would you like to edit?", [
                [
                    "Display - The way the feed is displayed",
                    lambda: self.edit(message, url, target, display=True)
                ]
            ])

    def post_entry(self, destination, entry):
        keys = self.default_settings \
                if destination["keys"] == "default" \
                else destination["keys"]
        # turns a key format into value string
        format_key = lambda t: " ".join(entry[k[1:]]
                if k[0] == "$" else k for k in keys[t].split())
        self.bot.msg(
            destination["target"],
            " " + " ".join(destination["pings"]),
            embed=self.bot.server.embed(
                title=format_key("title"),
                desc=format_key("desc"),
                footer=format_key("footer"),
                url=format_key("url"),
                color=format_key("color")
            )
        )

    def loop(self):
        while True:
            for feed in self.feeds_col.find({}):
                f = feedparser.parse(feed["url"])
                if "entries" in f:
                    # could not get feed. Disconnected from the internet?
                    continue
                # find out where the new entries start
                i = 0
                for entry in f["entries"]:
                    if feed["unique_key"] == entry["title"]:
                        break
                    i += 1
                # if there are no new entries
                if i == 0:
                    # no new articles, go to next feed
                    continue
                elif i+1 > len(f["entries"]):
                    # we didn't find our title at all. Post all articles
                    i = len(f["entries"])
                # make list of only new entries
                entries = f["entries"][:i]
                # remove entry list from the feed to save resources
                del f["entries"]
                # for each new entry
                for entry in f["entries"][:i]:
                    # add some of the feed keys for use in markup
                    entry.update({"feed:"+k:v for k, v in f.items()})
                    for destination in feed["destinations"]:
                        # default to true if there are no conditions
                        match = False if destination["conditions"] else True
                        # run the conditions against the entry
                        for key, conditions in destination["conditions"]:
                            for conditions in conditions:
                                if re.search(condition, entry[key]):
                                    match = True
                                    break
                        if not match:
                            # entry does not match the conditions for this dest
                            continue
                        self.post_entry(destination, entry)
                self.feeds_col.update(feed, {
                    "$set":{
                        "unique_key": f["entries"][0]["title"]
                    }
                })
            time.sleep(60*60)

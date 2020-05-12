import json
import requests
from bs4 import BeautifulSoup

from taiiwobot.plugin import Plugin

class Movies(Plugin):
    def __init__(self, bot):
        self.acceptable_qualities = ["HDRip", "HD", "720p"]

        self.bot = bot
        self.db = bot.util.get_db()
        self.interface = bot.util.Interface(
            "movie",
            "Sets up notifications for when movies are released in HD",
            [],
            self.root,
            subcommands=[
                bot.util.Interface(
                    "search",
                    "Search for a movie",
                    [],
                    self.search
                )
            ]
        ).listen()

    def root(self):
        self.interface.help(message.target, self)

    def search(self, message, *query):
        # search for the movie on IMDB
        title = "_".join(query).lower()
        imdb_resp = requests.get(
            "https://v2.sg.media-imdb.com/suggests/%s/%s.json" % (title[0], title)
        ).text
        imdb_list = json.loads(imdb_resp[6+len(title):-1])
        imdb_list = imdb_list["d"] if "d" in imdb_list else []
        imdb = False
        for movie in imdb_list:
            if movie["q"] in ["feature", "tv_movie", "tv_special", "tv_short"]:
                imdb = movie
                break
        if not imdb:
            self.bot.msg(message.target, "Movie birb could not find that movie. Movie birb is sorry.")
            return
        quality, link = self.movie_available(imdb)
        #quality = "TEST" # uncomment for ghetto debugging
        # make an embed for the movie
        embed = {
            "title": imdb["l"],
            "color":"bade83",
            "desc": "With " + imdb["s"]
        }
        if quality:
            embed["url"] = "https://fmovies.cafe" + link
        if "i" in imdb:
            embed["thumbnail"] = imdb["i"][0]
        embed = self.bot.server.embed(**embed)
        quality = "the future" if not quality else quality
        if quality in self.acceptable_qualities:
            self.bot.msg(message.target,
                "This movie is already available in `%s`." % quality,
                embed=embed
            )
            return True

        def handler(reaction):
            if reaction["reactor"] == self.bot.server.me():
                return
            self.add_request(imdb, reaction["reactor"], message.target)
            self.bot.msg(
                message.target,
                "Ok, %s, I've updated your watchlist." %
                        self.bot.server.mention(reaction["reactor"])
            )

        self.bot.msg(message.target,
            "This movie is currently only available in `%s`. To be notified when the movie is available in HDRip or better, ring the bell!" % quality,
            embed=embed,
            reactions=[("🔔", handler)]
        )

    def add_request(self, movie, requester, target):
        # add the movie to the watch list if we're not watching it already
        if not self.db["movies_watch_list"].find_one({"l": movie["l"]}):
            self.db["movies_watch_list"].insert_one(movie)
        # set the request args
        request = {
            "requesters": [requester],
            "request_channel": target,
            "l": movie["l"]
        }
        print(request)
        db_request = self.db["movies_requests"].find_one({"l": movie["l"], "request_channel": target})
        if db_request:
            # append existing request
            r = self.db["movies_requests"].update(
                db_request,
                {"$push": {"requesters": requester}}
            )
        else:
            # add the request to the database
            r = self.db["movies_requests"].insert_one(request)
        return r

    # checks if a movie is available on FMovies, and in what quality
    def movie_available(self, movie):
        """ torrentapi seems broken, skip for now
        # get a new token if required
        global token_time, token
        if token_time - time.time() >= 60*15:
            token = requests.post("https://torrentapi.org/pubapi_v2.php", {
                "get_token": "get_token"
            } ).text
            print(token)
            token_time = time.time()
        search = requests.post("https://torrentapi.org/pubapi_v2.php", {
            "mode": "search",
            "token": token,
            "search_string": movie["l"]
        } ).text
        """
        fmovies_html = json.loads(requests.get(
            "https://fmovies.cafe/ajax/film/search?sort=year:desc&keyword=%s" %
            movie["l"].replace("_", "+")
        ).text)["html"]
        if fmovies_html == "":
            return False, False
        soup = BeautifulSoup(fmovies_html, "html.parser")
        #TODO: Maybe add support for similar titles
        title = soup.find(class_="name")
        if soup.find(class_="name").get_text() != movie["l"]:
            return False, False
        return soup.find(class_="quality").get_text(), title["href"]

import json, requests, time
from bs4 import BeautifulSoup
from taiiwobot.plugin import Plugin


class Movie(Plugin):
    def __init__(self, bot):
        self.acceptable_qualities = ["HDRip", "HD", "720p"]
        self.bot = bot
        self.db = bot.util.get_db()
        self.interface = bot.util.Interface(
            "movie",
            "Sets up notifications for when movies are released in HD. Args: <search_query>",
            [],
            self.search,
            subcommands=[
                bot.util.Interface(
                    "search",
                    "Search for a movie Args: search_query (default command)",
                    [],
                    self.search,
                ),
                bot.util.Interface(
                    "watchlist",
                    "Display your watchlist. Args: [user]",
                    [],
                    self.watchlist,
                ),
                bot.util.Interface(
                    "delete",
                    "Delete a movie from your watchlist. Args: [movie_title]",
                    [],
                    self.delete,
                ),
            ],
        ).listen()
        self.updated_db = False
        self.db_cache = False
        bot.util.thread(self.loop)

    def root(self, message, *args):
        self.interface.help(message.target, self)

    def loop(self):
        # every one hour
        while True:
            # check for movies
            for movie in self.get_watch_list():
                quality, link = self.movie_available(movie)
                print(movie["l"] + " - " + (quality if quality else "False"))
                if quality and quality in self.acceptable_qualities:
                    # we got a movie
                    # fulfill all the notify requests
                    requests = self.db["movie_requests"].find({"l": movie["l"]})
                    for request in requests:
                        mentions = " ".join(
                            [self.bot.server.mention(r) for r in request["requesters"]]
                        )
                        self.bot.msg(
                            request["request_channel"],
                            "The movie `%s` is now available on fmovies in `%s` %s - [http://fmovies.taxi%s]"
                            % (movie["l"], quality, mentions, link),
                        )
                    self.remove_from_watch_list(movie)
            time.sleep(60 * 60)

    def watchlist(self, message):
        requests = self.db["movie_requests"].find({"requesters": message.author})
        if not requests:
            self.bot.msg(
                message.target,
                "You have no movies in your watchlist. Use $movie search <title> to add some!",
            )
            return
        f = lambda r: "%s - %s" % (
            self.bot.server.mention(r["request_channel"]),
            r["l"],
        )
        self.bot.msg(message.target, "\n".join([f(r) for r in requests]))
        self.bot.menu(
            message.target,
            message.author,
            "Would you like to delete an entry from this list?",
            ync=[lambda r: self.delete(message), lambda r: None, lambda r: None],
        )

    def delete(self, message, *args):
        requests = self.db["movie_requests"].find({"requesters": message.author})
        requests = [r for r in requests]

        def del_real(r, request):
            if len(request["requesters"]) == 1:
                self.db["movie_requests"].remove(request)
            else:
                self.db["movie_requests"].update(
                    request, {"$pop": {"requesters": message.target}}
                )
            self.bot.msg(
                message.target,
                "%s has been removed from your watchlist!" % request["l"],
            )

        def del_movie(title, channel=message.target):
            for request in requests:
                if (
                    title.lower() == request["l"].lower()
                    and request["request_channel"] == message.target
                ):
                    self.bot.menu(
                        message.target,
                        message.author,
                        "Are you sure you wish to delete %s?" % request["l"],
                        ync=[
                            lambda r: del_real(r, request),
                            lambda r: None,
                            lambda r: None,
                        ],
                    )

        if len(args) == 0:
            if len(requests) > 11:
                titles = "\n".join([r["l"] for r in requests])
                if len(titles) <= 2000:
                    self.bot.msg(message.target, titles)
                else:
                    self.bot.msg(message.target, "You have too many movies to list!")
                self.bot.prompt(
                    message.target,
                    message.author,
                    "Please type the name of the movie you want to delete:",
                    del_movie,
                )
            else:
                self.bot.menu(
                    message.target,
                    message.author,
                    "Select the movie you want to delete: ",
                    answers=[[t["l"], lambda r: del_movie(t["l"])] for t in requests],
                )
        else:
            title = " ".join(args)
            for request in requests:
                if request["l"].lower() == title.lower():
                    del_movie(title)

    def search(self, message, *query):
        print("searching...", message.target)
        title = "_".join(query).lower()
        imdb_resp = requests.get(
            "https://v2.sg.media-imdb.com/suggests/%s/%s.json" % (title[0], title)
        ).text
        imdb_list = json.loads(imdb_resp[6 + len(title) : -1])
        imdb_list = imdb_list["d"] if "d" in imdb_list else []
        imdb = False
        for movie in imdb_list:
            if movie["q"] in ("feature", "tv_movie", "tv_special", "tv_short"):
                imdb = movie
                break
            else:
                if not imdb:
                    self.bot.msg(
                        message.target,
                        "Movie birb could not find that movie. Movie birb is sorry.",
                    )
                    return
        quality, link = self.movie_available(imdb)
        embed = {"title": imdb["l"], "color": "bade83", "desc": "With " + imdb["s"]}
        if quality:
            embed["url"] = "https://fmovies.cafe" + link
        if "i" in imdb:
            embed["thumbnail"] = imdb["i"][0]
        embed = (self.bot.server.embed)(**embed)
        quality = "the future" if not quality else quality
        # quality = "TEST"
        if quality in self.acceptable_qualities:
            self.bot.msg(
                (message.target),
                ("This movie is already available in `%s`." % quality),
                embed=embed,
            )
            return True

        def handler(reaction):
            if reaction["reactor"] == self.bot.server.me():
                return
            if self.add_request(imdb, reaction["reactor"], message.target):
                self.bot.msg(
                    message.target,
                    "Ok, %s, I've updated your watchlist."
                    % self.bot.server.mention(reaction["reactor"]),
                )
            else:
                self.bot.msg(
                    message.target,
                    "That movie is already on your watchlist, %s."
                    % self.bot.server.mention(reaction["reactor"]),
                )

        self.bot.msg(
            (message.target),
            (
                "This movie is currently only available in `%s`. To be " % (quality)
                + "notified when the movie is available in HDRip or better, "
                + "ring the bell!"
            ),
            embed=embed,
            reactions=[("🔔", handler)],
        )

    def add_request(self, movie, requester, target):
        self.updated_db = True
        if not self.db["movie_watch_list"].find_one({"l": movie["l"]}):
            self.db["movie_watch_list"].insert_one(movie)
        request = {
            "requesters": [requester],
            "request_channel": target,
            "l": movie["l"],
        }
        print(request)
        db_request = self.db["movie_requests"].find_one(
            {"l": movie["l"], "request_channel": target}
        )
        if db_request:
            if requester in db_request["requesters"]:
                return False
            r = self.db["movie_requests"].update(
                db_request, {"$push": {"requesters": requester}}
            )
        else:
            r = self.db["movie_requests"].insert_one(request)
        return r

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
        try:
            fmovies_html = json.loads(
                requests.get(
                    "https://fmovies.cafe/ajax/film/search?sort=year:desc&keyword=%s"
                    % movie["l"].replace("_", "+")
                ).text
            )["html"]
        except requests.exceptions.ConnectionError as e:
            print(e)
            return (False, False)
        if fmovies_html == "":
            return (False, False)
        soup = BeautifulSoup(fmovies_html, "html.parser")
        movies = soup.find_all(class_="item")
        for m in movies:
            if m.find(class_="name").get_text().lower() == movie["l"].lower():
                return (
                    m.find(class_="quality").get_text(),
                    m.find(class_="name")["href"],
                )
        return (False, False)

    def get_watch_list(self):
        if self.updated_db or not self.db_cache:
            self.db_cache = self.db["movie_watch_list"].find()
            self.updated_db = False
        else:
            self.db_cache.rewind()
        return self.db_cache

    def remove_from_watch_list(self, movie):
        self.updated_db = True
        self.db["movie_watch_list"].remove({"l": movie["l"]})
        self.db["movie_requests"].remove({"l": movie["l"]})

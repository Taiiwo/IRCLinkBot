import discord
import time
import re

Empty = discord.Embed.Empty

from . import util

class Discord:
    def __init__(self, config):
        missing_keys = util.missing_keys(["api_key"], config)
        if missing_keys:
            quit("[E] Missing args: %s. Check config.json" % (', ').join(missing_keys))
        defaults = {
        }
        defaults.update(config)
        self.config = defaults
        self.callbacks = {}
        self.reaction_callbacks = {}

        self.client = discord.Client()

        @self.client.event
        async def on_message(message):
            message = self.format_message(message)
            self.trigger("message", message)

        @self.client.event
        async def on_reaction_add(reaction, reactor):
            # do we have any code to run in response to this?
            if reaction.message.id in self.reaction_callbacks:
                user, reactions = self.reaction_callbacks[reaction.message.id]
                if user != reactor.id:
                    return False
                for reaction_emoji, function in reactions:
                    if reaction.emoji == reaction_emoji:
                        function()
                        # remove reactions
                        calls = []
                        for reaction_emoji, x in reactions:
                            calls.append([self.client.remove_reaction, (
                                reaction.message, reaction_emoji, self.client.user
                            ), {}])
                        self.gaysyncio(calls)
                        # remove callbacks
                        del self.reaction_callbacks[reaction.message.id]
                        break

    def start(self):
        self.client.run(self.config["api_key"])

    def embed(self, title=Empty, url=Empty, desc=Empty, author_name=Empty,
            author_url=Empty, author_icon=Empty, fields=[], footer=Empty,
            color=Empty, thumbnail=Empty):
        e = discord.Embed(title=title, url=url, description=desc, color=int(color, 16))
        if thumbnail:
            e.set_thumbnail(url=thumbnail)
        for field in fields:
            e.add_field(name=field[0], value=field[1],
                        inline=field[2] if len(field) > 2 and not field[2] else True)
        if author_name or author_url or author_icon:
            e.set_author(name=author_name, url=author_url, icon_url=author_icon)
        e.set_footer(text=footer)
        return e

    def menu(self, target, user, question, answers=None, ync=None):
        if ync:
            if len(ync) != 3:
                raise util.Error("ync must have 3 elements:"
                        "a function for yes, no, and cancel")
            reactions = ["👍", "👎", "❌"]
            answers = ["Yes", "No", "Cancel"]
            functions = ync

        else:
            if not answers:
                raise util.Error("You can't call this function with no answers")
            if len(answers) > 11:
                raise util.Error(
                    "A maximum of 11 options are supported. You supplied %s" %
                    len(answers)
                )
            numbers = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
            # if user supplies an icon to use, use that, else use a number icon
            reactions = [numbers[i] if len(a) < 3 else a[0]
                    for i, a in enumerate(zip(*answers))]
            # parse the answers array, ignoring the supplied icon if supplied
            answers, functions = [a_f_tuple if len(a_f_tuple) < 3 else a_f_tuple[1:3]
                    for a_f_tuple in zip(*answers)]
        message = "%s\n\n%s\n\nReact to answer." % (
            question,
            "\n".join(["[%s] - %s" % (r, a) for r, a in zip(reactions, answers)])
        )
        self.msg(target, message, reactions=zip(reactions, functions), user=user)

    # discord method wrappers
    def msg(self, target, message, embed=None, reactions=tuple(), user=None):
        if type(target) == str:
            if target.isnumeric():
                t = self.client.get_channel(target)
                if not t:
                    t = self.client.get_user_info(target)
                target = t
        if type(message) == util.Message:
            message = message.content
        if message != "":
            # a list of asynchronous calls to make
            async_calls = [
                # sending the message
                [self.client.send_message, (target, message), {"embed": embed}]
            ]
            reactions = list(reactions)
            # add the reactions
            for r, f in reactions:
                async_calls.append([self.client.add_reaction, ("$0", r), {}])
            # a callback for when the message and all the reactions have been sent
            async def add_reaction_callbacks(message):
                # make a note of the message id, so that if the user clicks them
                # the reaction callback function is run
                self.reaction_callbacks[message.id] = (user, reactions)
            # finally, add the reactions callback if required
            if reactions:
                async_calls.append([add_reaction_callbacks, ("$0",), {}])
            self.gaysyncio(async_calls)
            self.trigger("sent", target, message, embed)

    def join(self, channel):
        pass

    # event handler handling
    def on(self, command):
        def handler(f):
            self.add_callback(f, command)
        return handler

    # removes an even handler
    def off(self, f, command):
        if command in self.callbacks:
            self.callbacks[command].remove(f)

    def trigger(self, event, *data):
        if event in self.callbacks:
            try:
                util.callback(self.callbacks[event], *data)
            except util.RuntimeError as e:
                print(e.text)

    def add_callback(self, callback, command):
        if command not in self.callbacks:
            self.callbacks[command] = []
        self.callbacks[command].append(callback)

    def format_message(self, m):
        return util.Message(
            nick=m.author.nick if hasattr(m.author, "nick") else m.author.name,
            username="%s#%s" % (m.author.name, m.author.discriminator),
            author_id=m.author.id,
            type="message",
            target=m.channel.id,
            content=m.content,
            raw_message=m,
            server_type="discord",
            timestamp=m.timestamp,
            embeds=m.embeds,
            attachments=m.attachments
        )

    def gaysyncio(self, calls):
        async def f():
            # make a buffer of output values
            buffer = []
            # if one of the args starts with a $, replace it with it's index inbuffer
            for function, args, kwargs in calls:
                args2 = []
                for arg in args:
                    if type(arg) == str and len(arg) > 1 and arg[0] == "$":
                        try:
                            args2.append(buffer[int(arg[1:])])
                        except IndexError:
                            args2.append(arg)
                    else:
                        args2.append(arg)
                args = args2
                buffer.append(await function(*args, **kwargs))
        self.client.loop.create_task(f())

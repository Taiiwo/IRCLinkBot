import time
import re

from . import util

class Server:
    callbacks = {}
    message_callbacks = {}

    def code_block(self, text):
        # code blocks aren't supported by default
        return text

    def mention(self, user):
        return user

    def me(self):
        return self.config["user"]

    def menu(self, target, user, question, answers=None, ync=None, cancel=False):
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
                    for i, a in enumerate(zip(answers))]
            # parse the answers array, ignoring the supplied icon if supplied
            answers, functions = zip(*[a_f if len(a_f) < 3 else a_f[1:3]
                    for a_f in answers])
        message = "%s\n\n%s\n\nReact to answer." % (
            question,
            "\n".join(["[%s] - %s" % (r, a) for r, a in zip(reactions, answers)])
        )
        self.msg(target, message, reactions=zip(reactions, functions), user=user)

    def prompt(self, target, user, prompt, handler, cancel=False, timeout=60.0):
        self.msg(target, prompt,
            reactions=[["❌", cancel_wrapper]],
            user=user
        )
        self.message_callbacks[target + ":" + user] = [time.time(), handler, timeout]

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
        print(event)
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
            server_type="unknown",
            timestamp=m.timestamp,
            embeds=m.embeds,
            attachments=m.attachments
        )

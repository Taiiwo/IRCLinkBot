import pymongo
import requests
from threading import Thread

def thread(func, args=[], kwargs={}):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread

def maketiny(url):# make a tinyurl from a string
    try:
        html = requests.get("http://tinyurl.com/api-create.php?url=" + url)
        tiny = str(html.text)
        tiny = tiny.replace("http", "https")
        return tiny
    except:
        return url

db = False
def get_db():
    global db
    if not db:
        db = pymongo.MongoClient()["taiiwobot"]
    return db

def debug(msg):
    print(msg)

def missing_keys(keys, dict):
    missing_keys = []
    for key in keys:
        if key not in dict:
            missing_keys.append(key)
    return False if len(missing_keys) == 0 else missing_keys

def callback(callbacks, data):
    for callback in callbacks:
        callback(data)

# universal message object
class Message():
    def __init__(self, nick=None, username=None, author_id=None, host=None,
                    type=None, target=None, content=None, raw_message=None,
                    timestamp=None, server_type=None, embeds=[], attachments=[],
                    ident=None):
        self.nick = nick # display name of the user
        self.username = username # unique username of the user
        self.author = author_id
        self.author_id = author_id # deprecated
        self.host = host
        self.type = type
        self.target = target
        self.content = content
        self.raw_message = raw_message
        self.server_type = server_type
        self.timestamp = timestamp
        self.attachments = attachments
        self.embeds = embeds

class Interface:
    def __init__(self, name, desc, flag_info, func,
                    subcommands=[], is_subcommand=False, prefix="$"):
        self.prefix = prefix
        self.name = name
        self.desc = desc
        self.func = func
        self.subcommands = []
        for subcommand in subcommands:
            subcommand.is_subcommand = True
            self.subcommands.append(subcommand)
        self.is_subcommand = is_subcommand
        try:
            self.flag_info = [[
                x[0], x[1].replace("-", "_"), " ".join(x[2:-1]), int(x[-1])
            ] for x in [b.split() for b in flag_info]]
        except ValueError as e:
            raise Error("The last word of a flag string must be an integer", e)
        self.flags = []
        # make a list of all our flags
        [self.flags.extend(i[0:2]) for i in self.flag_info]

    # listen for messages
    def listen(self):
        @self.func.__self__.bot.on("message")
        def on_message(message):
            if not self.func or hasattr(self.func.__self__, "_unloaded"):
                self.func = None
            else:
                self.func.__self__.interface.process(message)
        return self

    def add_subcommand(self, interface):
        if not self.subcommands:
            self.subcommands = []
        interface.is_subcommand = True
        self.subcommands.append(interface)

    # posts the help message for this command into the chat
    def help(self, target, plugin):
        subcommands = "\n".join(
            ["\t%s%s %s" % (s.name, " " * (10 - len(s.name)), s.desc) for s in self.subcommands]
        )
        flags = "\n".join(
            ["\t-%s --%s%s %s %s" % (
                f[0], f[1], "=<value>" if f[3] else "",
                " " * (20 - len(f[0] + f[1]) - (8 if f[3] else 0)), f[2]
            ) for f in self.flag_info]
        )
        plugin.bot.server.msg(
            target,
            "```\n"
            "%s - %s\n\n"
            "Subcommands:\n"
            "\thelp       display usage information for this command\n"
            "%s\n\n"
            "Flags:\n"
            "\t--help                    display usage information for this command\n"
            "%s"
            "```" % (self.prefix + self.name, self.desc, subcommands, flags)
        )

    # Future Taiiwo here. This function is a completely needless reimplementation
    # of the argparse module. Come and marvel of the effects of not searching
    # for code before you write it, and the subbornness of still using it
    # even if the original code is probably better...........
    def process(self, message, arguments=False, kwargs=False, o_message=False):
        kwargs = kwargs if kwargs else {}
        arguments = arguments if arguments else tuple()
        o_message = o_message if o_message else message
        args = message.content.split()
        if not self.is_subcommand and len(args) < 1:
            return False
        # skip the first arg because it's the name of the command
        i = 1
        # if command != our command name (omitting prefix if we're a subcommand)
        if args[0] != self.prefix * (not self.is_subcommand) + self.name:
            # this message does not refer to this interface
            return False
        while i < len(args):
            arg = args[i]
            # get a list of subcommands where the name == arg
            subcommand = [x for x in self.subcommands if arg == x.name]
            # grab the first match if exists else False
            subcommand = subcommand[0] if len(subcommand) == 1 else False
            # is arg a subcommand?
            if subcommand:
                # process the rest of this command as the sub command
                message.content = " ".join(args[i:])
                return subcommand.process(message,
                    arguments=arguments, kwargs=kwargs, o_message=message) # pass the flags we got
            elif arg.lstrip("-") == "help":
                self.help(o_message.target, self.func.__self__)
                return False
            # does this arg look like a flag?
            if arg[0] == "-":
                # look for this flag in our list of flags
                flag_name = arg.strip("-").split("=")[0]
                if flag_name in self.flags:
                    # get the info for this flag
                    info = self.flag_info[int(self.flags.index(flag_name) / 2)]
                    # parse the value of this flag
                    if "=" in arg:
                        # the flag has an =, so parse the contents as the value
                        value = "=".join(arg.split("=")[1:])
                    elif info[3] == 1:
                        # skip processing on the next arg
                        i += 1
                        if i >= len(args):
                            raise RuntimeError('Flag `%s` requires a value. Try -%s="some value"' %
                                    (info[1], info[0]))
                        # set the value to that next arg
                        value = args[i]
                    else:
                        value = "True"
                    # if the value has quotes around it
                    if value[0] == '"':
                        quote = False
                        start = i
                        # look for the end quote
                        while i < len(args):
                            if args[i][-1] == '"':
                                # we found the end
                                quote = (value + " ".join(args[start+1:i+1]))[1:-1]
                                break
                            i += 1
                        # did we find the end of the quote
                        if quote:
                            value = quote
                        else:
                            # set i back to normal
                            i = start
                            # put the quote back
                            value = '"' + value
                    else:
                        # remove escaping backslashes if present
                        value = value[1:] if value[0] == "\\" else value
                    if value == "true" or value == "True":
                        value = True
                    kwargs[info[1]] = value
                else:
                    # this arg looks like a flag, but actually is not
                    raise RuntimeError(
                        "Flag %s does not exist. If it was intended as an "
                        "argument, you must escape it like `\\\\%s`" % (arg, arg),
                    o_message.target, self.func.__self__)
            else:
                # this argument is not a flag, therefore we can add it as an argument
                arguments += (arg[1:] if arg[0] == "\\" else arg,)
            i += 1
        return self.func(message, *arguments, **kwargs)

def interface_test():
    interface = Interface(
        "test",
        "This is a test interface",
        [
            "t test This is a test flag 0",
            "t2 test2 This flag has a value 1"
        ],
        lambda *x, **y: (x, y),
        subcommands=[
            Interface(
                "sub_test",
                "This is a test subcommand",
                [],
                lambda *x, **y: (x, y)
            )
        ]
    )
    import copy
    interface.add_subcommand(copy.copy(interface)) # is this allowed? :eyes:
    message_tests = [
        [Message(content='$test -t2="ayy"'), (tuple(), {"test2":"ayy"})], # passing a quoted value to a non-bool flag
        [Message(content="$test -t"), (tuple(), {"test": True})], # default use of a bool flag
        [Message(content="$test -t a"), (("a",), {"test": True})], # passing a value to a bool flag
        [Message(content="$test -t a b"), (("a", "b"), {"test": True})], # passing a value to a bool flag plus an argument
        [Message(content="$test sub_test ayy"), (("ayy",), {})], # passing an argument to a sub command
        [Message(content="$test test -t"),(tuple(), {"test": True})], # testing sub command recurrsion
        [Message(content="$test test test test -t"),(tuple(), {"test": True})] # hmmm
    ]
    for test in message_tests:
        r = interface.process(test[0])
        print("%s - %s" % (r, "True" if r[0][1:] == test[1][0] and r[1] == test[1][1] else "False"))

class Error(Exception):
    pass

class RuntimeError(Exception):
    def __init__(self, message, target, plugin):
        self.text = message
        super().__init__(message)
        plugin.bot.server.msg(target, message)


if __name__ == "__main__":
    interface_test()

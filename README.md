TaiiwoBot - v5
==========
Introduction - What is TaiiwoBot v5?
------------------------------------------------
This program is chat bot framework that allows you to add custom plugins and customization options that runs quickly on a high memory system.
There are some plugins preinstalled that I developed.
You can use these as is, or as examples to build your own plugins.
It it built to run on any platform, but the currently supported plaforms are IRC and Discord.

<video controls autoplay>
    <source src="https://thumbs.gfycat.com/FearlessTightGarpike-mobile.mp4" type="video/mp4">
    Video not supported by your browser!
</video>


Refactor - Why is this different from IRCLinkBot?
-----------------------------------------------------------------
In this restructure, I decided to make the bot totally platform independant.
Theoretically, all of the plugins should work on any chat platform, as long as an appropriate
server wrapper is created.

On top of having drop in plugins like in the previous version, the plugins now have
a class structure for a more robust plugin coding experience, automatic help text,
and implementation of argument and subcommand parsing, allowing you to code normal pythonic
functions as opposed to parsing input data from the message string.

The server wrappers are implemented in a way that makes creating cross platform plugins
extremely high level and simple. Many interface features are implemented at the server wrapper
level, so you can create very advanced looking, experience-rich plugins with very little code.

How to run the bot:
-------------------
1. Install the dependecies in requirements.txt: `pip install -r requirements.txt`
2. Run the bot with `python discord_main.py` or replace `discord` with your platform of choice
3. If it's your first time running the bot, a `config.json` file will be created for you to edit. Add the required values for your chosen platform (including API Tokens), and repeat step 2

Once the bot successfully logs in, you can get started by typing `$help` anywhere the bot can read.

Developing Plugins
------------------
### The Plugin Code
Creating plugins is very simple. Open a new python file in the plugins directory.
Create a new class that inherits the Plugin base class. Make sure the class name
is the same as the file name, and type `$reload example` to load your plugin into
the running bot (The plugin will also automatically load when the bot is restarted).

Most basic plugin example:

```python
from taiiwobot import Plugin

class Example(Plugin):
    def __init__(self, bot):
        # this code runs when the plugin is loaded
```

### Interfacing with the platform
The code above will run your code, and give it access to the `bot` context, but
nothing else. In order for your plugin to listen for and parse user input we need to create an `Interface`.

Creating an Interface can look a bit complicated, but it's really very simple,
and it gets all of the user friendly stuff out of the way, so you can focus on programming.

Take this example:

```python
from taiiwobot import Plugin

class Example(Plugin):
    def __init__(self, bot):
        # make the bot context accessible
        self.bot = bot
        # define our interface
        self.interface = bot.util.Interface(
            "example", # plugin name
            "This is a demo plugin you can use to learn how plugins work", # plugin description
            ["e example-flag This is an example flag 1"], # flags - we'll explain these later
            self.say, # main function
        ).listen() # Begin listening for messages

    def say(self, message, *things, example_flag=""):
        # sends a message to the channel it came from
        self.bot.msg(message.target, " ".join(things))
```

The above is a very simple example of an Interface. It will listen to messages
starting with the prefix, followed by the plugin name (`$example`), and will execute
the main function in response. In this case, `self.say()`. The interface will automatically
parse the arguments supplied by the user, and pass them to the `*things` argument.
The `say()` function then repeats the user's message to the same channel that sent it
using the `message` context object.

The interface also handles your help text. You can now type `$example help`, and
the interface will create useful help documentation, telling the user how to use
it's subcommands and flags. It will look something like this:

```
$example - This is a demo plugin you can use to learn how plugins work

Subcommands:
    help       display usage information for this command

Flags:
    --help                    display usage information for this command
    -e --example-flag=<value> This is an example flag
```

### Flags
Adding flags to your Interface allows you to pass keyword arguments to your main
function, parsed directly from the user's message. Flags are defined as an array of
flag strings. The syntax for defining a flag string consists of 4 parts:

1. short name
2. long name
3. description
4. value type

For example: "e example-flag This is an example flag 1"

The above flag can be invoked by the user with either `-e value` or `--example-flag="value with space"`.
The values will be passed as keyword arguments to your main function in the form `main_function(..., example_flag="parsed value")`. Note: hyphens are converted to underscores to maintain naming conventions.

The description is used in the generation of the help text, and should be used to
describe the function of the flag, and the accepted values.

Value type determines the type of the value that will be parsed from the flag and can be either:

0. A boolean flag; can be passed by itsself, and sets the flag value to True
1. A string value; sets the flag to expect a string value

Both short and long flag types support string values expressed in the following ways:

```bash
-f value
-f "value with space"
-f="value with space"
-f=value
```

Obviously, flags and flag values are consumed, and don't show up in the function aruments.
If you want raw message content including flags, use `message.content`.

### Subcommands
The purpose of a subcommand is to allow the plugin to accept secondary commands to
separate its functionality into multiple functions defined within the plugin class.
Subcommands are submitted to the interface as a keyword argument in the form of an array of Interface objects.

### In summary:
You should now understand all the features of the following example, and be well on
your way to creating awsome plugins:

```python
from taiiwobot import Plugin

class Example(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.interface = bot.util.Interface(
            "example", # plugin name
            "This is a demo plugin you can use to learn how plugins work", # plugin description
            [ # Flags: <short form> <long form> <description> <1=string or 0=bool>
            # these will be loaded as kwargs to your main function
                "o output Specifies the location of the output file 1",
                "f force Forces the action 0",
                "q quiet Does the action quietly 0"
            ],
            self.some_func, # main function
            subcommands=[ # list of subcommands
                bot.util.Interface(
                    "sub", # invoked with $template sub <args/flags>
                    "says some stuff", # subcommand description
                    [ # subcommand flags
                        "f force Force adding the thing 0"
                    ],
                    self.say # subcommand function
                )
            ]
        ).listen() # sets the on message callbacks and parses messages

    # flags are parsed and passed to the assigned function like so:
    # *args catches all uncaught command arguments as an array.
    def some_func(self, message, *args, output="output", force=False, quiet=False):
        # asks the user for some text, runs the handler function with
        # their response
        self.bot.prompt(message.target, message.author_id,
            "This is an example prompt: ",
            lambda m: self.bot.msg(message.target, "Hello, " + m.content)
        )

    def say(self, message, *things, force=False):
        # sends a message to the channel it came from
        self.bot.msg(message.target, " ".join(things))

```


The Bot API
-----------
So now you've parsed your input and created your command, you're going to want
to interact back with the user. The simplest way to do this is to use the `bot.msg`
method used above to send text back into the channel, but as promised, this framework
has some useful features to make coding plugins even easier. Here's a list of all the
things you can do:

### bot.msg
Sends a message to the target. Arguments:

- target - The desired destination of the message.
- message - the string of the message contents
- embed=bot.embed - send fancy rich embeds (If the platform supports them)
- reactions=[[emoji, callback], ...] - Add reactions to your message, and run `callback` when clicked
- user=util.User - If specified, reaction callbacks only apply to `user`
- files=[file] - an array of files to upload to the target

### bot.menu
Creates a menu for the user to supply input. Arguments:

- target - The desired destination of the message.
- user:util.User - The user to listen to
- question:str - The text at the top of the menu
- answers=[[answer, callback], ...] - The list of answers, and their callbacks
- cancel=callback - callback for if the menu is cancelled
- ync=[callback, callback, callback] - shorthand for quick yes, no, cancel menu

### bot.prompt
Prompt the user for a response, and pass it to a handler. Arguments:

- target - The desired destination of the message.
- user:util.User - The user to listen to
- prompt:str - The text at the top of the menu
- handler:function(message) - function to run when the user has responded
- cancel=function(reaction_event) - callback function if the user cancels the prompt
- timeout=float(60.0) - amount of time to wait before timing out the prompt

### bot.server.me()
Returns the user representor for the bot user

### bot.server.mention
returns the mention string for the target using the current platform. Arguments:

target - the target to mention

### bot.server.join
Joins a target object (not really implemented as most platforms don't support bots joining servers)

### bot.server.code_block
returns a code block formatted for the target platform. Arguments:

- text:str - string to put in the code block

### Bot events
Bot is event driven. Use these methods to control bot event handlers:

#### bot.on
function decorator to handle raw bot events. Arguments:

- event:str - Name of the event to handle

#### bot.off
Removes an event handler. Arguments:

- handler:function - hander to remove
- event:str - event name to remove it from

#### bot.trigger
Triggers a global bot event. Arguments:

- event:str - name of the event to trigger
- \*data - data to send to the even handler

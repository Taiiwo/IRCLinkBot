Creating a Server Module
========================
To create a server module for TaiiwoBot, it needs to connect on init, and
serve the following features:

Event Handlers
--------------
An `on` decorator function that takes a list of command words. Each command
word corresponds to a different event handler assignment:

`message`: When a user message is sent from another user

`join`: When a user connects to a channel

`leave`: When a user joins a channel

`quit`: When a user logs out

`ping`: called when the server requests a ping from the bot

`sent`: Every time a message is sent by the bot

Support for all other commands is optional until further notice

Required methods
----------------
In order for your module to be compatible with other TaiiwoBot plugins, you
need to serve the following methods:

`msg(target, message, embed=None)`: Sends a text message to the server
  target can be any string or object used by your wrapper to signify a message location
  message is a universal message object or a string of the message contents
  embed must be whatever is returned by `embed`, and should be handled by sending the contents of the object in a neat an uniform way. For example discord servers can send Embed objects and IRC could send a nice ASCII table

`join(channel)`: Joins the named channel or room

`part(channel)`: Leaves the named channel or room

`embed(title:str, url:str, desc:str, author_name:str, author_url:str,
        author_icon:str, fields=[], footer:str, message_text:str):`
  returns something that is accepted by `msg(embed)`

`start()`
  a blocking function that is called when taiiwobot is done initiating and all the plugins have been instantiated. If you're using asyncio, this is where you execute your event loop. If you're using sockets, this is where you recv in an infinite loop, handling all your events

`format_message(message)`
  takes your representation of a message and returns a universal `Message` object defined in `util` to be sent to the plugin for use
  Note: Your original message object is represented as Message.raw_message
  everything else should be self explanatory. Just try and fill it up as much as you can. It's the plugin's responsibility to check the existence of properties before use

Example server handler skeleton
-------------------------------
This is just a suggestion / example of how to adhere to the above standards

Asyncio Example:
```python
class MyServer:
    def __init__(self, config):
        # your required config keys
        missing_keys = util.missing_keys(["api_key"], config)
        if missing_keys:
            quit("[E] Missing args: %s. Check config.json" % (', ').join(missing_keys))
        # your default config values
        defaults = {
        }
        defaults.update(config)
        self.config = defaults
        self.callbacks = {}

        # instatiate your server wrapper here if you need to
        self.client = server_wrapper.Client()

        # instruct your server wrapper to trigger the corresponding events
        @self.client.on_message
        async def on_message(data):
            self.trigger("message", data)

        @self.client.on_join
        async def on_join(data):
            self.trigger("join", data)

        @self.client.on_leave
        async def on_leave(data):
            self.trigger("leave", data)

        @self.client.on_quit
        async def on_quit(data):
            self.trigger("quit", data)

        @self.client.on_ping
        async def on_ping(data):
            self.trigger("ping", data)

        @self.client.on_send
        async def on_send(data):
            self.trigger("send", data)

    # server method wrappers

    # sends a message to a target
    # target should be the same type as util.Message["target"] and if applicable, util.Message["author"]
    # message is a string or universal util.Message object
    def msg(self, target, message, embed=None):
        if type(message) == str:
            message = message.splitlines()
        for line in message:
            if line != "":
                # you own custom message sending function. Make sure to handle
                # your embed object before sending it as the appropriate type
                # for your server type
                self.send_message(target, message, embed=Embed)
                self.trigger("sent", target, message)

    # joins a channel
    def join(self, channel):
      # joins a channel

    # event handling
    def on(self, *commands):
        def handler(f):
            for command in commands:
                self.add_callback(f, command)
        return handler

    def trigger(self, event, *data):
        util.callback(self.callbacks[event], data)

    # this method is not required, but is an example of how you might internally
    # handle callbacks
    def add_callback(self, callback, *commands):
        for command in commands:
            if command not in self.callbacks:
                self.callbacks[command] = []
            self.callbacks[command].append(callback)

    # parses your server-specific message type and turns it into a util.Message
    def format_message(self, m):
        return util.Message(
            nick=m.author.nick if hasattr(m.author, "nick") else m.author.name,
            username=m.author.name,
            type="message",
            target=m.channel,
            content=m.content,
            raw_message=m,
            server_type="discord",
            timestamp=m.timestamp,
            embeds=m.embeds,
            attachments=m.attachments
        )

```

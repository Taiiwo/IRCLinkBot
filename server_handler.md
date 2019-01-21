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

`msg(str: target, str:message)`: Sends a text message to the server
`join(str: channel)`: Joins the named channel or room
`part(str: channel)`: Leaves the named channel or room
import time
from taiiwobot import taiiwobot, irc, config

config = config.get_config()
# use IRC as our server protocol
server = irc.IRC(config['irc_config'])
# Start the bot!
taiiwobot.TaiiwoBot(server, config)

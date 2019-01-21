import time
from taiiwobot import taiiwobot, discord, config

config = config.get_config()
# load our server protocol
server = discord.Discord(config['irc_config'])
# Start the bot!
taiiwobot.TaiiwoBot(server, config)
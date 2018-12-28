import time
from taiiwobot import taiiwobot, discord, config, util

config = config.get_config()
# use discord as our server protocol
server = discord.Discord(config['discord_config'])
# Start the bot!
taiiwobot.TaiiwoBot(server, config)

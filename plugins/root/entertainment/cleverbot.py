def main(data):
	if data['config']['settings']['botNick'] in data['recv'] or data['config']['settings']['botNick'].lower() in data['recv']:
		from chatterbotapi import ChatterBotFactory, ChatterBotType
		factory = ChatterBotFactory()
		botfac = factory.create(ChatterBotType.CLEVERBOT)
		bot = botfac.create_session()
		args = argv(':', data['recv'])
		answer = bot.think( ' '.join(args['argv'][1:].replace('CleverBot',data['config']['settings']['botNick']))
		answer = answer.replace('CleverBot',data['config']['settings']['botNick']
		return say(args['channel'],answer)

		

def main(data):
	if data['config']['settings']['botNick'] in data['recv'] or data['config']['settings']['botNick'].lower() in data['recv']:
		from libchatterbot import ChatterBotFactory, ChatterBotType
		factory = ChatterBotFactory()
		botfac = factory.create(ChatterBotType.JABBERWACKY)
		bot = botfac.create_session()
		args = argv('@', data['recv'])
		junk = ':' + textbetween(':',' :', data['recv']) + ' :'
		query = data['recv'].replace(junk, '')
		query = query.replace('\n','')
		query = query.replace('\r','')
		query = query.replace(data['config']['settings']['botNick'] + ':','')
		query = query.replace(data['config']['settings']['botNick'],'Jorn')
		answer = bot.think(query)
		answer = answer.replace('George',data['config']['settings']['botNick'])
		answer = answer.replace('God','Taiiwo')
		answer = answer.replace('&ouml;', 'o')
		debug = 'Query: ' + query + ' -- Answer: "' + answer + '"'
		#return say(args['channel'],args['nick'] + ': ' + debug)
		return say(args['channel'],args['nick'] + ': ' + answer)
		

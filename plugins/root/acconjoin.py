def main(data):
        if ' JOIN ' in data['recv']:
                args = argv('JOIN', data['recv'])
		regdNick = False
		for user in data['config']['settings']['userModes']:
			if args['nick'] == user['nick']:
				regdNick = True
		if regdNick:
                	data['api'].say('nickserv', 'acc ' + args['nick'])


def main(data):
	if '!listmodes' in data['recv']:
		args = argv(data['recv'])
		for user in data['config']['settings']['userModes']:
			if args['argv'][1] == user['nick']:
				toret = user['nick'] + "'s modes: " + user['modes']
				return say(args['channel'], toret)

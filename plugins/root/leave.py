def main(data):
        if '!leave' in data['recv']:
                args = argv('!leave',data['recv'])
		for user in data['config']['settings']['userModes']:
	                if args['nick'] == user['nick'] and modeCheck('a',data):
				if 'g' in user['modes'] or args['channel'] == user['channel']:
					if 'a' in user['modes']:
		                        	return 'PART ' + args['argv'][1] + '\r\n'
						data['config']['channels'].remove(args['argv'][1])
						saveConfigChanges(data['config'])

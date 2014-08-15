def main(data):
        if '!join' in data['recv']:
                args = argv('!join',data['recv'])
                for user in data['config']['settings']['userModes']:
                        if args['nick'] == user['nick'] and modeCheck('a',data):
                                if 'g' in user['modes'] or args['channel'] == user['channel']:
                                        if args['argv'][1][0] == "#":
						#if channel not in channel list
						if not args['argv'][1].lower() in data['config']['settings']['joinChannels']:
							#add it
                                                	data['config']['settings']['joinChannels'].append(args['argv'][1].lower())
                                                	saveConfigChanges(data['config'])
                                                return 'JOIN ' + args['argv'][1] + '\r\n'

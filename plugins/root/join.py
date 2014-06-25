def main(data):
        if '!join' in data['recv']:
                args = argv('!join',data['recv'])
                for user in data['config']['settings']['userModes']:
                        if args['nick'] == user['nick'] and modeCheck('a',data):
                                if 'g' in user['modes'] or args['channel'] == user['channel']:
                                        if 'a' in user['modes'] and not args['argv'][1].lower() in data['joinChannels'] and args['argv'][1][0] == '\#':
                                                data['config']['settings']['joinChannels'].append(args['argv'][1].lower())
                                                saveConfigChanges(data['config'])
                                                return 'JOIN ' + args['argv'][1] + '\r\n'

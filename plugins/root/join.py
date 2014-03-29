def main(data):
        if '!join' in data['recv']:
                args = argv('!join',data['recv'])
                for user in data['config']['settings']['userModes']:
                        if args['nick'] == user['nick'] and modeCheck('a',data):
                                if 'g' in user['modes'] or args['channel'] == user['channel']:
                                        if 'a' in user['modes']:
                                                data['config']['channels'].append(args['argv'][1])
                                                saveConfigChanges(data['config'])
                                                return 'JOIN ' + args['argv'][1] + '\r\n'

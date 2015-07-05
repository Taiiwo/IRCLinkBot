def main(data):
    if '!listmodes' in data['recv']:
        args = argv('!listmodes', data['recv'])
        toret = ""
        for user in data['config']['settings']['userModes']:
            if args['argv'][1] == user['nick']:
                toret += say(args['channel'],user['nick'] + "'s modes: " + user['modes'])
        return toret

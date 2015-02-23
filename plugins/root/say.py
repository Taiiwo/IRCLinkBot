def main(data):
    if '!say' in data['recv']:
        args = argv("!say", data['recv'])
        if modeCheck('a', data):
            message = ' '.join(args['argv'][2:])
            data['api'].say(args['argv'][1], message)
